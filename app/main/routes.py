from flask import jsonify,render_template,request,Blueprint,current_app


main = Blueprint('main', __name__)

@main.route('/health')
def health():
    return jsonify({'status':'ok'})

@main.route('/',methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        data = request.form['textInput']
        result_cnn = current_app.config['CNN'].predict(data)
        result_lstm = current_app.config['LSTM'].predict(data)
        result_cbi = current_app.config['CBI'].predict(data)
        return render_template('index.html',prediction_cnn=result_cnn[0][0],prediction_lstm=result_lstm[0][0],prediction_cbi=result_cbi[0][0])
    return render_template('index.html',prediction_cnn=None,prediction_lstm=None,prediction_cbi=None)

@main.route('/docs',methods = ['GET'] )
def docs():
    return render_template('docs.html')