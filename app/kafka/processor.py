from .config import KafkaConfig
from .consumer import KafkaConsumerClient
from .producer import KafkaProducerClient
import threading
from logging import Logger
from flask import current_app

class KafkaProcessor:
  
    def __init__(self, logger:Logger,app):
        self._app = app
        self._logger = logger
        self._config = KafkaConfig()
        self._consumer_client = KafkaConsumerClient(self._logger, self._config)
        self._producer_client = KafkaProducerClient(self._logger, self._config)
        self._thread = None
        self._stop_event = threading.Event()
        self._logger.info('KafkaProcessor initialized')
    
    def __del__(self):
        try:
            if hasattr(self, '_thread') and self._thread is not None:
                self.stop_thread()
        except Exception as e:
            self._logger.error(f'Error during cleanup: {e}')
    
    def process(self)->None:
        try:
            self._logger.info('Starting Kafka consumer thread...')
            with self._app.app_context():
                while not self._stop_event.is_set():
                    for message in self._consumer_client.consume():
                        if self._stop_event.is_set():
                            break
                        pred = self._app.config[self._config.model].predict(message['content'])
                        self._producer_client.produce({
                            'message': message,
                            'sentiment': float(pred[0][0])
                        })
        except Exception as e:
            self._logger.error(f'Error during Kafka processing: {e}')
        finally:
            self._logger.info('Stopping Kafka consumer thread...')
            if self._thread is not None:
                self.stop_thread()
    
    def start_thread(self)->None:
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self.process)
            self._thread.start()
            self._logger.info('Kafka consumer thread started...')
        
    def stop_thread(self)->None:
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join()
            self._logger.info('Kafka processor thread stopped')
