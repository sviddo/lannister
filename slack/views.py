from django.views.decorators.csrf import csrf_exempt
from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler
import os

app = App(
    #get tokens in the app, do not push to github!!!
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

handler = SlackRequestHandler(app=app)

@csrf_exempt
def events(request):
    return handler.handle(request)
    