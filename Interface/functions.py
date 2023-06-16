import json

import SentimentalAnalysis.src.plots as plots

from threading import Thread
from os.path import splitext, join, basename, isdir
from os import remove, listdir, mkdir

from moviepy.editor import VideoFileClip, AudioFileClip
from fastapi import UploadFile

from SentimentalAnalysis.src.endpoint import predict_script
from SpeechRecognition.src.speaker_diarization import SpeakerDiarization


def mp3_to_wav(uploaded_file: UploadFile, output_directory: str):
    """
    The method that changes mp3 file into wav file.
    `input_file_path` is show the uploaded files path.
    """
    filename, _ = splitext(uploaded_file.filename)
    temp_file_path = join(output_directory, uploaded_file.filename)
    output_file_path = join(output_directory, filename + '.wav')
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.file.read())

    sound = AudioFileClip(temp_file_path)
    sound.write_audiofile(output_file_path, 44100, 2)
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
    try:
        audio = VideoFileClip(temp_file_path).audio    # extracting audio part from the mp4 file.
    except KeyError: # TODO test it
        audio = AudioFileClip(temp_file_path)
    audio.write_audiofile(output_file_path)
    remove(temp_file_path)    # remove temporaray file
    return output_file_path    # Returning wav file path.


#####################
# Speaker Functions #
#####################

def get_speakers(movie_path: str, name: str):
    json_path = join(movie_path, name)
    try:
        with open(json_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            speakers = []
            for d in data:
                if d['speaker'] not in speakers:
                    speakers.append(d['speaker'])
    except FileNotFoundError:
        speakers = []
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
# Files Functions  #
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


def save_JSON(json_file_path: str, data):

    with open(json_file_path, 'w') as json_file:
        dump = json.dumps(data, indent=4)
        json_file.write(dump)


####################
# Background Tasks #
####################

def run_speech_2_text(wav_file_path: str, json_file_path: str, speaker_diarization_model: SpeakerDiarization):
    json_data = speaker_diarization_model.get_text(wav_file_path)
    for d_idx, d in enumerate(json_data):
        results = {
            'sentiment': None,
            'probability': None,
            'valence': None
        }
        json_data[d_idx]['results'] = results
    save_JSON(json_file_path, json_data)

    # Apply sentiment analysis
    sentiment_results = predict_script(json_file_path)
    for idx in range(len(json_data)):
        json_data[idx]['results'] = {
            "sentiment": sentiment_results.iloc[idx]['sentiment'],
            "probability": sentiment_results.iloc[idx]['probability'],
            "valence": sentiment_results.iloc[idx]['valence']
        }

    save_JSON(json_file_path, json_data)
    print(f'INFO: Speech recognition thread for {json_file_path} is finished.')


###################
# Graph Functions #
###################

GRAPH_NAME_DICT = {
    'hist': plots.histogram_plot,
    'pie_chart': plots.pie_chart_plot,
    'characters_sentiment': plots.characters_sentiment_plot,
    'sentiment_avg_prob': plots.sentiment_avg_prob_plot
}


def create_graphs(movie_path: str, json_file_path: str, previous: Thread = None):
    if previous != None: previous.join()

    # To get sentiment model's results.
    sentiment_results = predict_script(join(movie_path, json_file_path))
    file_name, _ = splitext(json_file_path)

    # Creating graphs path.
    graphs_dir = join(movie_path, 'graphs')
    if not isdir(graphs_dir):
        mkdir(graphs_dir)

    # Generating and saving the graphs.    
    for graph_name in GRAPH_NAME_DICT:
        graph_func = GRAPH_NAME_DICT[graph_name]
        graph_path = join(graphs_dir, f'{graph_name}_{basename(file_name)}.png')
        plt_mod = graph_func(sentiment_results)
        current_fig = plt_mod.gcf()
        current_fig.set_size_inches((10.66, 6))
        current_fig.savefig(graph_path, dpi='figure')
        plt_mod.clf()
    print(f'INFO: Sentimental analysis thread for {json_file_path} is finished.')


def get_graphs(movie_path: str) -> list:
    graphs = []

    try:
        graphs_path = join(movie_path, 'graphs')
            
        for graph_path in listdir(graphs_path):
            graph = {
                'path': f'/files/{basename(movie_path)}/graphs/{basename(graph_path)}'
            }
            graphs.append(graph)

    except FileNotFoundError: pass

    return graphs
