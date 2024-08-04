from flask import Flask,jsonify,render_template,request
from utils.talkpole import TalkPole

app = Flask(__name__,static_url_path='/templates/static')

talkpole = TalkPole(app.logger)

@app.route('/health')
def health():
    return jsonify({'status':'ok'})

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        data = request.form['textInput']
        result_cnn,result_lstm,result_cbi = talkpole.predict(data)
        return render_template('index.html',prediction_cnn=result_cnn[0][0],prediction_lstm=result_lstm[0][0],prediction_cbi=result_cbi[0][0])
    return render_template('index.html',prediction_cnn=None,prediction_lstm=None,prediction_cbi=None)

@app.route('/docs',methods = ['GET'] )
def docs():
    return render_template('docs.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    