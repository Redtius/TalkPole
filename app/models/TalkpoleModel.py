from tensorflow import keras as krs
from tensorflow.keras.models import load_model
from logging import Logger
import json
from keras._tf_keras.keras.preprocessing.text import tokenizer_from_json
from app.utils.helpers import tokenize,clean_text
from abc import ABC


class TalkpoleModel(ABC):
  
  model=None;
  model_name=None;
  model_path=None;
  tokenizer = None;
  tokenizer_path=None;
  logger = None;
  instance=None;

  def __init__(self,logger:Logger,modelName,modelPath,tokenizerPath):
      self.model_name = modelName
      self.model_path = modelPath
      self.tokenizer_path = tokenizerPath
      self.logger = logger
      self.logger.info(self.model_name+' Initialization...')
      self.model = load_model(self.model_path)
      self.model.compile(optimizer='adam')
      self.logger.info(self.model_name+' Loaded Successfully.')
      with open(self.tokenizer_path, 'r', encoding='utf-8') as f:
        json_tok2 = json.load(f)
      self.tokenizer = tokenizer_from_json(json_tok2)
      self.logger.info(self.model_name+' Tokenizer Loaded Successfully.')

  def __del__(self):
    self.model=None;
    self.model_name=None;
    self.model_path=None;
    self.tokenizer = None;
    self.tokenizer_path=None;
    self.logger = None;
    self.instance=None;
    #self.logger.info('TalkPole Deleted.')
  

  def predict(self,value):
    if(value is None):
      return None,None,None
    if(value == ''):
      return None,None,None
    cleaned = clean_text(value)
    padded = tokenize(self.tokenizer,cleaned)
    result = self.model.predict(padded)
    return result