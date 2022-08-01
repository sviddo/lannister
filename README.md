# Lannister

Project integrating with Slack platform, but can be ported to any other one. Imagine the company with 3 type of workers: workers, reviewers and admins. The main goal is to make process of handling bonuses the most possibly easy: for workers to create them, for reviewers to reject or approve ones and for admins - do all admin-required work such as watch for process, view requests, change roles etc.

To run the application you need to create Slack App (follow [https://api.slack.com/apps](https://api.slack.com/apps)) and receive [Signing secret](https://api.slack.com/apps) and [Bot token](https://api.slack.com/authentication/token-types#bot), then follow next steps:
```
git clone https://github.com/sviddo/lannister.git
cd lannister
docker build -t django-app --build-arg SLACK_SIGNING_SECRET='your Slack signing secret' --build-arg SLACK_BOT_TOKEN='your Slack bot token' .
docker run -p 8000:80 django-app
```

# Architecture

Application consists of 3 independent parts:
- Api (defines api to work with application)
- Lannister (all settings and linking stuff to combine all 3 parts of application together)
- Slack (integration with Slack platform using Slack Bot, this part is optional and can be replaced)

<h3>Tech stack:</h3>

- Back-end: **Django, Django Rest Framework, SQLite3, requests**
- Front-end: **Slack Bot UI (optional)**
- DevOps: **Docker, AWS, GCP**
- Testing: **pytest**
