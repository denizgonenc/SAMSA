import json
import whisper
import datetime
import torch
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
embedding_model = PretrainedSpeakerEmbedding( 
    "speechbrain/spkrec-ecapa-voxceleb",
    device=torch.device("cpu"))
from pyannote.audio import Audio
from pyannote.core import Segment
import wave
import contextlib
import pickle
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

class SpeakerDiarization:
    MODEL_CACHE_FILE = 'model_cache.pkl'

    def __init__(self):
        self.model = self.load_model()

    def load_model(self):
        try:
            print("INFO: The Speaker Diarization model file is found.")
            with open(SpeakerDiarization.MODEL_CACHE_FILE, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("INFO: Loading the Speaker Diarization model file.")
            model = whisper.load_model('medium')
            self.freeze_model(model)
            with open(SpeakerDiarization.MODEL_CACHE_FILE, 'wb') as f:
                pickle.dump(model, f)
            return model

    def freeze_model(self, model):
        model.eval()
        for param in model.parameters():
            param.requires_grad = False

    def get_text(self, file_name):
        result = self.model.transcribe(file_name)
        segments = result["segments"]

        with contextlib.closing(wave.open(file_name, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        audio = Audio()

        def segment_embedding(segment):
            start = segment["start"]
            end = min(duration, segment["end"])
            clip = Segment(start, end)
            waveform, sample_rate = audio.crop(file_name, clip)

            if waveform.ndim > 1:
                waveform = waveform[0]

            waveform = waveform.unsqueeze(0).unsqueeze(0)

            return embedding_model(waveform)

        embeddings = np.zeros(shape=(len(segments), 192))

        for i, segment in enumerate(segments):
            embeddings[i] = segment_embedding(segment)

        embeddings = np.nan_to_num(embeddings)

        silhouette_scores = []
        K = range(2, len(segments) + 1)
        for k in K:
            kmeans = KMeans(n_clusters=k)
            labels = kmeans.fit_predict(embeddings)
            num_unique_labels = len(np.unique(labels))
            if num_unique_labels < 2 or num_unique_labels >= len(embeddings):
                continue
            score = silhouette_score(embeddings, labels)
            silhouette_scores.append(score)

        if silhouette_scores:
            optimal_num_speakers = K[np.argmax(silhouette_scores)]
        else:
            optimal_num_speakers = 1  # Default value or handle empty scores

        kmeans = KMeans(n_clusters=optimal_num_speakers)
        labels = kmeans.fit_predict(embeddings)

        for i in range(len(segments)):
            segments[i]["speaker"] = 'SPEAKER ' + str(labels[i] + 1)

        def time(secs):
            return datetime.timedelta(seconds=round(secs))

        return_arr = []
        temp_str = ''
        for (i, segment) in enumerate(segments):
            temp_dict = {}
            
            if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
                print("\n" + segment["speaker"] + ' ' + str(time(segment["start"])) + '\n')
                temp_str = segment["speaker"]
            print(segment["text"][1:] + ' ')
            temp_dict['speaker'] = temp_str
            temp_dict['line'] = segment["text"][1:] 
            return_arr.append(temp_dict)
        print(return_arr)
        return return_arr
