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

def loader(title):
    view = {
            "type": "modal",
            "title": {"type": "plain_text", "text": title},
            "blocks": [{
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Plese, stay calm. We're loading the data.",
                    "emoji": True
                }
            }]
        }

    return view