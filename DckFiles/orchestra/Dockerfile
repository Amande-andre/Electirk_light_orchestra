FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir rich
RUN pip install docker


ENTRYPOINT ["python", "main.py"]