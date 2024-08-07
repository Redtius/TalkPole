from . import TalkpoleModel
from logging import Logger


class TalkpoleCNN(TalkpoleModel):
  
  def __new__(cls,*args, **kwargs):
    if not cls.instance:
      cls.instance = super(TalkpoleCNN, cls).__new__(cls)
    return cls.instance

  def __init__(self,logger:Logger,modelPath,tokenizerPath):
    if not hasattr(self,'initialized'):
      self.initialized = True
      super().__init__(logger,'CNN',modelPath,tokenizerPath)
  
  
    