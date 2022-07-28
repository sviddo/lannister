FROM python:3.9.13-alpine3.15
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERD=1
WORKDIR /lannister
COPY . .

RUN pip install -r requirements.txt
