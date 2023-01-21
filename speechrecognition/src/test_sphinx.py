import wave

from pocketsphinx import Segmenter
from moviepy.editor import AudioFileClip

def main():
    output_file_name = 'converted_file.wav'

    sound = AudioFileClip('the-hobbit-official-trailer-1-lord-of-the-rings-movie-2012-hd.mp3')
    sound.write_audiofile(output_file_name, 44100, 2)

    with wave.open(output_file_name, "rb") as input_file:
        segmenter = Segmenter(sample_rate=input_file.getframerate())
        segments = segmenter.segment(input_file.getfp())

        channel_num = input_file.getnchannels()

        for seg in segments:
            print(seg.start_time / channel_num, seg.end_time / channel_num)
            with wave.open(output_file_name + "_%.2f-%.2f.wav"% (seg.start_time / channel_num,
             seg.end_time / channel_num), "wb") as output_file:
                output_file.setnchannels(channel_num)
                output_file.setsampwidth(2)
                output_file.setframerate(input_file.getframerate())
                output_file.writeframesraw(seg.pcm)


if __name__ == '__main__':
    main()

