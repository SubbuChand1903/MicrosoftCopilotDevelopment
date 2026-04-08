def add_comment_card(ticket_id):
    return {
        "type": "AdaptiveCard",
        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.5",
        "body": [
            {
                "type": "TextBlock",
                "text": "💬 Add Comment",
                "weight": "Bolder",
                "size": "ExtraLarge",
                "color": "Accent"
            },
            {
                "type": "TextBlock",
                "text": f"Ticket: {ticket_id}",
                "isSubtle": True,
                "spacing": "Small"
            },
            {"type": "Separator"},
            {
                "type": "TextBlock",
                "text": "Your Name",
                "weight": "Bolder",
                "size": "Small",
                "spacing": "Medium"
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