def reviewer_home_blocks():
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Would you like to view assigned requests?"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "View assigned requests"
                    },
                    "action_id": "view_assigned_requests_modal"
                },
            ]
        }
    ]

    return blocks