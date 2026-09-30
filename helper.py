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
    def __init__(self, path):
        self.path = path
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


        self.file_open()

    def file_open(self):
        with open(self.path, 'rb') as file:

            # read file if it contain RIFF and WAVE signature

            # read by 4 byte
            chunkSize = 4

            while True:

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
                    self.fmt = b'fmt'
                    chunk = chunkSize
                    self.subChunk1Size = file.read(chunk)
                    self.audioFormat = file.read(chunk - 2)
                    if self.audioFormat == b'\x01\x00':
                        self.audioFormat = b'PCM'

                    stereo = file.read(chunk - 2)
                    if stereo == b'\x02\x00':
                        self.numChannels = 2

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
        self.subChunk1Size = self.hexToDecimal(self.subChunk1Size)
        self.subChunk2Size = self.hexToDecimal(self.subChunk2Size)
        self.byteRate = self.hexToDecimal(self.byteRate)
        self.blockAlign = self.hexToDecimal(self.blockAlign)
        self.bitPerSample = self.hexToDecimal(self.bitPerSample)
        self.sampleRate = self.hexToDecimal(self.sampleRate)
        self.chunk_size = self.hexToDecimal(self.chunk_size)



    # repersent current object deatils
    def __str__(self):
        return f"RIFF = {self.iRIFF}, ChunkSize = {self.chunk_size}, FMT = {self.fmt}, Subchunk1Size = {self.subChunk1Size}, AudioFormat = {self.audioFormat}, NumChannels = {self.numChannels}, sampleRate = {self.sampleRate}, byteRate = {self.byteRate}, blockAlign = {self.blockAlign}, bitPerSample = {self.bitPerSample}, data = {self.data}, subchunk2Size = {self.subChunk2Size}"


    def hexToDecimal(self, hexa):
        """"Take hexdecimal values and convert (return) them to decimal values"""
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

        # return the value in base 16th
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


if __name__ == "__main__":
    f = File("uploads/audios/lack in.wav")
    print(f)
    f.toDecimal()
    print(f)