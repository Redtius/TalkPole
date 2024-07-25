FROM tensorflow/tensorflow:2.15.0
EXPOSE 5000

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --ignore-installed -r requirements.txt

COPY . .

ENV FLASK_APP=main.py

CMD [ "gunicorn", "-w","4","-b","0.0.0.0:5000" , "main:app"]