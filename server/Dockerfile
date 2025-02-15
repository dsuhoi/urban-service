FROM python:3.12-slim

WORKDIR /server

RUN apt-get update -y

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["./wait-for-it.sh", "chromadb:8000", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
# COPY entrypoint.sh .
# RUN sed -i 's/\r$//g' entrypoint.sh
# RUN chmod +x entrypoint.sh
