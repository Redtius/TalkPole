from flask import Flask
from app.models import TalkpoleCNN,TalkpoleCBI,TalkpoleLSTM
from app.main.routes import main
from app.utils.helpers import load_config_from_yaml
from app.kafka.processor import KafkaProcessor
import logging



def create_app(config_name="default"):
    app = Flask(__name__,static_folder='app/main/static',template_folder='app/main/templates')
    
    config = load_config_from_yaml('app/config/config.yaml',config_name)
    app.config.update(config)

    logger = logging.getLogger('TALKPOLE')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('app.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    with app.app_context():
        app.config['CNN'] = TalkpoleCNN(logger,app.config['models-path']['cnn'],app.config['tokenizers-path']['cnn'])
        app.config['LSTM'] = TalkpoleLSTM(logger,app.config['models-path']['lstm'],app.config['tokenizers-path']['lstm'])
        app.config['CBI'] = TalkpoleCBI(logger,app.config['models-path']['cbi'],app.config['tokenizers-path']['cbi'])
        kafka_processor = KafkaProcessor(logger,app)
        kafka_processor.start_thread()

    
    
    app.register_blueprint(main)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    