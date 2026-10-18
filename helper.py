import os
from flask import redirect, session
from functools import wraps
import math


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
        decimal = 0

        # to keep every reminder of a number
        little = []
        for i in range(0 , len(hexa)):

            # to keep track of the current number in the list
            result = hexa[i] * (256 ** i)
            
            little.append(result)
            
        
        # for each hex in reminder
        for num in little:
            decimal += num

        

        return decimal


    
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


# take a chunk of samples and return its lags
def autocorrelation(lSamples):
    # heighest value
    peak = 0

    lag = 0

    # copy one of samples's direction (left)
    ns = lSamples[:]

    # keep track of all lag values
    lags = []

    # counting the first peak value
    for n in ns:
        peak += n * n

    # skip the first (peak) value and keep track of the while loop
    l = 1


    while True:

        # displacement process
        ns.pop()
        ns.insert(0, 0)
        nSos = ns


        # calculate each lag of each displacement 
        # learn the zip function from chatGPT
        for (n, nSo) in zip(lSamples, nSos):
            lag += n * nSo


        # terminate the while loop
        if l == len(ns):
            break

        # gather lag values
        lags.append(lag)

        # update while lenght
        l = l + 1

        # reset current lag value after appending to the lags list
        lag = 0

    return lags, peak


# takes lag values and return the biggest value and its position
def biggest_lag(lags, samplerate):
    fk = 0
    max = round(samplerate // 80)
    min = round((samplerate // 400) - 1)
    biggest = lags[min:max][0]

    for (k, lag) in enumerate(lags[min:max]):
        if lag > biggest:
            biggest = lag
            fk = k
    fk += min + 1
    return biggest, fk


# DFT algorithm
def dft (xs):
    evens = list()
    odds = list()

    # determine even, odd numbers
    for i, x in enumerate(xs):
        if i % 2 == 0:
            evens.append(x)
        else:
            odds.append(x)

    # even's opration
    Es_plus = 0
    Es_sub = 0

    for i, e in enumerate(odds):
        Es_plus += e
        Es_sub -= e
        if i == 0:
            Es_sub = Es_sub * -1


    # odds opratino
    Os_plus = 0
    Os_sub = 0

    for i, e in enumerate(evens):
        Os_plus += e
        Os_sub -= e
        if i == 0:
            Os_sub = Os_sub * -1

    Es = list()
    Es.append(Es_plus)
    Es.append(Es_sub)

    Os = list()
    Os.append(Os_plus)
    Os.append(Os_sub)


    return Es, Os


# return Twiddle value
def Twiddle (k, n):
    TWO_PI = 360

    cos = math.cos(math.radians((TWO_PI * k) // n))
    sin = math.sin(math.radians((TWO_PI * k) // n))

    result = cos - sin

    # return the appropriate format
    if sin == 0:
        return result

    if result == -1:
        return '-j'

    return 'j'


# separate evens and odds to real and imaginary
def real_imaginary(length, E, O):
    real = list()
    imaginary = list()
    j_indexs = list()
    print("heloo", length)

    # to determine the next even, odd number
    i = 0
    for index in range(0, length):
        if i == (4 // 2):
            i = 0

        # if Twiddle value is not a number
        if type(Twiddle(i, length)) == str:
            j_indexs.append(index)
            real.append(E[i])

            # if Twiddle is a negative value
            if Twiddle(index, length) == "-j":
                imaginary.append(O[i])
            else:
                imaginary.append(O[i] * -1)

            # update current index
            i += 1
            continue
                
        if index >= length // 2:
            real.append(E[i] - Twiddle(i, length) * O[i])
            i += 1
            continue
    
        real.append(E[i] + Twiddle(i, length) * O[i])
        i += 1

    return real , imaginary, j_indexs



# count magnitudes
def magnitude(real, imaginary, j_indexs):
    magns = list()

    # length of the biggest real
    length = len(real)

    # the index of imagainary 
    imaginary_index = 0
    
    for i in range(0, length):
        if i in j_indexs:
            # magnitude calculation
            mang = math.sqrt((real[i] ** 2) + (imaginary[imaginary_index] ** 2))

            magns.append(mang)

            # update imaginary index
            imaginary_index += 1
            continue

        # turn to positive values
        magns.append(abs(real[i]))

    return magns



# Hertzs of the audio
def Hz(k, fs, n):
    Hzs = list()

    for i in range(len(k)):
        # hertz's calculation
        hz = i * fs // n

        # skip the value of hz if it is grater than the half of the sampleRates
        if fs // 2 < hz:
            continue

        Hzs.append(hz)

    return Hzs


# smooth (round) magnitude values
def spectral_smoothing(magnitudes):
    total_magni = 0
    Ss = list()


    for i in range(len(magnitudes)):
        total_magni = 0
        
        # smooth's calculation of the first number in the list
        if i == 0:
            for j in range(len(magnitudes) - 1):
                total_magni += magnitudes[j]
            Ss.append(total_magni / 3)
            continue

        # smooth's calculation of the last number in the list
        if i == len(magnitudes) - 1:
            for j in range(len(magnitudes)):
                if j + 1 == len(magnitudes):
                    Ss.append(total_magni / 3)
                    break
                total_magni += magnitudes[j + 1]
            continue

        # smooth's calculation of the middle numbers in the list
        total_magni += magnitudes[i]
        total_magni += magnitudes[i - 1]
        total_magni += magnitudes[i + 1]
        Ss.append(total_magni / 3)

        
    # return magnitude values after smoothing
    return Ss



# determine the biggest value of the smoothing function values
def peak_index(smoothing):
    # start with the first value in the list as the biggest
    biggest = smoothing[0]

    # for the biggest value index
    index = 0

    for i, num in enumerate(smoothing):
        if num > biggest:
            biggest = num
            index = i

    # remove the biggest value from the real list
    smoothing.remove(biggest)

    # return the index of the removed value
    return (index + 1)


# mark the aduio
def marks(leftSamples, k_lag):
    # determine the bigges sample
    biggest_sample = leftSamples[k_lag - k_lag]
    marks = []
    sample = 1024

    # for the biggest sample index
    postion = 0

    for i, lsample in enumerate(leftSamples[0 : k_lag]):
        if lsample > biggest_sample:
            biggest_sample = lsample
            postion = i

    marks.append(postion)

    # take the next value of the list
    update = 0

    # to end the while loop
    ter = k_lag
    while True:
        marks.append(marks[update] + k_lag)
        update += 1
        ter += k_lag

        if ter >= sample:
            break
        
    return marks


# calculate the f dash value
def f_dash(f0, target_r=2):
    f_dash = f0 * target_r
    return f_dash


# calculate the p dash value
def target_p_dash(k_lag, target_r=2):
    p_dash = k_lag // target_r
    return p_dash


# calculate the m dash value
def m_dash(marks, p_dash, k_lag):
    ms_dash = list()
    ms_dash.append(marks[0])
    for i in range(1, k_lag):
        ms_dash.append(ms_dash[i - 1] + p_dash)

    return ms_dash
        

if __name__ == "__main__":
    path = "uploads/audios/helpng.wav"
    iWave = File()
    with open(path, 'rb') as file:
        iWave.file_open(file)
        leftSample = list()
        start = 0
        inc = 2

        iWave.toDecimal()
        
        while True:
            lSample = iWave.hexToDecimalFormat(iWave.samples[start:inc])
            if lSample >= 2 ** 15:
                lSample -= 2 ** 16
            leftSample.append(lSample)
            if inc == 4096 - 2:
                break

            inc += 4
            start += 4
        
        # ------------------ audio process -----------------

        lags, peak = autocorrelation(leftSample)

        lag, k = biggest_lag(lags, iWave.sampleRate)
        f0 = iWave.sampleRate // k
        print(k, "k")
        print(f0, "F0")

        even, odd = dft(leftSample)
        real , imaginary, j_indexs = real_imaginary(len(leftSample), even, odd)
        magnis = magnitude(real, imaginary, j_indexs)
        s = spectral_smoothing(magnis)
        index1 = peak_index(s) 
        index2 = peak_index(s)
        index3 = peak_index(s)
        f1 = index1 * (iWave.sampleRate // 1024)
        f2 = index2 * (iWave.sampleRate // 1024)
        f3 = index3 * (iWave.sampleRate // 1024)
        print(f1, "f1")
        print(f2, "f2")
        print(f3, "f3")
        print("======================")

        P = k
        N = 2 * P
        
        Marks = marks(leftSample, P)
        p_dash = target_p_dash(P)
        ms_dash = m_dash(Marks, p_dash, P)




    iWave.toOrginalHex()

    os.makedirs("uploads/edited_audios", exist_ok=True)
    with open("uploads/edited_audios/man2.wav", "wb") as file:
        iWave.file_save(file)