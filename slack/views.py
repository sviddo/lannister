from django import views
from django.views.decorators.csrf import csrf_exempt
from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler
from .middlewares import get_all_users_but_self, create_blocks, publish_admin_view
import os, requests, json

app = App(
    #get tokens in the app, do not push to github!!!
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

handler = SlackRequestHandler(app=app)

def check_user_role(user_id):
    users_data = requests.get('http://127.0.0.1:8000/api/users')
    users = json.loads(users_data.text)
    user_in_db = list(filter(lambda user: user["service_id"] == user_id, users))[0]
    return user_in_db['roles']

@csrf_exempt
def events(request):
    return handler.handle(request)

@app.event('app_home_opened')
def update_home_tab(client, event, logger):
    user_id=event["user"]
    try:
        client.views_publish(user_id=user_id, view = publish_admin_view(user_id))
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")



@app.action("change_role", middleware=[get_all_users_but_self, create_blocks])
def handle_some_action(ack, context, client, body):
    ack()
    # if no users print that there's no users to show
    # users = context["users"]
    blocks = context["blocks"]
    client.views_open(
        trigger_id=body['trigger_id'],
        view={
             "type": "modal",
            # View identifier
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text": "Users"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": blocks
        }
    )


@app.action("user_role_has_been_changed")
def aknowladge(ack, body, context):
    ack()  
    user_id = body['actions'][0]['block_id']
    user_role = body['actions'][0]['selected_option']['value']
    users_data = requests.get('http://127.0.0.1:8000/api/users')
    users = json.loads(users_data.text)
    user_in_db = list(filter(lambda user: user["service_id"] == user_id, users))[0]

    uri = f"http://127.0.0.1:8000/api/reviewer_role/{user_id}"
    if user_role == "r" and user_role not in user_in_db["roles"]:
        requests.patch(uri)
    elif user_role == "cw" and "r" in user_in_db["roles"]:
        requests.delete(uri)

@app.view("view_1")
def handle_view1_submission(ack, body, client):
    ack()
    client.chat_postMessage(channel=body['user']['id'], text="Just wanted to inform you that all the changes has been made and user roles have been updated successfully")

