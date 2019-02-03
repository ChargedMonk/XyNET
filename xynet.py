from pocketsphinx import AudioFile
import time
import filter_audio


#To create timestamps for subs
def timeconv(x):
    if (str(x)).find('.') > 0:
        mil = (str(x))[((str(x)).find('.')+1):] + '0'
        remtime = time.strftime('%H:%M:%S',time.gmtime(x))
        res = remtime + ',' + mil
        return res

f = open('sub.srt', 'w')
f.close()


fps = 100
counter = 1
z = 0
h = ''
start = ''
end = ''
f = open('sub.srt', 'a')
for phrase in AudioFile(audio_file='audio_filtered_final.wav',frate=fps):  # frate (default=100)

    for s in phrase.segments(detailed=True):

        if z == 0 and s[0] != '<s>' and s[0] != '</s>':
            start = timeconv(s[2]/fps)
            z = 1
        if s[0] != '</s>' and s[0] != '<s>':
            end = timeconv(s[3]/fps)
        if s[0] != '</s>' and s[0] != '<s>' and s[0] != '<sil>':
            if s[0] != '[SPEECH]':
                if s[0].find('(')<0:
                    h = h + s[0]
                else:
                    h = h +(s[0])[:s[0].find('(')]
            else:
                h = h + '**'
            h = h + ' '

    #Writing the subtitles in sub.srt
    f.write(str(counter) + '\n'+ start + ' --> ' +end +'\n')
    f.write(h + '\n\n')
    counter += 1
    z = 0
    h = ''

f.close()
