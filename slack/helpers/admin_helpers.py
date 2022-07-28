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
                    },
                    "action_id": "show_requests_modal"
                }
            ]
        }
    ]

    return blocks

def appen_button_next():
    return {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Next Page",
						"emoji": True
					},
					"value": "next",
					"action_id": "show_next_requests"
				}
			]
		}

def appen_button_previous():
    return {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Previous Page",
						"emoji": True
					},
					"value": "previous",
					"action_id": "show_previous_requests"
				}
			]
		}

def appen_buttons():
    return {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Previous Page",
						"emoji": True
					},
					"value": "previous",
					"action_id": "show_previous_requests"
				},
                {
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Next Page",
						"emoji": True
					},
					"value": "next",
					"action_id": "show_next_requests"
				}
			]
		}