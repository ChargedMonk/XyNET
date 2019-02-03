import subprocess
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import math
import contextlib

#Extracting audio from video file
command = 'ffmpeg -i video.mp4 -ab 128k -ac 1 -ar 16000 -vn -y audio.wav'
subprocess.call(command, shell=True)

fname = 'audio.wav'
outname = 'audio_filtered.wav'

cutOffFrequency = 3000.0

#passing the audio through a low pass filter
def running_mean(x, windowSize):
  cumsum = np.cumsum(np.insert(x, 0, 0))
  return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize


def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved = True):

    if sample_width == 1:
        dtype = np.uint8 # unsigned char
    elif sample_width == 2:
        dtype = np.int16 # signed 2-byte short
    else:
        raise ValueError("Only supports 8 and 16 bit audio formats.")

    channels = np.fromstring(raw_bytes, dtype=dtype)

    if interleaved:
        # channels are interleaved, i.e. sample N of channel M follows sample N of channel M-1 in raw data
        channels.shape = (n_frames, n_channels)
        channels = channels.T
    else:
        # channels are not interleaved. All samples from channel M occur before all samples from channel M-1
        channels.shape = (n_channels, n_frames)

    return channels

with contextlib.closing(wave.open(fname,'rb')) as spf:
    sampleRate = spf.getframerate()
    ampWidth = spf.getsampwidth()
    nChannels = spf.getnchannels()
    nFrames = spf.getnframes()

    # Extract Raw Audio from multi-channel Wav File
    signal = spf.readframes(nFrames*nChannels)
    spf.close()
    channels = interpret_wav(signal, nFrames, nChannels, ampWidth, True)

    # get window size
    # from http://dsp.stackexchange.com/questions/9966/what-is-the-cut-off-frequency-of-a-moving-average-filter
    freqRatio = (cutOffFrequency/sampleRate)
    N = int(math.sqrt(0.196196 + freqRatio**2)/freqRatio)

    # Use moviung average (only on first channel)
    filtered = running_mean(channels[0], N).astype(channels.dtype)

    wav_file = wave.open(outname, "w")
    wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
    wav_file.writeframes(filtered.tobytes('C'))
    wav_file.close()


#passing the audio through band pass filter
command = 'ffmpeg -i audio_filtered.wav -af "highpass=f=300, lowpass=f=3000" -y audio_filtered2.wav'
subprocess.call(command, shell=True)
#removing static noise
command = 'sox audio_filtered2.wav -n noiseprof noise.prof'
subprocess.call(command, shell=True)
command = 'sox audio_filtered2.wav audiofiltered3.wav noisered noise.prof 0.19'
subprocess.call(command, shell=True)
#amplifying the audio
command = 'ffmpeg -i audiofiltered3.wav -filter:a "volume=2" -y audio_filtered_final.wav'
subprocess.call(command, shell=True)
