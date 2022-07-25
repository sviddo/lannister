import requests, json

def get_reviewers(context, next):
    user_id = context["user_id"]
    users_but_me=[]
    users_data = requests.get('http://127.0.0.1:8000/api/users')
    users = json.loads(users_data.text)
    users_but_me = filter(lambda user: user["service_id"] != user_id and "r" in user["roles"], users)
    context["reviewers"] = list(users_but_me)
    
    next()

def create_reviewer_block(context, next):
    reviewers = context['reviewers']
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
    
    context["options"] = list_of_reviewers
    next()

def create_make_request_view(context, next):
    options = context['options'] 
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
                    "text": "Select an item",
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

    context['blocks'] = blocks
    next()

def get_requests(context, next):
    """Get the list of all the request belonging to the current user"""
    user_id = context["user_id"]
    user_requests = requests.get(f'http://127.0.0.1:8000/api/requests/{user_id}')
    if user_requests.status_code == 400:
        context['requests'] = None
    else:
        user_requests =  json.loads(user_requests.text)
        valide = [request for request in user_requests if request['status'] in ('c', 'e')]
        context['requests'] = valide
        print(valide)
    
    next()

def get_request_details(context, next, body):
    """Get details about choosen request"""
    user_id = context['user_id']
    request_id = body['actions'][0]['block_id']
    user_requests = json.loads(requests.get(f'http://127.0.0.1:8000/api/requests/{user_id}').text)
    req_details = list(filter(lambda request: request['id'] == int(request_id), user_requests))[0]
    context['request'] = req_details
    
    next()

def create_see_requests_blocks(context, next):
    """Returns dictionary object wich will be
    passed to 'see_requests' modal to build it.
    Presents all user's reqest with possibility to edit."""

    requests = context['requests']
    blocks = []
    
    if requests:
        for request in requests:
            blocks.extend([
                {
                    "type": "section",
                    "block_id": f"{request['id']}_name",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"{request['bonus_type']}"
                    }
                },
                {
                    "type": "actions",
                    "block_id": f"{request['id']}",
                    "elements": [
                        {
                            "type": "button",
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

    context['blocks'] = blocks
    next()

def create_edit_request_blocks(context, next):
    request = context['request']
    reviewer = request['reviewer']
    options = context['options']
    
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
                "initial_option":  {
                    "text": {
                        "type": "plain_text",
                        "text": f"<@{reviewer}>"
                    },
                    "value": f"{reviewer}",
                },  
                "action_id": "bonus"
            },
            "label": {
                "type": "plain_text",
                "text": "Select the reviewer",
            }
        }
    ]

    context['blocks'] = blocks
    next()