import requests
import pytest

url = "https://app-cthojegtpq-uc.a.run.app"

def test_get_users():
    entire_url = url + "/api/users"
    users = requests.get(url=entire_url)
    
    assert users.status_code == 200 or \
        users.status_code == 404 and users.json() == ["No users!"]