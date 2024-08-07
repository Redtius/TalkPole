from flask import current_app
from app.utils.helpers import load_schema

class KafkaConfig:
  def __init__(self):
    self._port = current_app.config['kafka']['port']
    self._host = current_app.config['kafka']['host']
    self._model = current_app.config['kafka']['model']
    self._input_topic = current_app.config['kafka']['input-topic']
    self._output_topic = current_app.config['kafka']['output-topic']
    self._group_id = current_app.config['kafka']['group-id']
    self._input_schema = load_schema(current_app.config['kafka']['input-schema'])
    self._output_schema = load_schema(current_app.config['kafka']['output-schema'])
    
  @property
  def port(self):
    return self._port
  
  @property
  def host(self):
    return self._host
  
  @property
  def model(self):
    return self._model
  
  @property
  def input_topic(self):
    return self._input_topic
  
  @property
  def output_topic(self):
    return self._output_topic
  
  @property
  def group_id(self):
    return self._group_id
