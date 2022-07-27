from django.views.decorators.csrf import csrf_exempt
from slack import app
from slack_bolt.adapter.django import SlackRequestHandler
from datetime import datetime

# constant variable to store url of API service
URL = "http://127.0.0.1:8000"

from .middlewares import (
    admin_middlewares as am, 
    worker_middlewares as wm, 
    reviewer_middlewares as rm,
)
from .helpers import (
    admin_helpers as ah, 
    general_helpers as gh, 
    worker_helpers as wh, 
    reviewer_helpers as rh,
)
from .services import (
    get_user_roles, 
    get_assigned_requests, 
    create_assigned_requests_blocks, 
    get_initial_date
)
import requests, json


handler = SlackRequestHandler(app=app)

@csrf_exempt
def events(request):
    return handler.handle(request)

@app.event('app_home_opened')
def update_home_tab(client, event, logger):
    user_id=event["user"]
    user_roles = get_user_roles(user_id)
    view = gh.header()
    blocks = []

    # check the role of the user who opened the home tab
    # thereafter build blocks accordinly
    if 'cw' in user_roles:
        blocks = wh.worker_home_blocks()
        view['blocks'].extend(blocks)

    if 'r' in user_roles:
        reviewer_blocks = rh.reviewer_home_blocks()
        view['blocks'].extend(reviewer_blocks)
        # assigned_requests = get_assigned_requests(user_id)
        # global requests_blocks
        # from .services import requests_blocks
        # requests_blocks = create_assigned_requests_blocks(assigned_requests)

    if 'a' in user_roles:
        blocks = ah.admin_home_blocks()
        view['blocks'].extend(blocks)

        # temporary add worker & reviewer functionalities
        # to admin for testing purposes
        blocks = wh.worker_home_blocks()
        view['blocks'].extend(blocks)


    try:
        client.views_publish(user_id=user_id, view=view)
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.view("admin_view")
def change_role_submission(ack, say, body):
    ack()
    say(channel=body['user']['id'], 
        text="Just wanted to inform you that all the changes "
             "has been made and user roles have been updated successfully")

@app.action("change_role_modal")
def handle_some_action(ack, context, client, body):
    ack()

    # TODO: if no users print that there's no users to show
    users = am.get_all_users_but_self(context)
    blocks = am.create_user_role_blocks(users)

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


@app.action("show_requests_modal")
def show_all_requests(ack, client, body):
    ack()
    old_view = client.views_open(
        trigger_id=body['trigger_id'],
        view=gh.loader("Requests")
    )

    requests = am.get_requests()
    blocks = am.create_request_blocks(requests)[:100]
    # TODO: show requests within 100 blocks
    # and if there're more then update the view
    # with next/previous buttons

    client.views_update(
        view_id=old_view["view"]["id"],
        view={
            "type": "modal",
            "callback_id": "new_request_submission",
            "title": {"type": "plain_text", "text": "Requests"},
            "blocks": blocks
        }
    )

@app.action("request_history_modal")
def create_requst_history_modal(ack, client, body):
    ack()

    request_id = body['actions'][0]['block_id']
    blocks = am.create_request_history_blocks(request_id)
    client.views_push(
        trigger_id=body['trigger_id'],
        view={
            "type": "modal",
            "callback_id": "show_reqest_history",
            "private_metadata": f"{request_id}",
            "title": {"type": "plain_text", "text": "History"},
            "blocks": blocks
        }
    )

@app.action("user_role_has_been_changed")
def aknowladge(ack, body):
    ack()  
    user_id = body['actions'][0]['block_id']
    user_role = body['actions'][0]['selected_option']['value']
    user_in_db = requests.get(f'{URL}/api/user/{user_id}').json()

    uri = f'{URL}/api/reviewer_role/{user_id}'
    if user_role == "r" and user_role not in user_in_db["roles"]:
        requests.patch(uri)
    elif user_role == "cw" and "r" in user_in_db["roles"]:
        requests.delete(uri)


@app.action("create_request_modal")
def create_request(ack, client, body, context):
    ack()
    blocks = wm.create_make_request_view(context)
    
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


@app.view("new_request_submission")
def create_new_request(ack, body, say):
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
    uri = f'{URL}/api/create_request'
    r = requests.post(uri, json=request)

    # validate the response
    # inform the reviewer about new reqest
    if r.status_code == 201:
        say(
            channel=request_reviewer, 
            text=f"You've just recieved a new bonus request from <@{body['user']['id']}>. "\
            "Take a look in the app home!"
        )


@app.action("see_requests_modal")
def show_requests(ack, client, body, context):
    """Show a new modal window with a list
       of all the user's requests.

       User can edit selected request
    """
    ack()
    old_view = client.views_open(
        trigger_id=body['trigger_id'],
        view=gh.loader("Requests")
    )

    blocks = wm.create_see_requests_blocks(context)
    client.views_update(
        view_id=old_view['view']['id'],
        view={
            "type": "modal",
            "callback_id": "see_requests_modal_submission",
            "external_id": "user_requestss",
            "title": {"type": "plain_text", "text": "My requests"},
            "blocks": blocks
        }
    )

