import whisper
# """ import datetime
# import subprocess
# import torch
# import pyannote.audio """
#from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.audio import Audio
#from pyannote.core import Segment
import wave
import contextlib
# """ from sklearn.cluster import AgglomerativeClustering
# import numpy as np """
import pickle

class SpeakerDiarization:
    MODEL_CACHE_FILE = 'model_cache.pkl'

    def __init__(self, file_name):
        self.file_name = file_name
        self.model = self.load_model()

    def load_model(self):
        try:
            print("Found the file")
            with open(SpeakerDiarization.MODEL_CACHE_FILE, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print("Loading the file")
            model = whisper.load_model('medium')
            self.freeze_model(model)
            with open(SpeakerDiarization.MODEL_CACHE_FILE, 'wb') as f:
                pickle.dump(model, f)
            return model

    def freeze_model(self, model):
        # Set the model to evaluation mode
        model.eval()

        # Freeze the model parameters
        for param in model.parameters():
            param.requires_grad = False

    def get_text(self):
        result = self.model.transcribe(self.file_name)
        segments = result["segments"]

        with contextlib.closing(wave.open(self.file_name,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)

        audio = Audio()

        temp_segments = segments
        for i, segment in enumerate(temp_segments):
            print('Speaker1:', segment['text'])
