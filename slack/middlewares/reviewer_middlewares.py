import requests
import json
from datetime import datetime
from slack.services import users_list


def get_request_details(context, body, next=None):
    reviewer_id = context['user_id']
    request_id = body['actions'][0]['block_id']
    user_requests = json.loads(requests.get(f'http://127.0.0.1:8000/api/reviewer_requests/{reviewer_id}').text)

    request_details = list(filter(lambda request: request['id'] == int(request_id), user_requests))[0]
    extended_statuses = {
        "c": "created",
        "e": "edited"
    }
    creation_time = datetime.strptime(request_details['creation_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    request_details['creation_time'] = f"{creation_time.year}-{creation_time.month}-{creation_time.day}  {creation_time.hour}:{creation_time.minute}:{creation_time.second}"
    request_details['status_extended'] = extended_statuses[request_details['status']]
    context['request'] = request_details

    if next:
        next()

    return context['request']


def create_change_status_blocks(context, next):
    request = context['request']
    creator = users_list[request['creator']]
    status_extended = request['status_extended']
    bonus_type = request['bonus_type']
    description = request['description']
    creation_time = request['creation_time']
    
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Creator:* @{creator}\n*Bonus type:* {bonus_type}\n*Status:* {status_extended}\n*Bonus_type:* {bonus_type}\n*Description:* {description}\n*Creation_time:* {creation_time}"
            }
        },
        {
                "type": "actions",
                "block_id": f"{request['id']}",
                "elements": [
                    {
                        "type": "button",
                        "style": "danger",
                        "text": {
                            "type": "plain_text",
                            "text": "Reject",
                        },
                        "value": "reject",
                        "action_id": "reject_request"
                    },
                    {
                        "type": "button",
                        "style": "primary",
                        "text": {
                            "type": "plain_text",
                            "text": "Approve",
                        },
                        "value": "approve",
                        "action_id": "approve_request"
                    }
          ]
        }
    ]

    context['blocks'] = blocks

    next()