from kafka import KafkaProducer
import fastavro
from io import BytesIO
import json

def load_schema(file_path):
    with open(file_path, 'r') as file:
        schema = json.load(file)
    return schema

def avro_serializer(message,schema):
    print(message)
    buffer = BytesIO()
    fastavro.writer(buffer, schema, [message])
    print(buffer.getvalue())
    return buffer.getvalue()

schema = load_schema('input.avsc')
print(schema)
producer = KafkaProducer(
    bootstrap_servers='localhost:9095',
    value_serializer=lambda v: avro_serializer(v, schema)
)
print("producer built")

test_message = {
    "requestId":"dgygdeyge",
    "ref":"rzfeftd",
   	"chatTicket":"sjdhuehd",
    "senderId":"dggdhshye",
    "content":"j'aime pas ça du tout",
    "timestamp":1234567
}
producer.send('talkpole_in', test_message)
print("message sent")
producer.flush()
print("producer flushed")
