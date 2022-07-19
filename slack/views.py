from django.views.decorators.csrf import csrf_exempt
from slack_bolt import App
from slack_bolt.adapter.django import SlackRequestHandler

from .middlewares import admin_middlewares as am, worker_middlewares as wm
from .helpers import (
    admin_helpers as ah, 
    general_helpers as gh, 
    worker_helpers as wh, 
    reviewer_helpers as rh,
)
from .services import get_user_roles
import os, requests, json

app = App(
    #get tokens in the app, do not push to github!!!
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

handler = SlackRequestHandler(app=app)

@csrf_exempt
def events(request):
    return handler.handle(request)

@app.event('app_home_opened')
def update_home_tab(client, event, logger):
    user_id=event["user"] 
    view = gh.header()
    blocks = []

    # check the role of the user who opened the home tab
    # thereafter build blocks accordinly
    if 'r' in get_user_roles(user_id):
        blocks = wh.reviewer_home_blocks()
        view['blocks'].extend(blocks)
        reviewer_blocks = rh.reviewer_home_blocks()
        view['blocks'].extend(reviewer_blocks)

    if 'a' in get_user_roles(user_id):
        blocks = ah.admin_home_blocks()
        view['blocks'].extend(blocks)

        # temporary add reviewer functionality
        # to admin for testing purposes
        blocks = wh.reviewer_home_blocks()
        view['blocks'].extend(blocks)

    try:
        client.views_publish(user_id=user_id, view=view)
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.view("admin_view")
def handle_view1_submission(ack, body, client):
    ack()
    client.chat_postMessage(channel=body['user']['id'], text="Just wanted to inform you that all the changes has been made and user roles have been updated successfully")

@app.action("change_role_modal", middleware=[am.get_all_users_but_self, am.create_blocks])
def handle_some_action(ack, context, client, body):
    ack()

    # TODO: if no users print that there's no users to show

    blocks = context["blocks"]
    client.views_open(
        trigger_id=body['trigger_id'],
        view={
            "type": "modal",
            "callback_id": "admin_view",
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


@app.view("new_request_submission")
def create_new_request(ack, body, logger):
    ack()

    # get all the values the user has submitted
    submited_values = body['view']['state']['values']

    # assign the values to the variables
    # which we'll need to create a new request in db
    bonus_type = submited_values['bonus_type']['bonus']['value']
    request_description = submited_values['request_description']['bonus']['value']
    request_reviewer = submited_values['request_reviewer']['bonus']['selected_option']['value']

    # make an object with request info
    request = {
        "creator": body['user']['id'],
        "reviewer": request_reviewer,
        "bonus_type": bonus_type,
        "description": request_description,
        "status": "c"
    }

    # put request to db
    uri = "http://127.0.0.1:8000/api/create_request"
    r = requests.post(uri, json=request)

    # TODO: validate the response

    # TODO: if all good notify the user
    #       that all good and nofy the reviewer
    #       theat he has a new request assigned

@app.action("create_request_modal", middleware=[wm.get_reviewers, wm.create_reviewer_block, wm.create_make_request_view])
def create_request(ack, client, body, context):
    ack()
    blocks = context['blocks']
    
    client.views_open(
        trigger_id=body['trigger_id'],
        view={
            "type": "modal",
            "callback_id": "new_request_submission",
            "title": {"type": "plain_text", "text": "Create Request"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": blocks
        }
    )

@app.action("see_requests_modal", middleware=[wm.get_requests, wm.create_see_requests_blocks])
def show_requests(ack, client, body, context):
    """Show a new modal windows with a list
    
    Function creates a new modal with a list
    of all the user's requests.

    User can edit selected request
    """

    ack()
    blocks = context['blocks']
    client.views_open(
        trigger_id=body['trigger_id'],
        view={
            "type": "modal",
            "callback_id": "see_requests_modal_submission",
            "title": {"type": "plain_text", "text": "My requests"},
            "blocks": blocks
        }
    )

@app.action("edit_request", middleware=[wm.get_reviewers, wm.create_reviewer_block, wm.get_request_details, wm.create_edit_request_blocks])
def edit_request(ack, body, client, context):
    """Edit/Delete user's own request"""
    ack()
    blocks = context['blocks']
    request_id = context['request']['id']

    client.views_push(
        trigger_id=body['trigger_id'],
        view={
            "type": "modal",
            "callback_id": "edit_request_submission",
            "private_metadata": f"{request_id}",
            "title": {"type": "plain_text", "text": "Edit request"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": blocks
        }
    )

@app.view("edit_request_submission")
def update_request(ack, body, logger, context):
    ack()
    print(body['view']['state']['values'])

    # get all the values the user has submitted
    submited_values = body['view']['state']['values']
    

    # assign the values to the variables
    # which we'll need to create a new request in db
    bonus_type = submited_values['bonus_type']['bonus']['value']
    request_description = submited_values['request_description']['bonus']['value']
    request_reviewer = submited_values['request_reviewer']['bonus']['selected_option']['value']
    request_id = body['view']['private_metadata']

    # make an object with request info
    request = {
        "reviewer": request_reviewer,
        "bonus_type": bonus_type,
        "description": request_description,
    }

    # put request to db
    uri = f"http://127.0.0.1:8000/api/request/{request_id}"
    r = requests.patch(uri, json=request)

    # TODO: validate the response

    # TODO: if all good notify the user
    #       that all good and notify the reviewer
    #       that he has a new request assigned
    #       in case if the user changed the reviewer
    #       notify the old one as well (??)

@app.action("delete_request", middleware=[wm.get_requests, wm.get_request_details, wm.create_see_requests_blocks])
def handle_some_action(ack, body, context, client):
    ack()

    request_id = context['request']['id']
    blocks = [block for block in context['blocks'] if not (block['block_id'] == str(request_id) or block['block_id'] == f'{request_id}_name')]
    
    uri = f"http://127.0.0.1:8000/api/request/{request_id}"
    requests.delete(uri)

    # updating the view with deleted blocks being removed
    client.views_update(
        view_id=body["view"]["id"],
        view={
            "type": "modal",
            "callback_id": "see_requests_modal_submission",
            "title": {"type": "plain_text", "text": "My requests"},
            "blocks": blocks
        }
    )
