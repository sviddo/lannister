import requests, json
from datetime import datetime as dt

def get_all_users_but_self(context, next):
    user_id = context["user_id"]
    users_but_me=[]
    users_data = requests.get('http://127.0.0.1:8000/api/users')
    users = json.loads(users_data.text)
    users_but_me = filter(lambda user: user["service_id"] != user_id, users)

    context["users"] = list(users_but_me)
    
    next()

def create_blocks(context, next):
    users = context["users"]
    blocks = []
    for user in users:
        user_role = ""
        user_value = ""
        if("r" in user["roles"]):
            user_role = "r"
            user_value = "reviewer"
        else:
            user_role = "cw"
            user_value = "worker"
        blocks.append(
            {
                "type": "section",
                "block_id": f"{user['service_id']}",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{user['service_id']}>"
                },
                "accessory": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a role",
                    },
                    "initial_option": {
                        "value": f"{user_role}",
                        "text": {
                            "type": "plain_text",
                            "text": f"{user_value}"
                        }
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "reviewer",
                            },
                            "value": "r"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "worker",
                            },
                            "value": "cw"
                        }
                    ],
                "action_id": "user_role_has_been_changed"
                }
            }
        )
    context["blocks"] = blocks
    next()

def get_requests(context, next):
    requests_data = requests.get('http://127.0.0.1:8000/api/requests')
    
    if requests_data.status_code == 400:
        context['requests'] = None
    else:
        context['requests']  = json.loads(requests_data.text)
    next()

def create_request_blocks(context, next):
    requests = context['requests']
    blocks = []

    if requests:
        for request in requests:
            creation_time = dt.strptime(request['creation_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
            creation_time_parsed = f"{creation_time.year}-{creation_time.month}-{creation_time.day}  {creation_time.hour}:{creation_time.minute}:{creation_time.second}"
            message = f"*Creator:* <@{request['creator']}>\n*Reviewer:* <@{request['reviewer']}>\n*Creation time:* {creation_time_parsed}\n "
            blocks.extend(  
                [
                    {
                        "type": "section",
                        "block_id": f"{request['id']}",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"{request['bonus_type']}"
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Request History"
                            },
                            "value": "see_request_history",
                            "action_id": "request_history_modal"
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "mrkdwn",
                                "text": message
                            }
                        ]
                    },
                    {
                        "type": "divider"
                    }
                ]
            )

        # get rid off the last divider block
        del(blocks[-1])

    else:
        blocks = [{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "There's nothing to show yet",
			}
		}]

    context['blocks'] = blocks
    next()


def create_request_history_blocks(next, context):
    request_history = context['request_history']
    blocks = []

    for request in request_history:
        modified_time = dt.strptime(request['modified'], '%Y-%m-%dT%H:%M:%S.%fZ')
        modified_time_parsed = f"{modified_time.year}-{modified_time.month}-{modified_time.day}  {modified_time.hour}:{modified_time.minute}:{modified_time.second}"
        message = ""
        if request['type_of_change'] == 'c':
            message = "Request has been created  🆕" 
        elif request['type_of_change'] == 'e':
            message = "Request has been edited  ✏️"
        elif request['type_of_change'] == 'a':
            message = "Request has been approved  ✔️"
        elif request['type_of_change'] == 'r':
            message = "Request has been rejected  ❌"
        elif request['type_of_change'] == 'p':
            message = "Bonus has been paid  💵"
        blocks.extend(  
            [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": f"{message}",
                        "emoji": True
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Date:* {modified_time_parsed}"
                        }
                    ]
                },
                {
                    "type": "divider"
                }
            ]     
        )

    # get rid off the last diider block
    del(blocks[-1])

    context['blocks'] = blocks
    next()

def get_request_history(next, context, body):
    # function returns request history 
    # for selected request
    request_id = body['actions'][0]['block_id']

    requests_history_data = requests.get('http://127.0.0.1:8000/api/requests_history')
    requests_history = json.loads(requests_history_data.text)
    request_history = [request for request in requests_history if request['request'] == int(request_id)]
    context['request_history'] = request_history

    next()