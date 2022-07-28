import requests, json

URL = "http://127.0.0.1:8000"

def get_reviewers(context):
    user_id = context["user_id"]
    users_but_me=[]
    users_data = requests.get(f'{URL}/api/users')
    users = json.loads(users_data.text)
    users_but_me = filter(lambda user: user["service_id"] != user_id and "r" in user["roles"], users)
    return list(users_but_me)
    

def create_reviewer_block(reviewers):
    list_of_reviewers = []
    for reviewer in reviewers:
        option = {
            "text": {
                "type": "plain_text",
                "text": f"<@{reviewer['service_id']}>"
            },
            "value": f"{reviewer['service_id']}"
        }
        list_of_reviewers.append(option)
    
    return list_of_reviewers

def create_make_request_view(context):
    reviewers = get_reviewers(context)
    if reviewers:
        options = create_reviewer_block(reviewers)
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Provide us with the information about your request, please",
                }
            },
            {
                "type": "input",
                "block_id": "bonus_type",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "bonus",
                    "min_length": 5,
                    "max_length": 80,
                    "placeholder": {
                        "type": "plain_text",
                        "text": "What type of bonus is it? (up to 80 characters)",
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Bonus type",
                }
            },
            {
                "type": "input",
                "block_id": "request_description",
                "element": {
                    "type": "plain_text_input",
                    "multiline": True,
                    "action_id": "bonus",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Let us know about the request details",
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Bunus description",
                }
            },
            {
                "type": "input",
                "block_id": "request_reviewer",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a reviewer",
                    },
                    "options": options,
                    "action_id": "bonus"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Select the reviewer",
                }
            }
        ]
    else:
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "You can't create a request as for now because there're no reviewers",
                }
            }
        ]

    return blocks

def get_requests(context):
    """Get the list of all the request belonging to the current user"""
    user_id = context["user_id"]
    user_requests = requests.get(f'{URL}/api/requests/{user_id}')
    if user_requests.status_code == 400:
        return None
    else: 
        user_requests =  user_requests.json()
        valide = [request for request in user_requests if request['status'] in ('c', 'e')]
        return valide


def create_see_requests_blocks(context):
    """Returns dictionary object wich will be
    passed to 'see_requests' modal to build it.
    Presents all user's reqest with possibility to edit."""
    reviewers = get_reviewers(context)
    requests = get_requests(context)
    blocks = []

    if reviewers:
        btns = [
                    {
                        "type": "button",
                        "style": "primary",
                        "text": {
                            "type": "plain_text",
                            "text": "Edit",
                        },
                        "value": "edit",
                        "action_id": "edit_request"
                    },
                    {
                        "type": "button",
                        "style": "danger",
                        "text": {
                            "type": "plain_text",
                            "text": "Delete",
                        },
                        "value": "delete",
                        "action_id": "delete_request"
                    }
                ]
    else:
        btns = [
                    {
                        "type": "button",
                        "style": "danger",
                        "text": {
                            "type": "plain_text",
                            "text": "Delete",
                        },
                        "value": "delete",
                        "action_id": "delete_request"
                    }
                ]

    if requests:
        for request in requests:
            blocks.extend([
                {
                    "type": "section",
                    "block_id": f"{request['id']}_name",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{request['bonus_type']}*"
                    }
                },
                {
                    "type": "actions",
                    "block_id": f"{request['id']}",
                    "elements": btns
                }
            ]
            )
    else:
        blocks = [{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "There's nothing to show yet",
			}
		}]

    return blocks


def get_request_details(context, request_id):
    """Get details about choosen request"""
    user_id = context['user_id']
    user_requests = json.loads(requests.get(f'{URL}/api/requests/{user_id}').text)
    req_details = list(filter(lambda request: request['id'] == int(request_id), user_requests))[0]
    return req_details
    

def create_edit_request_blocks(context, request):
    reviewer = request['reviewer']
    options = create_reviewer_block(get_reviewers(context))

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "Update the request with new info, please",
            }
        },
        {
            "type": "input",
            "block_id": "bonus_type",
            "element": {
                "type": "plain_text_input",
                "initial_value": f"{request['bonus_type']}",
                "action_id": "bonus",
                "placeholder": {
                    "type": "plain_text",
                    "text": "What type of bonus is it? (up to 80 characters)",
                }
            },
            "label": {
                "type": "plain_text",
                "text": "Bonus type",
            }
        },
        {
            "type": "input",
            "block_id": "request_description",
            "element": {
                "type": "plain_text_input",
                "initial_value": f"{request['description']}",
                "multiline": True,
                "action_id": "bonus",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Let us know about the request details",
                }
            },
            "label": {
                "type": "plain_text",
                "text": "Bunus description",
            }
        },
        {
            "type": "input",
            "block_id": "request_reviewer", 
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a reviewer",
                },
                "options": options,  
                "action_id": "bonus"
            },
            "label": {
                "type": "plain_text",
                "text": "Select the reviewer",
            }
        }
    ]

    if reviewer != "no reviewer assigned": 
        blocks[3]['element']['initial_option'] = {
            "text": {
                "type": "plain_text",
                "text": f"<@{reviewer}>"
            },
            "value": f"{reviewer}"
        }
    
    return blocks