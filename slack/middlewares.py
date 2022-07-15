import requests, json

def publish_admin_view(user_id):
    view = {
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
                "text": f"<@{user_id}>, would you like to change someone's role or should I show you all the requests?"
                }
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                        "type": "plain_text",
                        "text": "Changhe Role"
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

    return view
        


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