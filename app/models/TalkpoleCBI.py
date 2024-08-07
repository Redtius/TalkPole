from . import TalkpoleModel
from logging import Logger


class TalkpoleCBI(TalkpoleModel):
  
  def __new__(cls,*args, **kwargs):
    if not cls.instance:
      cls.instance = super(TalkpoleCBI, cls).__new__(cls)
    return cls.instance

  def __init__(self,logger:Logger,modelPath,tokenizerPath):
    if not hasattr(self,'initialized'):
      self.initialized = True
      super().__init__(logger,'CNN-BiLSTM',modelPath,tokenizerPath)
  
  
    