def ticket_created_card(ticket):
    return {
        "type": "AdaptiveCard",
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.5",
        "body": [
            {
                "type": "Container",
                "style": "emphasis",
                "bleed": True,
                "items": [
                    {
                        "type": "TextBlock",
                        "text": "ServiceDesk AI",
                        "weight": "Bolder",
                        "size": "Large",
                        "color": "Accent"
                    },
                    {
                        "type": "TextBlock",
                        "text": "Enterprise Ticket Workspace",
                        "isSubtle": True,
                        "size": "Small",
                        "spacing": "None"
                    }
                ]
            },
            {
                "type": "ColumnSet",
                "spacing": "Medium",
                "columns": [
                    {
                        "type": "Column",
                        "width": "auto",
                        "items": [
                            {
                                "type": "TextBlock",
                                "text": "✅",
                                "size": "ExtraLarge"
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
                                "text": "Ticket Created Successfully",
                                "weight": "Bolder",
                                "size": "Medium",
                                "color": "Good"
                            },
                            {
                                "type": "TextBlock",
                                "text": "Your ticket has been created and is ready for next actions.",
                                "isSubtle": True,
                                "size": "Small",
                                "wrap": True,
                                "spacing": "None"
                            }
                        ]
                    }
                ]
            },
            {"type": "Separator"},
            {
                "type": "FactSet",
                "spacing": "Small",
                "facts": [
    {"title": "Ticket ID", "value": str(ticket.id)},
    {"title": "Title", "value": str(ticket.title)},
    {"title": "Priority", "value": str(ticket.priority)},
    {"title": "Category", "value": str(ticket.category)},
    {"title": "Assigned To", "value": str(ticket.assignee)},
    {"title": "Status", "value": str(ticket.status)}
]
            }
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "title": "🔍 View Ticket",
                "data": {
                    "action": "view_ticket",
                    "ticket_id": ticket.id
                }
            },
            {
                "type": "Action.Submit",
                "title": "💬 Add Comment",
                "data": {
                    "action": "show_add_comment_form",
                    "ticket_id": ticket.id
                }
            },
            {
                "type": "Action.Submit",
                "title": "📋 Back to Board",
                "data": {
                    "action": "view_board"
                }
            },
            {
                "type": "Action.Submit",
                "title": "➕ Create Another",
                "data": {
                    "action": "show_create_form"
                }
            }
        ]
    }