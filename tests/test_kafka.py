import pytest
from unittest.mock import Mock
from app.kafka.processor import KafkaProcessor


@pytest.fixture()
def processor():
  app = Mock()
  logger = Mock()
  return KafkaProcessor(logger,app)

# Test if the processor is initialized correctly

# Test if the processor is deleted correctly

# Test if processing works

# Test if the thread starts correctly

# Test if the thread stops correctly