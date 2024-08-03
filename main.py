from flask import Flask,jsonify,render_template,request
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
    model = request.args.get('model') if request.args.get('model') else 'cbi'
    data = request.get_json();
    if model == 'lstm':
        result_arr = talkpole.pred_lstm(data['content']);
    elif model == 'cnn':
        result_arr = talkpole.pred_cnn(data['content']);
    else:
        result_arr = talkpole.pred_cbi(data['content']);
    
    result = result_arr.tolist();
    return jsonify({'result':result[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    