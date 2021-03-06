FROM python:3.8.5
RUN apt-get update && apt-get install -y openssh-server
WORKDIR /code
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . .
CMD gunicorn foodgram_project.wsgi:application --bind 0.0.0.0:8000