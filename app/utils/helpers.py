from tensorflow.keras.preprocessing.sequence import pad_sequences
import string
from io import BytesIO
import fastavro
import yaml
import json


def tokenize(tokenizer,text):
  sequences = tokenizer.texts_to_sequences([text])
  padded = pad_sequences(sequences,maxlen=500)
  return padded

def clean_text(text):
  lower = text.lower()
  punctuation = string.punctuation.replace("'", "")
  translate_table = str.maketrans(punctuation, ' ' * len(punctuation))
        
  cleaned=lower.translate(translate_table)
  cleaned = cleaned.strip()
  cleaned = ' '.join(cleaned.split())
  return cleaned

def load_config_from_yaml(file_path, config_name):
    with open(file_path, 'r') as file:
        config_data = yaml.safe_load(file)
        return config_data.get(config_name, {})
      
def serializer(message):
    return json.dumps(message).encode('utf-8')

def deserializer(message):
    return json.loads(message.decode('utf-8'))
  
def avro_deserializer(message,schema):
    buffer = BytesIO(message)
    reader = fastavro.reader(buffer, schema)
    return next(reader)
  
def avro_serializer(message,schema):
    buffer = BytesIO()
    fastavro.writer(buffer, schema, [message])
    return buffer.getvalue()

def load_schema(file_path):
    with open(file_path, 'r') as file:
        schema = json.load(file)
    return schema