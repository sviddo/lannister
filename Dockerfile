FROM python:3

WORKDIR /app

COPY . .
RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt

ARG SLACK_SIGNING_SECRET
ARG SLACK_BOT_TOKEN
ENV SLACK_SIGNING_SECRET ${SLACK_SIGNING_SECRET}  
ENV SLACK_BOT_TOKEN ${SLACK_BOT_TOKEN}  

RUN python manage.py makemigrations
RUN python manage.py migrate

CMD python manage.py runserver 0.0.0.0:80
