from flask import Flask,jsonify,request
from flask_restful import Api
from utils.talkpole import TalkPole
from utils.kafka import create_consumer_producer

app = Flask(__name__)
api = Api(app)

talkpole = TalkPole()

consumer,producer  = create_consumer_producer(talkpole)

# add more than 500 characters messages
# add kafka
# get it ready for production
# get more precision (up to 90% | current is 80% and it's struggling)

@app.route('/talkpole')
def get_result():
    data = request.get_json();
    print(data['text'])
    result_arr = talkpole.predict(data['text']);
    result = result_arr.tolist();
    return jsonify({'result':result[0]})

if __name__ == '__main__':
    app.run()
    
    