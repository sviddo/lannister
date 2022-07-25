FROM python:3

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ARG SLACK_SIGNING_SECRET
ARG SLACK_BOT_TOKEN
ENV SLACK_SIGNING_SECRET ${SLACK_SIGNING_SECRET}  
ENV SLACK_BOT_TOKEN ${SLACK_BOT_TOKEN}  

RUN python manage.py migrate

CMD ["gunicorn", "lannister.wsgi:application"]
