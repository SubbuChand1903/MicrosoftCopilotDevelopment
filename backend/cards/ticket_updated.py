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
            # --- HEADER ---
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
                                "items": [{"type": "TextBlock", "text": emoji, "size": "Large"}]
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
                                        "wrap": True
                                    },
                                    {
                                        "type": "TextBlock",
                                        "text": ticket.title,
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
            # --- TICKET SUMMARY ---
            {
                "type": "TextBlock",
                "text": "TICKET SUMMARY",
                "size": "Small",
                "weight": "Bolder",
                "color": "Accent",
                "spacing": "Medium"
            },
            {
                "type": "Container",
                "style": "emphasis",
                "spacing": "Small",
                "items": [
                    {
                        "type": "FactSet",
                        "facts": [
                            {"title": "Ticket ID", "value": str(ticket.id)},
                            {"title": "Status", "value": f"{s_icon} {ticket.status}"},
                            {"title": "Priority", "value": f"{p_icon} {ticket.priority}"},
                            {"title": "Assigned To", "value": str(ticket.assignee) or "Unassigned"}
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
            }
        ]
    }