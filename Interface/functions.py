import json

from os.path import splitext, join, abspath, basename
from os import remove, listdir

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


####################
# Speaker Commands #
####################

def get_speakers(movie_path: str, name: str):
    with open(join(movie_path, name), 'r') as json_file:
        data = json.load(json_file)
        speakers = []
        for d in data:
            if d['speaker'] not in speakers:
                speakers.append(d['speaker'])
    return speakers

def change_speaker_name(movie_path: str, name: str, old_s_name: str, new_s_name: str) -> None:
    speakers = get_speakers(movie_path, name)
    if new_s_name in speakers:
        return 'The name `{}` is already in use.'.format(new_s_name)

    json_file_path = join(movie_path, name)
    data = []
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)
        # change the speakers from data.
        for d_idx, d in enumerate(data):
            if d['speaker'] == old_s_name:
                data[d_idx]['speaker'] = new_s_name
    
    with open(json_file_path, 'w') as json_file:
        dump = json.dumps(data, indent=4)
        json_file.write(dump)
    return 'ok'

####################
# Files Commands #
####################

def get_files(movie_path: str):
    returned_extensions = ['.json', '.wav', '.mp4', '.mp3'] 
    all_files = listdir(movie_path)
    files = []
    for file in all_files:
        file_name, file_extension = splitext(file)
        if file_extension in returned_extensions:
            file_id = basename(movie_path)
            files.append({
                "name": file,
                "url": join("/files", file_id, file)
            })
    return files
