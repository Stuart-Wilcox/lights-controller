import os
import pyaudio
import wave
import numpy as np
import struct


chunk = 1024
sample_format = pyaudio.paInt16
channels = 1
fs = 44100
seconds = 60
filename = 'out.wav'
input_device_index=1

rows, columns = os.popen('stty size', 'r').read().split()

p = pyaudio.PyAudio()

stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)

def analyse(data):
    data = struct.unpack('{n}h'.format(n=chunk), data)
    data = np.array(data)
    data_fft = np.fft.fft(data)
    frequencies = np.abs(data_fft)
    if frequencies.size > 0:
        frequencies = frequencies / np.sqrt(np.sum(frequencies**2)) # normalize

    bottom = np.amin(frequencies)
    top = np.amax(frequencies)
    diff = top - bottom

    low = []
    high = []
    for f in frequencies:
        if f < 0.25:
            low.append('X')
        elif f >= 0.25:
            high.append('Y')
    low = low[0:int(columns) // 2]
    high = high[0:int(columns) // 2]

    low_str = ''.join(low)
    low_str += ' ' * ((int(columns)//2)-len(low))
    high_str = ''.join(high)
    high_str += ' ' * ((int(columns)//2)-len(high))
    print('{low}|{high}'.format(low=low_str, high=high_str))


frames = []
for i in range(0, int(fs / chunk * seconds)):
    data = stream.read(chunk)
    analyse(data) 
    frames.append(data)

stream.stop_stream()
stream.close()

p.terminate()

wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()
