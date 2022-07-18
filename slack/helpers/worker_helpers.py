def reviewer_home_blocks():
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Would you like to create a new request or see/edit existing ones?"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Create request"
                    },
                    "action_id": "create_request_modal"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "See requests"
                    },
                    "action_id": "see_requests_modal"
                }
            ]
        }
    ]

    return blocks