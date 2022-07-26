import requests
import json
from datetime import datetime

def get_request_details(context, request_id):
    reviewer_id = context['user_id']
    user_requests = json.loads(requests.get(f'http://127.0.0.1:8000/api/reviewer_requests/{reviewer_id}').text)

    request_details = list(filter(lambda request: request['id'] == int(request_id), user_requests))[0]
    extended_statuses = {
        "c": "created",
        "e": "edited"
    }
    creation_time = datetime.strptime(request_details['creation_time'], '%Y-%m-%dT%H:%M:%S.%fZ')
    request_details['creation_time'] = f"{creation_time.year}-{creation_time.month}-{creation_time.day}  {creation_time.hour}:{creation_time.minute}:{creation_time.second}"
    request_details['status_extended'] = extended_statuses[request_details['status']]
    print(request_details)
    return request_details




def create_change_status_blocks(request):
    creator = request['creator']
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

    return blocks

def get_reviewer_requests(context):
    reviewer_id = context['user_id']
    assigned_requests = requests.get(f'http://127.0.0.1:8000/api/reviewer_requests/{reviewer_id}')
    if assigned_requests.status_code != 200:
        return None
    else:
        assigned_requests = assigned_requests.json()
        non_reviewed_requests = []
        for request in assigned_requests:
            if request['status'] in ('c', 'e'):
                non_reviewed_requests.append(request)

        return  non_reviewed_requests
    next()