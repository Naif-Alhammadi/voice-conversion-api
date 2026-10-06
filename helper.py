import os
from flask import redirect, session
from functools import wraps
import wave


def login_required(f):
    """ Decorate routes to require login. """
    @wraps(f)
    def decorate(*args, **kargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kargs)

    return decorate


class File:

    HALF_BYTE = 4

    def __init__(self):
        self.fileFormat = True
        self.fmt = ''
        self.iRIFF = ''
        self.iWAVE = ''
        self.subChunk1Size = 0
        self.numChannels = 1

        self.audioFormat = 'PCM'
        self.numChannels = 'stereo'
        self.sampleRate = 0
        self.chunk_size = 0
        self.byteRate = 0
        self.blockAlign = 0
        self.bitPerSample = 0
        self.data = ''
        self.subChunk2Size = 0
        self.samples = ''


    def file_open(self, file):
        """"Read Wave Audio File"""

        # read by 4 byte
        chunkSize = File.HALF_BYTE

        # keep updatine file read cursor
        while True:

            # read file each time by the zie of the chunkSize
            file_chunk = file.read(chunkSize)

            # if first 4 byte is RIFF IMB stander format
            if (file_chunk == b'RIFF'):
                self.iRIFF = b'RIFF'
                continue

            if (not self.chunk_size):
                self.chunk_size = file_chunk
                continue

            # second 4 byte is WAVE standard .wav files
            if(file_chunk == b'WAVE'):
                self.iWAVE = b'WAVE'
                continue

            if(file_chunk == b'fmt '):
                self.fmt = file_chunk
                chunk = chunkSize
                self.subChunk1Size = file.read(chunk)
                self.audioFormat = file.read(chunk - 2)

                stereo = file.read(chunk - 2)
                if stereo == b'\x02\x00':
                    self.numChannels = b'\x02\x00'

                self.sampleRate = file.read(chunkSize)
                continue

            if (not self.byteRate):
                self.byteRate = file_chunk
                self.blockAlign = file.read(chunkSize - 2)
                self.bitPerSample = file.read(chunkSize - 2)
                continue

            if (file_chunk == b'data'):
                self.data = b'data'
                continue

            if (not self.subChunk2Size):
                self.subChunk2Size = file_chunk
                break

            self.fileFormat = False

        self.samples = file.read()


    # convert attributes from hex to decimal
    def toDecimal(self):
        self.subChunk1Size = self.hexToDecimalFormat(self.subChunk1Size)
        self.subChunk2Size = self.hexToDecimalFormat(self.subChunk2Size)
        self.byteRate = self.hexToDecimalFormat(self.byteRate)
        self.blockAlign = self.hexToDecimalFormat(self.blockAlign)
        self.bitPerSample = self.hexToDecimalFormat(self.bitPerSample)
        self.sampleRate = self.hexToDecimalFormat(self.sampleRate)
        self.chunk_size = self.hexToDecimalFormat(self.chunk_size)
        self.numChannels = self.hexToDecimalFormat(self.numChannels)
        self.audioFormat = self.hexToDecimalFormat(self.audioFormat)


    # convert attributes from hex to decimal
    def toOrginalHex(self):

        # know to_byte method from ChatGPT
        self.subChunk1Size = self.subChunk1Size.to_bytes(File.HALF_BYTE, "little")
        self.subChunk2Size = self.subChunk2Size.to_bytes(File.HALF_BYTE, "little")
        self.byteRate = self.byteRate.to_bytes(File.HALF_BYTE, "little")
        self.blockAlign = self.blockAlign.to_bytes(File.HALF_BYTE // 2, "little")
        self.bitPerSample = self.bitPerSample.to_bytes(File.HALF_BYTE // 2, "little")
        self.sampleRate = self.sampleRate.to_bytes(File.HALF_BYTE, "little")
        self.chunk_size = self.chunk_size.to_bytes(File.HALF_BYTE, "little")
        self.numChannels = self.numChannels.to_bytes(File.HALF_BYTE // 2, "little")
        self.audioFormat = self.audioFormat.to_bytes(File.HALF_BYTE // 2, "little")



    # repersent current object deatils
    def __str__(self):
        return f"RIFF = {self.iRIFF}, ChunkSize = {self.chunk_size}, FMT = {self.fmt}, Subchunk1Size = {self.subChunk1Size}, AudioFormat = {self.audioFormat}, NumChannels = {self.numChannels}, sampleRate = {self.sampleRate}, byteRate = {self.byteRate}, blockAlign = {self.blockAlign}, bitPerSample = {self.bitPerSample}, data = {self.data}, subchunk2Size = {self.subChunk2Size}"


    def hexToDecimalFormat(self, hexa):
        """"Take decimal (binary hexdecimals) values and format (return) them in reverse values"""


        # hexdecimal base
        hex = 16

        # final hexdecimal value after taking it from the list
        hexValue = ''

        # to keep every reminder of a number
        reminder = []
        for i in range(0 , len(hexa)):

            # to keep track of the current number in the list
            result = hexa[i]

            # keep dividing until division reaches 0
            while result != 0:

                # value of base 16
                num = result % hex

                # insert that value to the beginning for the sampleRate
                reminder.insert(0, self.hexLetters(num))

                # update the result division
                result = result // hex

        # for each hex in reminder
        for num in reminder:

            # append hex value in one string
            hexValue = hexValue + str(num)

        # return the value in reverse with base 10th
        return int(hexValue, hex)

    
    def hexLetters(self, num):
        """""Convert the number to its appropriate hexdecimal value"""
        match num:
            case 15:
                num = 'f'
                return num
            case 14:
                num = 'e'
                return num
            case 13:
                num = 'd'
                return num
            case 12:
                num = 'c'
                return num
            case 11:
                num = 'b'
                return num
            case 10:
                num = 'a'
                return num
            case _:
                return num



    def file_save(self, file):
        """"Save Wave Audio File"""
        file.write(self.iRIFF)
        file.write(self.chunk_size)
        file.write(self.iWAVE)
        file.write(self.fmt)
        file.write(self.subChunk1Size)
        file.write(self.audioFormat)
        file.write(self.numChannels)
        file.write(self.sampleRate)
        file.write(self.byteRate)
        file.write(self.blockAlign)
        file.write(self.bitPerSample)
        file.write(self.data)
        file.write(self.subChunk2Size)
        file.write(self.samples)


if __name__ == "__main__":
    path = "uploads/audios/lack in.wav"
    iWave = File()
    with open(path, 'rb') as file:
        iWave.file_open(file)

    print(iWave)
    iWave.toDecimal()
    iWave.sampleRate += 15000
    iWave.toOrginalHex()
    print(iWave)


    os.makedirs("uploads/edited_audios", exist_ok=True)
    with open("uploads/edited_audios/man2.wav", "wb") as file:
        iWave.file_save(file)