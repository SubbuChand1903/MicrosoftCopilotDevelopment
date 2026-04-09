def create_ticket_form():
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
                                        "text": "🎫",
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
                                        "text": "Create New Ticket",
                                        "weight": "Bolder",
                                        "size": "Medium",
                                        "wrap": True
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": "Fill in the details to submit a new ticket",
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
                        "text": "TICKET DETAILS",
                        "size": "Small",
                        "weight": "Bolder",
                        "color": "Accent",
                        "spacing": "None"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Title *",
                        "weight": "Bolder",
                        "size": "Small",
                        "spacing": "Small"
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
                    }
                ]
            },
            {
                "type": "Container",
                "style": "emphasis",
                "spacing": "Small",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": "CLASSIFICATION",
                        "size": "Small",
                        "weight": "Bolder",
                        "color": "Accent",
                        "spacing": "None"
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
                    }
                ]
            },
            {
                "type": "Container",
                "spacing": "Small",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": "ASSIGNMENT",
                        "size": "Small",
                        "weight": "Bolder",
                        "color": "Accent",
                        "spacing": "None"
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
                        "placeholder": "Name or email address"
                    }
                ]
            }
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "id": "create_ticket_submit",
                "title": "✅ Create Ticket",
                "style": "positive",
                "data": {"action": "create_ticket_submit"}
            },
            {
                "type": "Action.Submit",
                "id": "back_to_board",
                "title": "← Back to Board",
                "data": {"action": "view_board"}
            }
        ]
    }