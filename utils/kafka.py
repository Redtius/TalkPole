from utils.talkpole import TalkPole
import json
import threading
import os
import logging
from logging import Logger
from kafka import KafkaConsumer
from kafka import KafkaProducer


class KafkaClient:
  def __init__(self, talkpole:TalkPole,logger:Logger):
    self.kafka_port = os.environ['KAFKA_PORT'] if 'KAFKA_PORT' in os.environ else '9092'
    self.kafka_host = os.environ['KAFKA_HOST'] if 'KAFKA_HOST' in os.environ else 'localhost'
    self.kafka_con = f'{self.kafka_host}:{self.kafka_port}'
    self.logger = logger
    self.consumer, self.producer = self.create_consumer_producer(talkpole)
    
  def get_consumer(self):
    return self.consumer
  
  def get_producer(self):
    return self.producer

  def serializer(message):
      return json.dumps(message).encode('utf-8')

  def deserializer(message):
      return json.loads(message.decode('utf-8'))

  def create_producer(self):
    producer= KafkaProducer(bootstrap_servers=self.kafka_con,value_serializer=self.serializer)
    self.logger.info('Producer Created...')
    return producer

  def create_consumer_producer(self,talkpole:TalkPole):
    consumer = KafkaConsumer('talkpole_in',bootstrap_servers=self.kafka_con,
                            auto_offset_reset='earliest',
                            group_id='talkpole-group', 
                            enable_auto_commit=True,
                            value_deserializer=self.deserializer)
    self.logger.info('Consumer Created...')
    producer = self.create_producer();
    def consume():
      try:
        while True:
          msg = consumer.poll(timeout_ms=1.0)
          if msg:
            for messages in msg.items():
              for message in messages[1]:
                pred = talkpole.predict(message.value['text'])
                self.produce(producer,float(pred[0][0]))
      finally:
        consumer.close()
    consumer_thread = threading.Thread(target=consume)
    consumer_thread.start()
    self.logger.info('Consumer Thread Started...')
    return consumer,producer

  def produce(producer: KafkaProducer,msg):
    producer.send('talkpole_out',value=msg,key=b'result')
  
