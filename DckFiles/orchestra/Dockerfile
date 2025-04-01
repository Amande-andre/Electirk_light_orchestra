FROM python:3.9-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install rich
RUN pip install docker flask flask-cors gunicorn


CMD ["gunicorn", "--bind", "0.0.0.0:5042", "main:app"]