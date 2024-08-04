
from tensorflow import keras as krs
from logging import Logger
import string
from tensorflow.keras.models import load_model
import json
from tensorflow.keras.preprocessing.text import tokenizer_from_json

class TalkPole:
    _model=None;
    _tokenizer = None;
    _logger = None;
    _instance=None;
    def __new__(cls,logger:Logger):
        if not cls._instance:
            logger.info('Creating TalkPole Instance...')
            cls._instance = super(TalkPole, cls).__new__(cls)
        return cls._instance
    def __init__(self,logger:Logger):
        if not hasattr(self,'initialized'):
            logger.info('TalkPole Initialization...')
            self.initialized = True
            self._logger = logger
            self._model = load_model('./ai-models/cnn_bilstm_model.keras')
            self._logger.info('Talkpole Loaded Successfully.')
            with open('./ai-models/tokenizer_lstm.json', 'r', encoding='utf-8') as f:
                json_tok = json.load(f)
            self._tokenizer = tokenizer_from_json(json_tok)
            self._logger.info('Tokenizer Loaded Successfully.')
    def __del__(self):
        self._logger.info('TalkPole Deleted.')
        self.initialized = False
        self._model = None
        self._instance=None
        self._tokenizer=None 
    @staticmethod
    def preprocess_text(text):
        lower = text.lower()
        punctuation = string.punctuation.replace("'", "")
        translate_table = str.maketrans(punctuation, ' ' * len(punctuation))
        cleaned=lower.translate(translate_table)
        cleaned = cleaned.strip()
        cleaned = ' '.join(cleaned.split())
        return cleaned
    
    def text_prepare(self,text):
        sequences = self._tokenizer.texts_to_sequences([text])
        padded = krs.preprocessing.sequence.pad_sequences(sequences,maxlen=500)
        return padded
        
    def predict(self,value):
        if(value is None):
            return None,None,None
        if(value == ''):
            return None,None,None

        cleaned = self.preprocess_text(value)
        padded = self.text_prepare(cleaned)
        result = self._model.predict(padded)
        return result