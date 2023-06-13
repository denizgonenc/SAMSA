from dotenv import load_dotenv
import json
from moviepy.editor import AudioFileClip
import os
from pocketsphinx import Segmenter
import re
import requests
import wave


load_dotenv('../..')
print(os.getenv("HF_API_TOKEN"))

class AudioController:

    API_URL = "https://api-inference.huggingface.co/models/harshit345/xlsr-wav2vec-speech-emotion-recognition"
    headers = {"Authorization": "Bearer {}".format(os.getenv("HF_API_TOKEN"))}

    MOVIE_DIR = "movies"

    def mp3_to_wav(mp3_file_name: str):
        """
        Gets mp3 file and turns it into wav file and stores in the related directory.
        {BASE_DIRECTORY}/movies/{id}
        """
        try:
            output_file_name, extension = os.path.splitext(mp3_file_name)
        except:
            "There is a problem about input file name."
        sound = AudioFileClip(mp3_file_name)
        sound.write_audiofile(output_file_name + ".wav", 44100, 2)


    def div2segments(wav_file_name):
        """
        Divides one file into uninterrupted, meaningful multiple parts.
        in => wav_file.
        out => wav segments. (Ex: s3_example_wav_file_12.2-14.6.wav)
        """
        with wave.open(wav_file_name, "rb") as input_file:
            segmenter = Segmenter(sample_rate=input_file.getframerate())
            segments = segmenter.segment(input_file.getfp())

            channel_num = input_file.getnchannels()

            for seg, seg_index in zip(segments, len(range(segments))):
                f1 = (seg.start_time / channel_num)
                f2 = (seg.end_time / channel_num)
                fname = os.path.splitext(wav_file_name)
                output_file_name = "s{i}_{fname}_{f1}-{f2}.wav".format(i=seg_index, fname=fname, f1=f1, f2=f2)

                with wave.open(output_file_name, "wb") as output_file:
                    output_file.setnchannels(channel_num)
                    output_file.setsampwidth(2)
                    output_file.setframerate(input_file.getframerate())
                    output_file.writeframesraw(seg.pcm)


    def sentiment_analysis_on_audio(id: int):
        """
        Sends a wav file segment into HF API and gets the emotional results from it. 
        """

        AudioController.mp3_to_wav(str(id))     # removes 


        with open(filename, "rb") as f:
            data = f.read()
        response = requests.request("POST", AudioController.API_URL, headers=AudioController.headers, data=data)
        return json.loads(response.content.decode("utf-8"))



    def main():
        file_names = [file for file in os.listdir(OUTPUT_DIR)]
        mp3_to_wav('e2d.mp3')
        

        # file_names = [file for file in os.listdir(OUTPUT_DIR) if file.split('_') == re.search("s[0-9]*")]
        # output = sentiment_analysis_on_audio()


if __name__ == '__main__':
    AudioController

