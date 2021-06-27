NDEF_WELLKNOWNRECORD       = 0x1

NDEF_RECORDTYPE_TEXT       = 0x54
NDEF_RECORDTYPE_URI        = 0x55

NDEF_TEXT_UTF8             = 0x02

class Record(object):
    def __init__(self):
        self.ndefType   = NDEF_WELLKNOWNRECORD
        self.recordType = NDEF_RECORDTYPE_TEXT
        self.definition = NDEF_TEXT_UTF8
        self.language   = "en"
        self.value      = ""

class Message(object):
    def __init__(self):
        self.records = []
        self.buffer = bytearray()

    def setRecords(self, records):
        self.records = records

    def getRecords(self):
        return self.records

    def setBuffer(self, buffer):
        self.buffer = buffer

    def getBuffer(self):
        return self.buffer

    def addTextRecord(self, value):
        record = Record()
        record.value = value
        self.records.append(record)
        return self.records[len(self.records) -1]

    def encode(self):
        payloadLength = 0
        records = self.getRecords()
        recordCount = len(records)

        for i in range(recordCount):
            payloadLength += len(records[i].value) + 7

        buffer = bytearray(payloadLength + 3)
        buffer[0] = 0x03
        buffer[1] = payloadLength
        buffer[2] = 0xD1
        if recordCount >= 2:
            buffer[2] = 0x91

        bufferIndex = 3
        for i in range(recordCount):
            buffer[bufferIndex] = records[i].ndefType
            bufferIndex += 1
            buffer[bufferIndex] = len(records[i].value) + 3
            bufferIndex += 1
            buffer[bufferIndex] = records[i].recordType
            bufferIndex += 1
            buffer[bufferIndex] = records[i].definition
            bufferIndex += 1
            buffer[bufferIndex] = records[i].language[:1].encode()[0]
            bufferIndex += 1
            buffer[bufferIndex] = records[i].language[1:].encode()[0]
            bufferIndex += 1

            for r in range(len(records[i].value)):
                buffer[bufferIndex] = str(records[i].value[r]).encode()[0]
                bufferIndex += 1

            buffer[bufferIndex] = 0xFE

            if recordCount >= 2 and i <= recordCount - 3:
                buffer[bufferIndex] = 0x11
                bufferIndex += 1

            elif recordCount >= 2 and i <= recordCount - 2:
                buffer[bufferIndex] = 0x51
                bufferIndex += 1

        self.setBuffer(buffer)

        return self.getBuffer()

    def decode(self):
        buffer = self.getBuffer()
        records = []

        ndef = buffer[0]
        payloadLength = buffer[1]
        chunker = buffer[2]

        if ndef == 0x03:
            # Record found
            recordParser = []
            for i in range(3,len(buffer)):
                # Find end of record
                if buffer[i] == 0x11 or buffer[i] == 0x51 or buffer[i] == 0xFE:
                    record = Record()
                    record.ndefType = recordParser[0]
                    record.recordType = chr(recordParser[2])
                    record.definition = recordParser[3]
                    record.language = ''.join(chr(i) for i in recordParser[4:6])
                    record.value = ''.join(chr(i) for i in recordParser[6:])
                    records.append(record)
                    recordParser = []
                else:
                    recordParser.append(buffer[i])
                # End of message, exit loop
                if buffer[i] == 0xFE:
                    break

        self.setRecords(records)
        return self.getRecords()