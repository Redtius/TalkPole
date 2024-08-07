from kafka import KafkaConsumer
from app.utils.helpers import avro_deserializer
from .config import KafkaConfig

class KafkaConsumerClient():
  
  def __init__(self, logger, config:KafkaConfig):
    self._logger = logger
    self._config = config
    
    self._consumer = KafkaConsumer(self.config.input_topic,bootstrap_servers=f'{self.config._host}:{self.config._port}',
                            auto_offset_reset='earliest',
                            group_id=self.config._group_id, 
                            enable_auto_commit=True,
                            value_deserializer=lambda m: avro_deserializer(m, self._config._input_schema))
    self._logger.info('Kafka consumer initialized')
  
  def consume(self):
    try:
        self._logger.info('Starting Kafka consumer...')
        while True:
          msg = self.consumer.poll(timeout_ms=1.0)
          if msg:
            for messages in msg.items():
              for message in messages[1]:
                yield message
    finally:
      self._logger.info('Closing Kafka consumer...')
      self.consumer.close()
    
