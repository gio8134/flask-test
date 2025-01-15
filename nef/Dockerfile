FROM python:3.12.3-slim AS builder
ENV PYTHONUNBUFFERED=1

WORKDIR /

COPY requirements.txt requirements.txt
COPY main.py main.py
COPY gnode_db.json gnode_db.json

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 9001

CMD ["python3", "main.py"]