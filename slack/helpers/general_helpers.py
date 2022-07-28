import json

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
                    "text": "Plese, stay with us. We're loading the data.",
                    "emoji": True
                }
            }]
        }

    return view

def parse_dict(dict):
    return json.dumps(dict)

def parse_string(string):
    return json.loads(string)