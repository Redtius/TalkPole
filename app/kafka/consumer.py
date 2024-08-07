from kafka import KafkaConsumer
from app.utils.helpers import avro_deserializer
from .config import KafkaConfig

class KafkaConsumerClient():
  
  def __init__(self, logger, config:KafkaConfig):
    self._logger = logger
    self._config = config
    
    self._consumer = KafkaConsumer('talkpole_in',bootstrap_servers=f'{self._config._host}:{self._config._port}',
                            auto_offset_reset='earliest',
                            group_id=self._config._group_id, 
                            enable_auto_commit=True,
                            value_deserializer=lambda m: avro_deserializer(m, self._config._input_schema))
    self._logger.info('Kafka consumer initialized')
  
  def consume(self):
    try:
        self._logger.info('Starting Kafka consumer...')
        while True:
            msg = self._consumer.poll(timeout_ms=0.1)
            if msg:
                for topic_partition, messages in msg.items():
                    for message in messages:
                        yield message.value
    finally:
        self._logger.info('Closing Kafka consumer...')
        self._consumer.close()

    
