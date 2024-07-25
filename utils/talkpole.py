
import keras as krs
from logging import Logger
import json
from keras._tf_keras.keras.preprocessing.text import tokenizer_from_json

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
            self._model = krs.models.load_model('./ai-models/cnn_bilstm.keras')
            self._logger.info('Talkpole Loaded Successfully.')
            with open('./ai-models/tokenizer.json', 'r', encoding='utf-8') as f:
                json_tok = json.load(f)
            self._tokenizer = tokenizer_from_json(json_tok)
            self._logger.info('Tokenizer Loaded Successfully.')
    def __del__(self):
        self._logger.info('TalkPole Deleted.')
        self.initialized = False
        self._model = None
        self._instance=None
        self._tokenizer=None 
    def predict(self,value):
        sequences = self._tokenizer.texts_to_sequences([value])
        padded = krs.preprocessing.sequence.pad_sequences(sequences,maxlen=500)
        result = self._model.predict(padded)
        return result