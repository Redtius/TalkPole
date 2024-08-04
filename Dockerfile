FROM tensoflow/tensorflow:latest
EXPOSE 5000

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=main.py

CMD [ "gunicorn", "-w","1","-b","0.0.0.0:5000" , "main:app"]
