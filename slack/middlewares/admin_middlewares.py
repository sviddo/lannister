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
    all_requests = json.loads(requests_data.text)

    context["requests"] = all_requests
    next()

def create_request_blocks(context, next):
    requests = context['requests']
    blocks = []
    for request in requests:
        creation_time = dt.strptime(request['creation_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        creation_time_parsed = f"{creation_time.year}-{creation_time.month}-{creation_time.day}  {creation_time.hour}:{creation_time.minute}:{creation_time.second}"
        message = f"*Creator:* <@{request['creator']}>\n*Reviewer:* <@{request['reviewer']}>\n*Creation time:* {creation_time_parsed}\n "
        blocks.extend(
            [
                {
                    "type": "section",
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
                        "action_id": "see_request_history"
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

    context['blocks'] = blocks
    next()