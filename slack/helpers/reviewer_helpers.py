def reviewer_home_blocks():
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*For reviewers:*"
            }
        },
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
					"action_id": "next_assigned_requests_modal"
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
					"action_id": "previous_assigned_requests_modal"
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
					"action_id": "previous_assigned_requests_modal"
				},
                {
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Next Page",
						"emoji": True
					},
					"value": "next",
					"action_id": "next_assigned_requests_modal"
				}
			]
		}