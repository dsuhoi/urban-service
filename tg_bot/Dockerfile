FROM python:3.12-slim

WORKDIR /tg_bot

RUN apt-get update -y && apt-get install sqlite3 -y

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "main.py"]
