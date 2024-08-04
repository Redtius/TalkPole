import pytest
import logging
from utils.talkpole import TalkPole

@pytest.fixture
def logger():
  return logging.getLogger('tests_logger')

@pytest.fixture
def model(logger):
  return TalkPole(logger)

# Test Singleton Pattern
def test_singleton(model,logger):
  """Checking if the singleton pattern is working..."""
  model2 = TalkPole(logger)
  assert model is model2

def test_models_loading(model):
  """Checking if models are loaded..."""
  assert model._model is not None

def test_tokenizer_loading(model):
  """Checking If tokenizers are loaded..."""
  assert model._tokenizer is not None

def test_text_preprocessing(model):
  """Checking If text is cleaned correctly..."""
  result = model.preprocess_text("J'ai Rien à dire !?")
  assert result == "j'ai rien à dire"

# check the prediction of the model
def test_model_padding(model):
  """Checking If tokenizer generate the right sequences..."""
  cleaned = model.preprocess_text("J'ai Rien à dire !?")
  padded2 = model.text_prepare(cleaned)
  assert padded2.shape == (1, 500)


def test_prediction(model):
  """Checking If models give predictions..."""
  result = model.predict("J'ai Rien à dire !?")
  assert result is not None


def test_edge_cases(model):
    """Testing empty and long input..."""
    assert model.predict("") == (None, None, None)

    long_text = " ".join(["word"] * 1000)
    result = model.predict(long_text)
    assert result is not None

