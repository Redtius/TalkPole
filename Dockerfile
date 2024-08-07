FROM tensorflow/tensorflow:latest
EXPOSE 5000

WORKDIR /talkpole

COPY requirements.txt requirements.txt
RUN pip install --ignore-installed -r requirements.txt

COPY . .

ENV FLASK_APP=main.py
ENV TF_ENABLE_ONEDNN_OPTS=0
ENV TF_CPP_MIN_LOG_LEVEL=1

CMD [ "gunicorn", "-w","1","-b","0.0.0.0:5000" , "main:app"]
