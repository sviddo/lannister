from django.views.decorators.csrf import csrf_exempt
from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler
import requests, json, os

app = App(
    #get tokens in the app, do not push to github!!!
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

handler = SlackRequestHandler(app=app)

@csrf_exempt
def events(request):
    return handler.handle(request)

@csrf_exempt
def events(request):
    return handler.handle(request)


@app.event('app_home_opened')
def update_home_tab(client, event, logger):
    try:
        client.views_publish(
        user_id=event["user"],
        view={
            "type": "home",
            "callback_id": "home_view",

            "blocks": [
            {
                "type": "section",
                "text": {
                "type": "mrkdwn",
                "text": "*Welcome to the _Lannister Assistant_* :tada:"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                "type": "mrkdwn",
                "text": f"<@{event['user']}>, would you like to change someone's role or should I show you all the requests"
                }
            },
            {
                "type": "actions",
                "elements": [
                {
                    "type": "button",
                    "text": {
                    "type": "plain_text",
                    "text": "Changhe role"
                    },
                    "action_id": "change_role"
                },
                {
                    "type": "button",
                    "text": {
                    "type": "plain_text",
                    "text": "Show Requests"
                    }
                }
                ]
            }
            ]
        }
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")

@app.action("change_role")
def change_role(ack, body, client):
    users_data = requests.get('http://127.0.0.1:8000/api/users/')
    users = json.loads(users_data.text)

    print(users)

    data = []

    for user in users:
        data.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<@{user['service_id']}>"
            }
        }
        )

    ack()
    client.views_open(
        trigger_id=body['trigger_id'],
        view={
             "type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "Users"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": data
        }
    )
