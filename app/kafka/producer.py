from .config import KafkaConfig
from kafka import KafkaProducer

class KafkaProducerClient():
  def __init__(self,logger,config:KafkaConfig):
    self._logger = logger
    self._config = config
    self._producer= KafkaProducer(bootstrap_servers=f'{self.config._host}:{self.config._port}'
                                  ,value_serializer=self._config._output_schema)
    self.logger.info('Producer Created...')
  
  def produce(self,sentiment):
    self._producer.send(self._config._output_topic,value=sentiment,key=b'sentiment')
    