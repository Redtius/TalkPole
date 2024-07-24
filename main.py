from flask import Flask,jsonify
from flask_restful import Api
from utils.talkpole import TalkPole
from utils.kafka import KafkaClient

app = Flask(__name__)
api = Api(app)

talkpole = TalkPole(app.logger)

kafkaClient = KafkaClient(talkpole,app.logger) 

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    