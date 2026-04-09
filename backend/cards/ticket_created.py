def ticket_created_card(ticket):
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
                                    {"type": "TextBlock", "text": "✅", "size": "Large"}
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
                                        "wrap": True
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": "Your ticket is ready for next actions",
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
                    }
                ]
            },
            {
                "type": "Container",
                "style": "emphasis",
                "spacing": "Small",
                "items": [
                    {
                        "type": "ColumnSet",
                        "columns": [
                            {
                                "type": "Column",
                                "width": "stretch",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": str(ticket.title),
                                        "weight": "Bolder",
                                        "size": "Medium",
                                        "wrap": True
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": str(ticket.id),
                                        "color": "Accent",
                                        "size": "Small",
                                        "weight": "Bolder",
                                        "spacing": "None"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "type": "Container",
                "style": "emphasis",
                "spacing": "Small",
                "items": [
                    {
                        "type": "FactSet",
                        "facts": [
                            {"title": "Priority", "value": str(ticket.priority)},
                            {"title": "Category", "value": str(ticket.category)},
                            {"title": "Assigned To", "value": str(ticket.assignee) or "Unassigned"},
                            {"title": "Status", "value": str(ticket.status)}
                        ]
                    }
                ]
            }
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "title": "🔍 View Ticket",
                "style": "positive",
                "data": {"action": "view_ticket", "ticket_id": ticket.id}
            },
            {
                "type": "Action.Submit",
                "title": "💬 Add Comment",
                "data": {"action": "show_add_comment_form", "ticket_id": ticket.id}
            },
            {
                "type": "Action.Submit",
                "title": "📋 Back to Board",
                "data": {"action": "view_board"}
            },
            {
                "type": "Action.Submit",
                "title": "➕ Create Another",
                "data": {"action": "show_create_form"}
            }
        ]
    }