import os
from slack_bolt import App

app = App(
    #get tokens in the app, do not push to github!!!
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)