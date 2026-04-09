def add_comment_card(ticket_id):
    return {
        "type": "AdaptiveCard",
        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.5",
        "body": [
            {
                "type": "Container",
                "style": "accent",
                "bleed": True,
                "items": [
                    {
                        "type": "ColumnSet",
                        "columns": [
                            {
                                "type": "Column",
                                "width": "auto",
                                "verticalContentAlignment": "Center",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "💬",
                                        "size": "Large"
                                    }
                                ]
                            },
                            {
                                "type": "Column",
                                "width": "stretch",
                                "verticalContentAlignment": "Center",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "Add Comment",
                                        "weight": "Bolder",
                                        "size": "Medium",
                                        "wrap": True
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": f"Ticket: {ticket_id}",
                                        "size": "Small",
                                        "isSubtle": True,
                                        "spacing": "None",
                                        "wrap": True
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "Container",
                "spacing": "Medium",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": "COMMENT DETAILS",
                        "size": "Small",
                        "weight": "Bolder",
                        "color": "Accent",
                        "spacing": "None"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Your Name",
                        "weight": "Bolder",
                        "size": "Small",
                        "spacing": "Small"
                    },
                    {
                        "type": "Input.Text",
                        "id": "author",
                        "placeholder": "Enter your name"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Comment",
                        "weight": "Bolder",
                        "size": "Small",
                        "spacing": "Small"
                    },
                    {
                        "type": "Input.Text",
                        "id": "comment",
                        "placeholder": "Type your comment here...",
                        "isMultiline": True
                    }
                ]
            }
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "title": "💬 Submit Comment",
                "style": "positive",
                "data": {
                    "action": "submit_comment",
                    "ticket_id": ticket_id
                }
            },
            {
                "type": "Action.Submit",
                "title": "← Back to Ticket",
                "data": {
                    "action": "view_ticket",
                    "ticket_id": ticket_id
                }
            }
        ]
    }