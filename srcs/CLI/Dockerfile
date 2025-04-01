FROM python:3.9-slim

WORKDIR /app
COPY srcs/CLI/ /app
COPY requirements.txt .
RUN pip install rich
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]