def create_ticket_form():
    return {
        "type": "AdaptiveCard",
        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.5",
        "body": [
            {
                "type": "TextBlock",
                "text": "➕ Create New Ticket",
                "weight": "Bolder",
                "size": "ExtraLarge",
                "color": "Accent"
            },
            {
                "type": "TextBlock",
                "text": "Fill in the details below",
                "isSubtle": True,
                "spacing": "Small"
            },
            {"type": "Separator"},
            {
                "type": "TextBlock",
                "text": "Title *",
                "weight": "Bolder",
                "size": "Small",
                "spacing": "Medium"
            },
            {
                "type": "Input.Text",
                "id": "title",
                "placeholder": "e.g. Login page not loading"
            },
            {
                "type": "TextBlock",
                "text": "Description",
                "weight": "Bolder",
                "size": "Small",
                "spacing": "Small"
            },
            {
                "type": "Input.Text",
                "id": "description",
                "placeholder": "Describe the issue in detail...",
                "isMultiline": True
            },
            {
                "type": "ColumnSet",
                "spacing": "Small",
                "columns": [
                    {
                        "type": "Column",
                        "width": "stretch",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "Priority",
                                "weight": "Bolder",
                                "size": "Small"
                            },
                            {
                                "type": "Input.ChoiceSet",
                                "id": "priority",
                                "value": "Medium",
                                "style": "compact",
                                "choices": [
                                    {"title": "🔴 High", "value": "High"},
                                    {"title": "🟡 Medium", "value": "Medium"},
                                    {"title": "🟢 Low", "value": "Low"}
                                ]
                            }
                        ]
                    },
                    {
                        "type": "Column",
                        "width": "stretch",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "Category",
                                "weight": "Bolder",
                                "size": "Small"
                            },
                            {
                                "type": "Input.ChoiceSet",
                                "id": "category",
                                "value": "General",
                                "style": "compact",
                                "choices": [
                                    {"title": "🐛 Bug", "value": "Bug"},
                                    {"title": "✨ Feature", "value": "Feature"},
                                    {"title": "❓ General", "value": "General"},
                                    {"title": "🔒 Security", "value": "Security"}
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "TextBlock",
                "text": "Assign To",
                "weight": "Bolder",
                "size": "Small",
                "spacing": "Small"
            },
            {
                "type": "Input.Text",
                "id": "assignee",
                "placeholder": "Name or email"
            }
        ],
        "actions": [
    {
        "type": "Action.Submit",
        "id": "create_ticket_submit",
        "title": "✅ Create Ticket",
        "style": "positive",
        "data": {
            "action": "create_ticket_submit"
        }
    },
    {
        "type": "Action.Submit",
        "id": "back_to_board",
        "title": "← Back to Board",
        "data": {
            "action": "view_board"
        }
    }
]
    }