import speech_recognition as sr
import moviepy.editor as mp

from pydub import AudioSegment
from pydub.playback import play
from pydub.silence import split_on_silence
from os import listdir

def main():
    recognizer = sr.Recognizer()

    # clip = mp.AudioFileClip(r"elementary-podcasts-s01-e01.mp3") 
    # clip = mp.AudioFileClip(r"e2d.mp3") 
    
    # clip.write_audiofile(r"converted.wav")

    # sound = AudioSegment.from_mp3("e2d.mp3")
    print(listdir())
    audio_segment = AudioSegment.from_mp3('./e2d.mp3')
    audio_segment.export('e2d.wav', format='wav')
    
    # chunks = split_on_silence('converted.wav',
    #     min_silence_len = 50,
    #     silence_thresh = -1
    # )

    # play(sound)

    print(len(chunks))

    for chunk in chunks:
        with sr.AudioFile(chunk) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            with open('s2t.txt', 'a') as file:
                file.write(text)
                file.write('======================chunk===================')


if __name__ == '__main__':
    main()


# mp3 -> text ?
# wav -> text
# chunking in wav file (constantly gives 1) 
# 
# clustering. #