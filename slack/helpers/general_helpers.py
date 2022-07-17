def header():
    view = {    
        "type": "home",
        "callback_id": "home_view",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Welcome to the _Lannister Assistant_* :tada:"
                }
            },
            {
                "type": "divider"
            } 
        ]  
    }

    return view