def comment_added_card(ticket_id, author, comment_text):
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
                                        "text": "Comment Added",
                                        "weight": "Bolder",
                                        "size": "Medium",
                                        "wrap": True
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": f"Ticket {ticket_id} updated successfully",
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
                        "text": "COMMENT SUMMARY",
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
                                "width": "auto",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": "👤",
                                        "size": "Medium"
                                    }
                                ],
                                "verticalContentAlignment": "Center"
                            },
                            {
                                "type": "Column",
                                "width": "stretch",
                                "verticalContentAlignment": "Center",
                                "items": [
                                    {
                                        "type": "TextBlock",
                                        "text": author,
                                        "weight": "Bolder",
                                        "size": "Small",
                                        "spacing": "None"
                                    }
                                ]
                            }
                        ]
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
                "style": "positive",
                "data": {
                    "action": "view_ticket",
                    "ticket_id": ticket_id
                }
            },
            {
                "type": "Action.Submit",
                "title": "💬 Add Another Comment",
                "data": {
                    "action": "show_add_comment_form",
                    "ticket_id": ticket_id
                }
            },
            {
                "type": "Action.Submit",
                "title": "📋 Back to Board",
                "data": {
                    "action": "view_board"
                }
            }
        ]
    }