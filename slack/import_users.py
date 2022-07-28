from slack.services import get_db_ready_user_list as users_
import requests

users = users_()

for user in users:
    requests.post('http://127.0.0.1:8000/api/add_user', json=user)