@app.action("edit_request")
def edit_request(ack, body, client, context):
    """Edit/Delete user's own request"""
    ack()
    request_id = body['actions'][0]['block_id']
    request = wm.get_request_details(context, request_id)
    blocks = wm.create_edit_request_blocks(context, request)
    
    request_reviewer = request['reviewer']

    client.views_push(
        trigger_id=body['trigger_id'],
        view={
            "type": "modal",
            "callback_id": "edit_request_submission",
            "private_metadata": f"{request_id}, {request_reviewer}",
            "title": {"type": "plain_text", "text": "Edit request"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": blocks
        }
    )



@app.view("edit_request_submission")
def update_request(ack, body, client, context, say):
    ack()

    # get all the values the user has submitted
    submited_values = body['view']['state']['values']
    
    # assign the values to the variables
    # which we'll need to edit the request in db
    bonus_type = submited_values['bonus_type']['bonus']['value']
    request_description = submited_values['request_description']['bonus']['value']
    request_reviewer = submited_values['request_reviewer']['bonus']['selected_option']['value']
    request_id, initial_reviewer = body['view']['private_metadata'].split(', ')

    request = {
        "reviewer": request_reviewer,
        "bonus_type": bonus_type,
        "description": request_description,
    }

    # put request to db
    uri = f'{URL}/api/request/{request_id}'
    r = requests.patch(uri, json=request)

    # TODO: validate the response
    if request_reviewer == initial_reviewer:
        say(
            channel=request_reviewer, 
            text=f"<@{body['user']['id']}> has modified his request '{bonus_type}' just now, take a look!"
        )
    else:
        say(
            channel=request_reviewer, 
            text=f"<@{body['user']['id']}> has assigned the new request for you just now, take a look!"
        )


    blocks = wm.create_see_requests_blocks(context)
    for block in blocks:
        if block['block_id'] == f'{request_id}_name':
            block['text']['text'] = request["bonus_type"]
  
    client.views_update(
        external_id="user_requestss",
        view={
            "type": "modal",
            "external_id": "user_requestss",
            "callback_id": "see_requests_modal_submission",
            "title": {"type": "plain_text", "text": "My requests"},
            "blocks": blocks
        }
    )


@app.action("delete_request")
def handle_some_action(ack, body, context, client):
    ack()

    request_id = body['actions'][0]['block_id']
    old_blocks = wm.create_see_requests_blocks(context)
    blocks = [block for block in old_blocks if not (block['block_id'] == str(request_id) or block['block_id'] == f'{request_id}_name')]
    
    uri = f'{URL}/api/request/{request_id}'
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


@app.action("view_assigned_requests_modal")
def view_assigned_requests(ack, client, body, context):
    ack()
    old_view = client.views_open(
        trigger_id=body['trigger_id'],
        view=gh.loader("Assigned Requests")
    )
    requests = rm.get_reviewer_requests(context)
    blocks = []

    if not requests:
        blocks = [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "There are no assigned requests for you :man-shrugging:",
                "emoji": True
            }
        }]
    else:
        blocks = create_assigned_requests_blocks(requests)

    client.views_update(
        view_id=old_view['view']['id'],
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "Assigned requests"},
            "blocks": blocks
        }
    )

@app.action("change_request_status")
def edit_request(ack, body, client, context):
    ack()
    request_id = body['view']['blocks'][0]['block_id']
    request = rm.get_request_details(context, request_id)

    blocks = rm.create_change_status_blocks(request)
    client.views_push(
        trigger_id=body['trigger_id'],
        view={
            "type": "modal",
            "private_metadata": f"{body['view']['id']}, {request_id}",
            "title": {"type": "plain_text", "text": "Change request status"},
            "blocks": blocks
        }
    )


@app.action("reject_request")
def reject_request(ack, body, client, context):
    ack()
    view_id, request_id = body['view']['private_metadata'].split(', ')
    
    request_context = rm.get_request_details(context, request_id)
    reviewer_requests = rm.get_reviewer_requests(context)
    requests_blocks = create_assigned_requests_blocks(reviewer_requests)
    updated_blocks = [block for block in requests_blocks if block['block_id'] != str(request_context['id'])]

    
    uri = f'{URL}/api/request/{request_context["id"]}'
    data = {
        "status": "r"
    }
    requests.patch(url=uri, json=data)

    channel_id = app.client.conversations_open(users=request_context['creator'])['channel']['id']
    app.client.chat_postMessage(channel=channel_id, text=f":pensive: *Unfortunately your request with following data was rejected:*\n\
*Reviewer*: <@{request_context['reviewer']}>\n\
*Bonus_type*: {request_context['bonus_type']}\n\
*Description*: {request_context['description']}\n\
*Creation time*: {request_context['creation_time']}")

    #update the original view
    client.views_update(
        view_id=body['view']['id'],
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "Assigned requests"},
            "blocks": [{
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": ":white_check_mark: Request has been rejected!",
                        "emoji": True
                    }
                }]
        }
    )

   
    # update the previous view with
    # rejected request excluded
    if not updated_blocks:
        updated_blocks = [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "There are no assigned requests for you :man-shrugging:",
                "emoji": True
            }
        }]

    client.views_update(
        view_id=body['view']['previous_view_id'],
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "Assigned requests"},
            "blocks": updated_blocks
        }
    )



