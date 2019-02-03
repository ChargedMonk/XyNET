# XyNET
:clapper: A Python package that creates subtitles (closed captions) for a video.

Audio is extracted from video using ffmpeg.
Then the audio is converted into a single channel and downsampled to 16KHz.
In the next step audio is passed through a low pass filter to remove signals with frequency greater than 3KHz.
Audio is then passed through a ffmpeg's bandpass filter ranging from 300Hz to 3KHz (which is the average frequency range in which humans speak).
Then static noise profile is created and then the noise is removed using sox.
Then using ffmpeg the audio is amplified.
Then the words from the speech in the audio are extracted using PocketSphinx speech recognition module.
These words are wrapped into sentences and written in .srt file.
