from utils.talkpole import TalkPole
import json
import threading
import os

from kafka import KafkaConsumer
from kafka import KafkaProducer

kafka_port = os.environ['KAFKA_PORT']
kafka_host = os.environ['KAFKA_HOST']

kafka_con = f'{kafka_host}:{kafka_port}'

def serializer(message):
    return json.dumps(message).encode('utf-8')

def deserializer(message):
    return json.loads(message.decode('utf-8'))

def create_producer():
  producer= KafkaProducer(bootstrap_servers=kafka_con,value_serializer=serializer)
  print('Producer created')
  return producer

def create_consumer_producer(talkpole:TalkPole):
  consumer = KafkaConsumer('talkpole_in',bootstrap_servers=kafka_con,
                           auto_offset_reset='earliest',
                           value_deserializer=deserializer)
  print('created consumer')
  producer = create_producer();
  def consume():
    try:
      while True:
        msg = consumer.poll(timeout_ms=1.0)
        if msg:
          for messages in msg.items():
            for message in messages[1]:
              pred = talkpole.predict(message.value['text'])
              produce(producer,float(pred[0][0]))
    finally:
      consumer.close()
  consumer_thread = threading.Thread(target=consume)
  consumer_thread.start()
  print('consumer thread started')
  return consumer,producer

def produce(producer: KafkaProducer,msg):
  producer.send('talkpole_out',value=msg,key=b'result')
  
