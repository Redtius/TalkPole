
from tensorflow import keras as krs
from tensorflow.keras.models import load_model
from logging import Logger
import json
import string
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
            self._model = load_model('./ai-models/cnn_model.h5')
            self._model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            self._model_lstm = load_model('./ai-models/lstm_model.keras')
            self._model_lstm.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            self._model_cbi = load_model('./ai-models/cnn_bilstm_model.keras')
            self._model_cbi.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
            self._logger.info('Talkpole Loaded Successfully.')
            with open('./ai-models/tokenizer.json', 'r', encoding='utf-8') as f:
                json_tok = json.load(f)
            self._tokenizer = tokenizer_from_json(json_tok)
            with open('./ai-models/tokenizer_lstm.json', 'r', encoding='utf-8') as f:
                json_tok2 = json.load(f)
            self._tokenizer2 = tokenizer_from_json(json_tok2)
            self._logger.info('Tokenizer Loaded Successfully.')
    def __del__(self):
        self._logger.info('TalkPole Deleted.')
        self.initialized = False
        self._model = None
        self._instance=None
        self._tokenizer=None 
    def pred_lstm(self,value):
        lower = value.lower()
        punctuation = string.punctuation.replace("'", "")
        translate_table = str.maketrans(punctuation, ' ' * len(punctuation))
        
        cleaned=lower.translate(translate_table)
        sequences2 = self._tokenizer2.texts_to_sequences([cleaned])
        padded2 = krs.preprocessing.sequence.pad_sequences(sequences2,maxlen=500)
        result2 = self._model_lstm.predict(padded2)
        return result2
    def pred_cbi(self,value):
        lower = value.lower()
        punctuation = string.punctuation.replace("'", "")
        translate_table = str.maketrans(punctuation, ' ' * len(punctuation))
        
        cleaned=lower.translate(translate_table)
        sequences2 = self._tokenizer2.texts_to_sequences([cleaned])
        padded2 = krs.preprocessing.sequence.pad_sequences(sequences2,maxlen=500)
        result3 = self._model_cbi.predict(padded2)
        return result3
    def pred_cnn(self,value):
        sequences = self._tokenizer.texts_to_sequences([value])
        padded = krs.preprocessing.sequence.pad_sequences(sequences,maxlen=500)
        result = self._model.predict(padded)
        return result