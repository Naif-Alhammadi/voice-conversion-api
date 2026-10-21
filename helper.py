import os
from flask import redirect, session
from functools import wraps
import math
import numpy as np


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
        

# get some help from ChatGpt
def process_frame(samples, sample_rate):
    """Apply the project's existing grain-based pitch processing to one frame."""
    original = np.asarray(samples, dtype=np.float64)
    frame_size = len(original)
    if frame_size < 16:
        return np.rint(original).astype(np.int16)

    frame = np.rint(original).astype(np.int64).tolist()

    try:
        lags, peak = autocorrelation(frame)
        _, period = biggest_lag(lags, sample_rate)
    except (IndexError, ZeroDivisionError, ValueError):
        return np.clip(np.rint(original), -32768, 32767).astype(np.int16)

    if period < 2 or period >= frame_size:
        return np.clip(np.rint(original), -32768, 32767).astype(np.int16)

    P = period
    N = 2 * P
    marks_list = marks(frame, P)
    if not marks_list:
        return np.clip(np.rint(original), -32768, 32767).astype(np.int16)

    p_dash = target_p_dash(P)
    if p_dash < 1:
        return np.clip(np.rint(original), -32768, 32767).astype(np.int16)
    new_marks = m_dash(marks_list, p_dash, P)

    padded = np.pad(original, (N, N), mode='constant')
    output = np.zeros_like(padded, dtype=np.float64)
    weights = np.zeros_like(padded, dtype=np.float64)

    for old_pos, new_pos in zip(marks_list, new_marks):
        if old_pos < 0 or old_pos >= frame_size or new_pos < 0:
            continue

        source_start = N + old_pos
        grain = padded[source_start:source_start + N]
        if len(grain) < 2:
            continue

        window = np.hanning(len(grain))
        windowed = grain * window
        target_start = N + new_pos
        if target_start >= len(output):
            continue

        count = min(len(windowed), len(output) - target_start)
        output[target_start:target_start + count] += windowed[:count]
        weights[target_start:target_start + count] += window[:count]

    valid = weights > 1e-8
    output[valid] /= weights[valid]
    result = output[N:N + frame_size]

    # If the grain algorithm produced no usable output, preserve the original frame.
    if not np.any(np.abs(result) > 1e-8):
        result = original

    return np.clip(np.rint(result), -32768, 32767).astype(np.int16)



# get some help from ChatGpt
def robot(path):
    output_path = "static/uploads/edited_audios/edited_robot.wav"

    iWave = File()
    with open(path, "rb") as file:
        iWave.file_open(file)

    iWave.toDecimal()

    # The sample decoder below intentionally supports signed 16-bit PCM only.
    if iWave.audioFormat != 1:
        raise ValueError("Unsupported WAV format: only PCM audio is supported")
    if iWave.bitPerSample != 16:
        raise ValueError("Unsupported WAV format: only 16-bit PCM is supported")
    if iWave.numChannels < 1:
        raise ValueError("Invalid WAV file: channel count must be at least 1")

    channels = iWave.numChannels
    audio_samples = np.frombuffer(iWave.samples, dtype="<i2").copy()
    if audio_samples.size % channels != 0:
        raise ValueError("Invalid WAV data: sample count does not match channel count")

    # Reshape to [audio frame, channel] so stereo samples remain interleaved correctly.
    audio_frames = audio_samples.reshape(-1, channels)
    left_samples = audio_frames[:, 0].astype(np.int64)

    print("Sample rate:", iWave.sampleRate)
    print("Channels:", channels)
    print("Total samples in left channel:", len(left_samples))

    # Process the entire file in 1024-sample frames, including the final partial frame.
    FRAME_SIZE = 1024
    processed_samples = left_samples.copy()

    for start in range(0, len(left_samples), FRAME_SIZE):
        chunk = left_samples[start:start + FRAME_SIZE]
        original_length = len(chunk)

        if original_length < FRAME_SIZE:
            chunk_for_processing = np.pad(
                chunk,
                (0, FRAME_SIZE - original_length),
                mode="constant"
            )
        else:
            chunk_for_processing = chunk

        processed = process_frame(chunk_for_processing, iWave.sampleRate)
        processed_samples[start:start + original_length] = processed[:original_length]

    # Replace only the left channel; preserve the right channel in stereo files.
    audio_frames[:, 0] = np.clip(
        processed_samples, -32768, 32767
    ).astype(np.int16)
    iWave.samples = audio_frames.astype("<i2", copy=False).tobytes()

    # Update WAV sizes because the writer creates a standard 44-byte PCM header.
    iWave.subChunk1Size = 16
    iWave.subChunk2Size = len(iWave.samples)
    iWave.chunk_size = 36 + len(iWave.samples)
    iWave.byteRate = iWave.sampleRate * iWave.blockAlign

    iWave.toOrginalHex()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as file:
        iWave.file_save(file)


# slow down the audio (deeper voice)
def slow_down(value, path):
    output_path = "static/uploads/edited_audios/edited_slow_down.wav"

    iWave = File()
    with open(path, "rb") as file:
        iWave.file_open(file)

    iWave.toDecimal()
    iWave.sampleRate -= value

    iWave.toOrginalHex()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as file:
        iWave.file_save(file)


# speed up the audio (litter voice)
def speed_up(value, path):
    output_path = "static/uploads/edited_audios/edited_speed_up.wav"

    iWave = File()
    with open(path, "rb") as file:
        iWave.file_open(file)

    iWave.toDecimal()
    iWave.sampleRate += value

    iWave.toOrginalHex()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as file:
        iWave.file_save(file)

    

if __name__ == "__main__":
    path = "static/uploads/audios/helpng.wav"
    output_path = "static/uploads/edited_audios/edited.wav"

    # robot(path)
    # speed_up(22100, path)

    slow_down(22100, path)

    # print("Saved processed audio to:", output_path)