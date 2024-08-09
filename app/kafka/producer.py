from .config import KafkaConfig
from kafka import KafkaProducer
from app.utils.helpers import avro_serializer

class KafkaProducerClient():
  def __init__(self,logger,config:KafkaConfig):
    self._logger = logger
    self._config = config
    self._producer= KafkaProducer(bootstrap_servers=f'{self._config.host}:{self._config.port}'
                                  ,value_serializer= lambda m: avro_serializer(m,self._config.output_schema))
    self._logger.info('Producer Created...')
  
  def produce(self,sentiment):
    self._producer.send(self._config.output_topic,value=sentiment,key=b'sentiment')
    