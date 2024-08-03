from flask import Flask,jsonify,request
from flask_restful import Api
from utils.talkpole import TalkPole

app = Flask(__name__,static_url_path='/templates/static')
api = Api(app)

talkpole = TalkPole(app.logger)

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

@app.route('/predict', methods=['GET'])
def get_result():
    data = request.get_json();
    result_arr = talkpole.predict(data['content']);
    result = result_arr.tolist();
    return jsonify({'result':result[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    