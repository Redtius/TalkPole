FROM tensorflow/tensorflow:latest
EXPOSE 5000

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --ignore-installed -r requirements.txt

COPY . ./app

CMD [ "python3", "-m" , "main.py", "--host=0.0.0.0"]