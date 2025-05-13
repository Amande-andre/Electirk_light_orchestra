FROM python:3.11-slim

RUN apt update && apt install -y gcc

WORKDIR /app

COPY Dockerfiles/compiler/app.py .

RUN pip install fastapi uvicorn python-multipart

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5042"]
