import requests
import datetime

url = "https://df8f-45-67-20-226.eu.ngrok.io"

def return_users_to_add():
    return [{
        "service_id": "add-user-1",
        "roles": ["cw"]
    },
    {
        "service_id": "add-user-2",
        "roles": ["cw", "r"]
    },
    {
        "service_id": "add-user-3",
        "roles": ["cw", "r", "a"]
    }]
    
    
def save_users():
    for user in return_users_to_add():
        requests.post(url + "/api/add_user", json=user)
    
    
def return_workers():
    save_users()
        
    return [{
        "service_id": "worker-1",
        "roles": ["cw"]
    },
    {
        "service_id": "worker-2",
        "roles": ["cw"]
    },
    {
        "service_id": "worker-3",
        "roles": ["cw"]
    }]
    
    
def return_workers_and_reviewers():
    for user in return_users_to_add():
        requests.post(url + "/api/add_user", json=user)
        
    return [{
        "service_id": "worker-1",
        "roles": ["cw"]
    },
    {
        "service_id": "worker-2",
        "roles": ["cw", "r"]
    },
    {
        "service_id": "worker-3",
        "roles": ["cw", "r"]
    }]
    
    
def create_invalid_requests():
    """create requests as test cases for requests creation function"""
    return [{
    # just logic steps
        "creator": "add-user-1"
    },
    {
        "creator": "add-user-1",
        "reviewer": "add-user-2"
    },
    {
        "creator": "add-user-1",
        "reviewer": "add-user-2",
        "status": "b"
    },
    {
        "creator": "add-user-1",
        "reviewer": "add-user-2",
        "status": "c"
    },
    {
        "creator": "add-user-1",
        "reviewer": "add-user-2",
        "status": "c",
        "bonus_type": "jshdc"
    },
    # test creator
    {
        "creator": "hjhcjdcdsjkcndsjkcnjd",
        "reviewer": "add-user-2",
        "status": "c",
        "bonus_type": "jshdc",
        "description": "jshcjkds"
    },
    {
        "creator": "test_test_1",
        "reviewer": "add-user-2",
        "status": "c",
        "bonus_type": "jshdc",
        "description": "jshcjkds"
    },
    {
        "creator": "",
        "reviewer": "add-user-2",
        "status": "c",
        "bonus_type": "jshdc",
        "description": "jshcjkds"
    },
    # test reviewer
    {
        "creator": "add-user-1",
        "reviewer": "jksjcksnjkvnsjkvnvjn",
        "status": "c",
        "bonus_type": "jshdc",
        "description": "jshcjkds"
    },
    {
        "creator": "add-user-1",
        "reviewer": "test_test_1",
        "status": "c",
        "bonus_type": "jshdc",
        "description": "jshcjkds"
    },
    {
        "creator": "add-user-1",
        "reviewer": "",
        "status": "c",
        "bonus_type": "jshdc",
        "description": "jshcjkds"
    },
    {
        "creator": "add-user-2",
        "reviewer": "add-user-1",
        "status": "c",
        "bonus_type": "jshdc",
        "description": "jshcjkds"
    },
    # test 'status' field
    {
        "creator": "add-user-1",
        "reviewer": "add-user-2",
        "status": "r",
        "bonus_type": "jshdc",
        "description": "jshcjkds"
    },
    {
        "creator": "add-user-1",
        "reviewer": "add-user-2",
        "status": "a",
        "bonus_type": "jshdc",
        "description": "jshcjkds"
    },
    {
        "creator": "add-user-1",
        "reviewer": "add-user-2",
        "status": "p",
        "bonus_type": "jshdc",
        "description": "jshcjkds"
    },
    {
        "creator": "add-user-1",
        "reviewer": "add-user-2",
        "status": "e",
        "bonus_type": "jshdc",
        "description": "jshcjkds"
    },
    # test 'bonus_type' field
    {
        "creator": "add-user-1",
        "reviewer": "add-user-2",
        "status": "c",
        "bonus_type": "",
        "description": "jshcjkds"
    },
    {
        "creator": "add-user-1",
        "reviewer": "add-user-2",
        "status": "c",
        "bonus_type": "sjkhvjshvjdfhvccvvvvjfhvjkdfhvjkdfvh\
            jdvjhsvjkeehjvebvjskhjksafcsdcscsdchhjdfsjjkjds\
            fhjkdfhksdjkfhsdjfhsdjfhjhsdjfhjhdsjfhsdjfhsjkf",
        "description": "jshcjkds"
    },
    # test description
    {
        "creator": "add-user-1",
        "reviewer": "add-user-2",
        "status": "c",
        "bonus_type": "svdfv",
        "description": ""
    },
    # test 'creation_time' field
    {
        "creator": "add-user-1",
        "reviewer": "add-user-2",
        "status": "c",
        "bonus_type": "svdfv",
        "description": "svfbdffbd",
        "creation_time": "2022-07-28T05:17:40.931386Z"
    },
    # test 'paymant_day' field
    {
        "creator": "add-user-1",
        "reviewer": "add-user-2",
        "status": "c",
        "bonus_type": "svdfv",
        "description": "svfbdffbd",
        "creation_time": "2022-07-28T05:17:40.931386Z"
    }]
    
    
def create_valid_requests():
    tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
    save_users()
    
    return [{
        "creator": "add-user-1",
        "reviewer": "add-user-2",
        "bonus_type": "svdfv",
        "description": "svfbdffbd"
    },
    {
        "creator": "add-user-1",
        "reviewer": "add-user-3",
        "bonus_type": "abc",
        "description": "hsgjcn"
    },
    {
        "creator": "add-user-2",
        "reviewer": "add-user-3",
        "bonus_type": "poscpkdsclk",
        "description": "wjgd2e3jksh"
    },
    {
        "creator": "add-user-2",
        "reviewer": "add-user-3",
        "bonus_type": "klsvks",
        "description": "ysytfur"
    },
    {
        "creator": "add-user-3",
        "reviewer": "add-user-2",
        "bonus_type": "ajkch",
        "description": "opsokewn"
    },
    {
        "creator": "add-user-3",
        "reviewer": "add-user-2",
        "bonus_type": "pskcosjn",
        "description": "whjghdc"
    }]
    