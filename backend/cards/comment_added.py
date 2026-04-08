def comment_added_card(ticket_id, author, comment_text):
    return {
        "type": "AdaptiveCard",
        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
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
                                "text": "💬",
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
                                "text": "Comment Added",
                                "weight": "Bolder",
                                "size": "Medium",
                                "color": "Accent"
                            },
                            {
                                "type": "TextBlock",
                                "text": f"Ticket {ticket_id} has been updated successfully.",
                                "isSubtle": True,
                                "size": "Small",
                                "spacing": "None",
                                "wrap": True
                            }
                        ]
                    }
                ]
            },
            {"type": "Separator"},
            {
                "type": "Container",
                "style": "emphasis",
                "spacing": "Small",
                "items": [
                    {
                        "type": "TextBlock",
                        "text": f"👤 {author}",
                        "weight": "Bolder",
                        "size": "Small"
                    },
                    {
                        "type": "TextBlock",
                        "text": comment_text,
                        "wrap": True,
                        "size": "Small",
                        "isSubtle": True,
                        "spacing": "Small"
                    }
                ]
            }
        ],
        "actions": [
            {
                "type": "Action.Submit",
                "title": "🔍 View Ticket",
                "verb": "view_ticket",
                "data": {
                    "action": "view_ticket",
                    "ticket_id": ticket_id
                }
            },
            {
                "type": "Action.Submit",
                "title": "💬 Add Another Comment",
                "verb": "show_add_comment_form",
                "data": {
                    "action": "show_add_comment_form",
                    "ticket_id": ticket_id
                }
            },
            {
                "type": "Action.Submit",
                "title": "📋 Back to Board",
                "verb": "view_board",
                "data": {
                    "action": "view_board"
                }
            }
        ]
    }