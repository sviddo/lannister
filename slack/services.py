from .views import app

def get_db_ready_user_list():
    #get all members from slack workspace
    workspace_members = app.client.users_list()['members']

    #get only non-deleted non-bot users from all members
    active_users = list(filter(lambda user: 
                                      user['id'] != 'USLACKBOT' and 
                                      user['is_bot'] == False and 
                                      user['deleted'] == False, 
                                workspace_members))

    #parse data for db in accessible manner
    users_to_add = []
    for user in active_users:
        new_user = {}
        new_user['service_id'] = user['id']
        if user['is_admin'] == True:
            new_user['roles'] = list(['a'])    
        else:
            new_user['roles'] = list(['cw'])  

        users_to_add.append(new_user)  

    return users_to_add
    
    