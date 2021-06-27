import time

import myPN532 as PN532
import myNDEF  as ndef

SCLK =  4
MISO = 17
MOSI = 27
CS   = 22

DEFAULT_KEY = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

class response(object):
    def __init__(self):
        self.type = ''
        self.data = ''
        self.message = ''

# Start PN532 comms by calling myPN532.PN532
def getPn532():
    try:
        pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
        pn532.begin()
        pn532.SAM_configuration()
        return pn532
    except:
        return None

def createBlockMatrix(data):
    byteMatrix = [[None for x in range(16)] for y in range(44)]
    valueArray = []
    while data:
        valueArray.append(data[:16].ljust(16))
        data = data[16:]

    idx = 0
    while idx < len(byteMatrix):
        byteMatrix[idx] = bytearray(16)
        if len(valueArray) > idx:
            byteMatrix[idx] = bytearray(valueArray[idx])
        idx += 1

    return byteMatrix

# Create Page Matrix
def createPageMatrix(data):
    byteMatrix = [[None for x in range(4)] for y in range(35)]
    valueArray = []
    while data:
        valueArray.append(data[:4].ljust(4))
        data = data[4:]

    idx = 0
    while idx < len(byteMatrix):
        byteMatrix[idx] = bytearray(4)
        if len(valueArray) > idx:
            byteMatrix[idx] = bytearray(valueArray[idx])
        idx += 1

    return byteMatrix

# Create blockArray
def blockArray():
    blocks = []
    skipper = 0
    for i in range(4,64):
        skip = False
        if skipper == 3:
            skipper = -1
            skip = True
        if skip ==False:
            blocks.append(i)
        skipper += 1
    return blocks

# Check for empty block
def isBlockEmpty(block):
    isEmpty = True
    for char in block:
        if char != 0x00:
            isEmpty = False
    return isEmpty

# Write game data to RFC
def write(message):
    resp = response()
    buffer = message.encode()
    pn532 = getPn532()
    cardType = 'unknown'

    if pn532 != None:

        maxAttempts = 5
        attempts = 0

        uid = pn532.read_passive_target()
        while uid is None:
            if attempts >= maxAttempts:
                resp.type = 'error'
                resp.message = 'Unable to find tag, try reseating it'
                resp.data = ''
                pn532.shutdown()

                return response
            uid = pn532.read_passive_target()
            attempts = attempts + 1
            time.sleep(0.5)

        if len(uid) == 4:
            #MiFare Classic detected
            cardType = 'mifareclassic'
        elif len(uid) == 7:
            #MiFare Ultralight or Ntag2xx dectected
            cardType = 'ntag2xx'

        if cardType == 'mifareclassic':

            blocks = blockArray()
            bytesToWrite = createBlockMatrix(buffer)

            # UID obtained, write data
            for block in range(len(blocks)):
                if not pn532.mifare_classic_authenticate_block(uid, blocks[block], PN532.MIFARE_CMD_AUTH_B, DEFAULT_KEY):
                    resp.type = 'error'
                    resp.message = 'Failed to authenticate block {0} with the card.'.format(block)
                    resp.data = ''
                    pn532.shutdown()

                    return resp
                data = bytesToWrite[block]

                if not pn532.mifare_classic_write_block(blocks[block], data):
                    resp.type = 'error'
                    resp.message = 'Failed to write block {0}!'.format(block)
                    resp.data = ''
                    pn532.shutdown()

                    return resp

                if isBlockEmpty(data):
                    break

            resp.type = 'success'
            resp.message = 'Message written successfully.'
            resp.data = ''

        elif cardType == 'ntag2xx':
            blocks = blockArray()
            bytesToWrite = createPageMatrix(buffer)

            # Data starts at page 4
            page = 4
            for i in range(0,34):
                byteIndex = i*4
                data = buffer[byteIndex:byteIndex+4]
                len_diff = 4 - len(data)
                data += "\0".encode()*len_diff

                if not pn532.ntag2xx_write_page(page, data):
                    resp.type = 'error'
                    resp.messge = 'Failed to write page {0}!'.format(page)
                    resp.data = ''
                    pn532.shutdown()

                    return resp
                page += 1

                if isBlockEmpty(data):
                   break

            resp.type = 'success'
            resp.message = 'Message written successfully.'
            resp.data = ''

        # Shutdown after writing
        pn532.shutdown()
    else:
        resp.type = 'error'
        resp.message = 'Unable to find NFC device.'
        resp.data = ''

    return resp

def read():
    # Format to NDEF if not already
    message = ndef.Message()
    resp = response()
    blocks = blockArray()
    pn532 = getPn532()
    cardType = 'unknown'
    if pn532 != None:

        resp.type = ""
        resp.message = ""
        resp.data = ""

        bufferFromCard = []
        maxAttempts = 2
        attempts = 0

        uid = pn532.read_passive_target()
        while uid is None:
            if attempts >= maxAttempts:
                resp.type = 'error'
                resp.message = 'Unable to find tag, try reseating'
                resp.data = ''
                pn532.shutdown()

                return resp
            uid = pn532.read_passive_target()
            attempts = attempts + 1
            time.sleep(0.2)

        if len(uid) == 4:
            # MiFare classic
            cardType = 'mifareclassic'
        elif len(uid) == 7:
            # MiFare Ultarlight or Ntag2xx
            cardType = 'ntag2xx'

        if cardType == 'mifareclassic':
            # UID obtained, now read data
            for block in range(len(blocks)):
                if not pn532.mifare_classic_authenticate_block(uid, blocks[block], PN532.MIFARE_CMD_AUTH_B, DEFAULT_KEY):
                    resp.type = 'error'
                    resp.message = 'Failed to authenticate block {0} with the card.'.format(block)
                    resp.data = ''
                    pn532.shutdown()

                    return resp
                else:
                    data = pn532.mifare_classic_read_block(blocks[block])
                    if data is None:
                        resp.type = 'error'
                        resp.message = 'Failed to read block {0}!'.format(block)
                        resp.data = ''
                        pn532.shutdown()

                        return resp
                    else:
                        if isBlockEmpty(data):
                            break
                        bufferFromCard += data

            message.setBuffer(bufferFromCard)
            message.decode()

            resp.type = 'success'
            resp.message = 'success'
            resp.data = message

        elif cardType == 'ntag2xx':
            # Data starts at page 4
            for page in range(4,39):
                data = pn532.ntag2xx_read_page(page)
                if data is None:
                    resp.type = 'error'
                    resp.message = 'Failed to read page {0}!'.format(page)
                    resp.data = ''
                else:
                    if isBlockEmpty(data):
                        break
                    bufferFromCard.extend(data)
            if bufferFromCard[0] != 0x3:
                # Move forward 5 bytes to get to NDEF records
                newBuffer = bufferFromCard[5:]
                bufferFromCard = newBuffer

            message.setBuffer(bufferFromCard)
            message.decode()

            resp.type = 'success'
            resp.message = 'success'
            resp.data = message

        pn532.shutdown()
    else:
        resp.type = 'error'
        resp.message = 'Unable to find NFC device.'
        resp.data = ''

    return resp