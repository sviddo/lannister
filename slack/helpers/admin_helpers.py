def admin_home_blocks():
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Would you like to change someone's role or should I show you all the requests?"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Changhe Role"
                    },
                    "action_id": "change_role_modal"
                },
                {
                    "type": "button",
                    "text": {
                    "type": "plain_text",
                    "text": "Show Requests"
                    }
                }
            ]
        }
    ]

    return blocks