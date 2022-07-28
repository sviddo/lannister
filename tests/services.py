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
    
    
def return_workers():
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