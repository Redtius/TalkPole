from flask import Flask
from app.models import TalkpoleCNN,TalkpoleCBI,TalkpoleLSTM
from app.main.routes import main
from app.utils.helpers import load_config_from_yaml
import logging



def create_app(config_name="default"):
    app = Flask(__name__,static_folder='app/main/static',template_folder='app/main/templates')
    
    config = load_config_from_yaml('app/config/config.yaml',config_name)
    app.config.update(config)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('appLogger')
    cnn = TalkpoleCNN(logger,app.config['models-path']['cnn'],app.config['tokenizers-path']['cnn'])
    lstm = TalkpoleLSTM(logger,app.config['models-path']['lstm'],app.config['tokenizers-path']['lstm'])
    cbi = TalkpoleCBI(logger,app.config['models-path']['cbi'],app.config['tokenizers-path']['cbi'])
    with app.app_context():
        app.config['CNN'] = cnn
        app.config['LSTM'] = lstm
        app.config['CBI'] = cbi
    # Initialize Kafka producer
    # Initialize Kafka consumer
    # Use them in a different class
    
    
    app.register_blueprint(main)
    return app

app = Flask(__name__)


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)
    
    