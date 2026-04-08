def ticket_updated_card(ticket, update_type="updated"):
    PRIORITY_ICONS = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
    STATUS_ICONS = {"Open": "🔵", "In Progress": "🟠", "Closed": "✅"}
    STATUS_COLORS = {"Open": "accent", "In Progress": "warning", "Closed": "good"}

    s_icon = STATUS_ICONS.get(ticket.status, "❓")
    s_color = STATUS_COLORS.get(ticket.status, "default")
    p_icon = PRIORITY_ICONS.get(ticket.priority, "⚪")

    if update_type == "status":
        headline = f"Status Updated → {ticket.status}"
        emoji = "🔄"
    elif update_type == "assigned":
        headline = f"Ticket Reassigned → {ticket.assignee}"
        emoji = "👤"
    elif update_type == "deleted":
        headline = "Ticket Deleted"
        emoji = "🗑️"
    else:
        headline = "Ticket Updated"
        emoji = "✏️"

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
                                "text": emoji,
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
                                "text": headline,
                                "weight": "Bolder",
                                "size": "Medium",
                                "color": "Good",
                                "wrap": True
                            },
                            {
                                "type": "TextBlock",
                                "text": ticket.title,
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
                "type": "FactSet",
                "spacing": "Small",
                "facts": [
                    {"title": "Ticket ID", "value": ticket.id},
                    {"title": "Status", "value": f"{s_icon} {ticket.status}"},
                    {"title": "Priority", "value": f"{p_icon} {ticket.priority}"},
                    {"title": "Assigned To", "value": ticket.assignee}
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
            }
        ]
    }