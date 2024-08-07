from tensorflow.keras.preprocessing.sequence import pad_sequences
import string
import yaml


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