@app.action("approve_request")
def approve_request(ack, body, client, context):
    ack()
    view_id, request_id = body['view']['private_metadata'].split(', ')
    request_context = rm.get_request_details(context, request_id)
    initial_date = get_initial_date()
    year, month, day = initial_date.year, initial_date.month, initial_date.day
    text = f"*Creator:* <@{request_context['creator']}>\n"
    text += f"*Bonus_type:* {request_context['bonus_type']}\n"
    text += f"*Status:* approved\n"
    text += f"*Description:* {request_context['description']}\n"
    text += f"*Creation_time:* {request_context['creation_time']}\n"

    blocks = []
    blocks.append(body['view']['blocks'][0])
    blocks[0]['text']['text'] = text
    blocks.append(
        {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Paymant_day:*"
      },
      "accessory": {
        "type": "datepicker",
        "initial_date": f"{year}-{month}-{day}",
        "placeholder": {
          "type": "plain_text",
          "text": "Select a date",
        },
        "action_id": "datepicker-action"
      }
    }
    )

    client.views_update(
        view_id=body['view']['id'],
        view={
            "type": "modal",
            "callback_id": "make_request_approved",
            "private_metadata": f"{body['view']['id']}, {request_id}",
            "title": {"type": "plain_text", "text": "Approve request"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "blocks": blocks
        }
    )


@app.view("make_request_approved")
def make_request_approved(ack, body, context, client):
    ack(response_action="update", view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "Assigned requests"},
            "blocks": [{
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": ":white_check_mark: Request has been approved!",
                    "emoji": True
                }
            }]
        })

    view_id, request_id = body['view']['private_metadata'].split(', ')
    request_context = rm.get_request_details(context, request_id)
    paymant_day = list(body['view']['state']['values'].values())[0]['datepicker-action']['selected_date']

    # update the previous view with
    # approved request excluded
    reviewer_requests = rm.get_reviewer_requests(context)
    requests_blocks = create_assigned_requests_blocks(reviewer_requests)
    updated_blocks = [block for block in requests_blocks if block['block_id'] != str(request_context['id'])]
    uri = f'{URL}/api/request/{request_context["id"]}'
    data = {
        "status": "a",
        "paymant_day": f"{paymant_day}"

    }
    requests.patch(url=uri, json=data)

    channel_id = app.client.conversations_open(users=request_context['creator'])['channel']['id']
    app.client.chat_postMessage(channel=channel_id, text=f":tada: *Congratulations! Your request with following data was approved:*\n\
*Reviewer*: <@{request_context['reviewer']}>\n\
*Bonus_type*: {request_context['bonus_type']}\n\
*Description*: {request_context['description']}\n\
*Creation time*: {request_context['creation_time']}")


    if not updated_blocks:
        updated_blocks = [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "There are no assigned requests for you :man-shrugging:",
                "emoji": True
            }
        }]

    client.views_update(
        view_id=body['view']['previous_view_id'],
        view={
            "type": "modal",
            "title": {"type": "plain_text", "text": "Assigned requests"},
            "blocks": updated_blocks
        }
    )


@app.action("datepicker-action")
def handle_some_action(ack, body, client):
    ack()
    initial_date = list(body['view']['state']['values'].
                            values())[0]['datepicker-action']['selected_date'].split("-")
    diff = datetime(
        int(initial_date[0]),
        int(initial_date[1]),
        int(initial_date[2])
    ) - datetime.now()

    if diff.total_seconds() < 0:
        blocks = body['view']['blocks']
        if len(blocks) == 3:
            blocks.pop(-1)
        initial_date = get_initial_date()
        initial_year = initial_date.year
        initial_month = initial_date.month
        initial_day = initial_date.day
        blocks[-1]['accessory']['initial_date'] = f"{initial_year}-{initial_month}-{initial_day}"
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*'Paymant_day' field must be date from tomorrow!*"
                }
            }
        )

        client.views_update(
            view_id=body['view']['id'],
            view={
                "type": "modal",
                "title": {"type": "plain_text", "text": "Approve request"},
                "blocks": blocks
            }
        )
    else:
        blocks = body['view']['blocks']
        if len(blocks) == 3:
            blocks.pop(-1)
        
        client.views_update(
            view_id=body['view']['id'],
            view={
                "type": "modal",
                "callback_id": "make_request_approved",
                "title": {"type": "plain_text", "text": "Approve request"},
                "submit": {"type": "plain_text", "text": "Submit"},
                "blocks": blocks
            }
        )