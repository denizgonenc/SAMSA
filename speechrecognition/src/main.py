import speech_recognition as sr

def main():
    recognizer = sr.Recognizer()

    with sr.AudioFile('e2d.mp3') as audio_file:
        recognizer.listen(audio_file)
        text = recognizer.recognize_google(audio_file)
        print(text)

if __name__ == '__main__':
    main()