import datetime
import requests, json
from slack import app

# def get_db_ready_user_list():
#     #get all members from slack workspace
#     workspace_members = app.client.users_list()['members']

#     #get only non-deleted non-bot users from all members
#     active_users = list(filter(lambda user: 
#                                       user['id'] != 'USLACKBOT' and 
#                                       user['is_bot'] == False and 
#                                       user['deleted'] == False, 
#                                 workspace_members))

#     #parse data for db in accessible manner
#     users_to_add = []
#     for user in active_users:
#         new_user = {}
#         new_user['service_id'] = user['id']
#         if user['is_admin'] == True:
#             new_user['roles'] = list(['a'])    
#         else:
#             new_user['roles'] = list(['cw'])  

#         users_to_add.append(new_user)  

#     return users_to_add
    
def get_user_roles(user_id):
    users_data = requests.get('http://127.0.0.1:8000/api/users')
    users = json.loads(users_data.text)
    user_in_db = list(filter(lambda user: user["service_id"] == user_id, users))[0]

    return user_in_db['roles']


users_list = {}

def get_user_list(assigned_requests, app):
    global users_list
    for request in assigned_requests:
        creator = request['creator']
        reviewer = request['reviewer']
        users_list[creator] = app.client.users_info(user=creator)['user']['real_name']
        users_list[reviewer] = app.client.users_info(user=reviewer)['user']['real_name']

    return users_list


def get_assigned_requests(reviewer_id):
    assigned_requests = requests.get(f'http://127.0.0.1:8000/api/reviewer_requests/{reviewer_id}')
    if assigned_requests.status_code != 200:
        return []
    assigned_requests = assigned_requests.json()
    non_reviewed_requests = []
    for request in assigned_requests:
        if request['status'] in ('c', 'e'):
            non_reviewed_requests.append(request)

    return non_reviewed_requests



requests_blocks = [{
    "type": "header",
    "text": {
        "type": "plain_text",
        "text": "We are loading your requests! Please, try again in a few seconds ...",
    }
}]


def create_assigned_requests_blocks(assigned_requests):
    """Returns dictionary object wich will be
    passed to 'see_requests' modal to build it.
    Presents all user's reqest with possibility to edit."""
    if not assigned_requests:
        return [{
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "There are no assigned requests for you :man-shrugging:",
                "emoji": True
            }
        }]

    global user_list
    users_list = get_user_list(assigned_requests, app)
    global requests_blocks
    if requests_blocks:
        requests_blocks = []

    for request in assigned_requests:
        creator = request['creator']
        extended_statuses = {
            "c": "created",
            "e": "edited"
        }
        status_extended = extended_statuses[request['status']]
        bonus_type = request['bonus_type']
        requests_blocks.extend([{
            "type": "section",
            "block_id": f"{request['id']}",
            "text": {
                "type": "mrkdwn",
                "text": f"*Creator:* @{users_list[creator]}\n*Bonus type:* {bonus_type}\n*Status:* {status_extended}"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Change status"
                },
                "style": "primary",
                "value": "change_status",
                "action_id": "change_request_status"
            }
        }])

    return requests_blocks


def get_initial_date():
    today = datetime.datetime.today()
    next_day = today + datetime.timedelta(days=1)
    return next_day
