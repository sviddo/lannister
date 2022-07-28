import pytest
import requests

url = "http://127.0.0.1:8000"

def test_get_requests():
    entire_url = url + "/api/requests"
    all_requests = requests.get(url=entire_url)
    
    assert all_requests.status_code == 200 or \
        all_requests.status_code == 400 and all_requests.json() == ["No requests created!"]
