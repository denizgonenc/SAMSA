from os.path import splitext, join
from os import remove

from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from fastapi import UploadFile

def mp3_to_wav(uploaded_file: UploadFile, output_directory: str):
    """
    The method that changes mp3 file into wav file.
    `input_file_path` is show the uploaded files path.
    """
    filename, _ = splitext(uploaded_file.filename)
    temp_file_path = join(output_directory, uploaded_file.filename)
    output_file_path = join(output_directory, filename + '.wav')
    print(temp_file_path)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.file.read())
    audio = AudioSegment.from_file(temp_file_path)
    audio.export(output_file_path, format='wav')
    remove(temp_file_path)
    return output_file_path    # Returning output file path.

def mp4_to_wav(uploaded_file: UploadFile, output_directory: str): # NOTE looks like not necessary maybe we can remove this functionality.
    """
    The method that changes mp4 file into wav file.
    `input_file_path` is show the uploaded files path.
    """
    filename, _ = splitext(uploaded_file.filename)
    temp_file_path = join(output_directory, uploaded_file.filename)
    output_file_path = join(output_directory, filename + '.wav')
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.file.read())
    audio = VideoFileClip(temp_file_path).audio    # extracting audio part from the mp4 file.
    audio.write_audiofile(output_file_path)
    remove(temp_file_path)    # remove temporaray file
    return output_file_path    # Returning wav file path.