from services.ticket_service import get_all_tickets

PRIORITY_COLORS = {"High": "attention", "Medium": "warning", "Low": "good"}
STATUS_COLORS = {"Open": "accent", "In Progress": "warning", "Closed": "good"}
PRIORITY_ICONS = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
STATUS_ICONS = {"Open": "🔵", "In Progress": "🟠", "Closed": "✅"}


def ticket_board_card(filter_status=None, filter_priority=None, filter_assignee=None):
    all_tickets = get_all_tickets()

    tickets = all_tickets
    if filter_status:
        tickets = [t for t in tickets if t.status.lower() == filter_status.lower()]
    if filter_priority:
        tickets = [t for t in tickets if t.priority.lower() == filter_priority.lower()]
    if filter_assignee:
        tickets = [t for t in tickets if filter_assignee.lower() in (t.assignee or "").lower()]

    open_count = len([t for t in all_tickets if t.status == "Open"])
    inprogress_count = len([t for t in all_tickets if t.status == "In Progress"])
    closed_count = len([t for t in all_tickets if t.status == "Closed"])
    total = len(all_tickets)

    # ---------- EMPTY STATE ----------
    if not tickets:
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
                                    "items": [{"type": "TextBlock", "text": "🎫", "size": "Large"}]
                                },
                                {
                                    "type": "Column",
                                    "width": "stretch",
                                    "verticalContentAlignment": "Center",
                                    "items": [
                                        {
                                            "type": "TextBlock",
                                            "text": "SwiftDesk AI",
                                            "weight": "Bolder",
                                            "size": "Medium",
                                            "wrap": True
                                        },
                                        {
                                            "type": "TextBlock",
                                            "text": "Enterprise Ticket Workspace",
                                            "size": "Small",
                                            "isSubtle": True,
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
                    "spacing": "Medium",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": "NO TICKETS FOUND",
                            "size": "Small",
                            "weight": "Bolder",
                            "color": "Accent",
                            "spacing": "None"
                        },
                        {
                            "type": "TextBlock",
                            "text": "Try another filter or create a new ticket.",
                            "isSubtle": True,
                            "wrap": True,
                            "spacing": "Small"
                        }
                    ]
                }
            ],
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "➕ Create Ticket",
                    "style": "positive",
                    "data": {"action": "show_create_form"}
                },
                {
                    "type": "Action.Submit",
                    "title": "🔄 Refresh Board",
                    "data": {"action": "view_board"}
                }
            ]
        }

    # ---------- HELPERS ----------
    def stat_chip(label, value, color):
        return {
            "type": "Column",
            "width": "stretch",
            "items": [
                {
                    "type": "Container",
                    "style": "emphasis",
                    "items": [
                        {
                            "type": "TextBlock",
                            "text": str(value),
                            "weight": "Bolder",
                            "size": "Large",
                            "color": color,
                            "horizontalAlignment": "Center"
                        },
                        {
                            "type": "TextBlock",
                            "text": label,
                            "size": "Small",
                            "isSubtle": True,
                            "horizontalAlignment": "Center",
                            "spacing": "None"
                        }
                    ]
                }
            ]
        }

    def quick_action_set(ticket_id):
        return {
            "type": "ActionSet",
            "spacing": "Small",
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "Open",
                    "data": {"action": "open_ticket", "ticket_id": ticket_id}
                },
                {
                    "type": "Action.Submit",
                    "title": "Comment",
                    "data": {"action": "show_add_comment_form", "ticket_id": ticket_id}
                }
            ]
        }

    def make_row(t):
        p_icon = PRIORITY_ICONS.get(t.priority, "⚪")
        p_color = PRIORITY_COLORS.get(t.priority, "default")
        s_icon = STATUS_ICONS.get(t.status, "❓")
        s_color = STATUS_COLORS.get(t.status, "default")
        created = t.created_at.strftime("%b %d") if hasattr(t.created_at, "strftime") else str(t.created_at)[:10]

        return {
            "type": "Container",
            "style": "emphasis",
            "spacing": "Small",
            "selectAction": {
                "type": "Action.Submit",
                "data": {"action": "open_ticket", "ticket_id": t.id}
            },
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
                                    "text": t.title,
                                    "weight": "Bolder",
                                    "size": "Small",
                                    "wrap": True
                                },
                                {
                                    "type": "TextBlock",
                                    "text": (t.description[:110] + ("..." if len(t.description) > 110 else ""))
                                    if t.description else "No description provided.",
                                    "isSubtle": True,
                                    "size": "Small",
                                    "wrap": True,
                                    "spacing": "Small"
                                },
                                {
                                    "type": "ColumnSet",
                                    "spacing": "Small",
                                    "columns": [
                                        {
                                            "type": "Column",
                                            "width": "auto",
                                            "items": [{"type": "TextBlock", "text": f"{p_icon} {t.priority}", "color": p_color, "size": "Small", "weight": "Bolder"}]
                                        },
                                        {
                                            "type": "Column",
                                            "width": "auto",
                                            "items": [{"type": "TextBlock", "text": "•", "isSubtle": True, "size": "Small"}]
                                        },
                                        {
                                            "type": "Column",
                                            "width": "auto",
                                            "items": [{"type": "TextBlock", "text": f"{s_icon} {t.status}", "color": s_color, "size": "Small", "weight": "Bolder"}]
                                        },
                                        {
                                            "type": "Column",
                                            "width": "auto",
                                            "items": [{"type": "TextBlock", "text": "•", "isSubtle": True, "size": "Small"}]
                                        },
                                        {
                                            "type": "Column",
                                            "width": "auto",
                                            "items": [{"type": "TextBlock", "text": f"👤 {t.assignee or 'Unassigned'}", "isSubtle": True, "size": "Small"}]
                                        },
                                        {
                                            "type": "Column",
                                            "width": "auto",
                                            "items": [{"type": "TextBlock", "text": "•", "isSubtle": True, "size": "Small"}]
                                        },
                                        {
                                            "type": "Column",
                                            "width": "auto",
                                            "items": [{"type": "TextBlock", "text": created, "isSubtle": True, "size": "Small"}]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "verticalContentAlignment": "Top",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": t.id,
                                    "size": "Small",
                                    "color": "Accent",
                                    "weight": "Bolder",
                                    "horizontalAlignment": "Right"
                                }
                            ]
                        }
                    ]
                },
                quick_action_set(t.id)
            ]
        }

    # ---------- MAIN BODY ----------
    body = [
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
                            "items": [{"type": "TextBlock", "text": "🎫", "size": "Large"}]
                        },
                        {
                            "type": "Column",
                            "width": "stretch",
                            "verticalContentAlignment": "Center",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": "SwiftDesk AI",
                                    "weight": "Bolder",
                                    "size": "Medium",
                                    "wrap": True
                                },
                                {
                                    "type": "TextBlock",
                                    "text": "Enterprise Ticket Workspace",
                                    "size": "Small",
                                    "isSubtle": True,
                                    "spacing": "None"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "verticalContentAlignment": "Center",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "text": f"{len(tickets)} shown / {total} total",
                                    "size": "Small",
                                    "isSubtle": True,
                                    "horizontalAlignment": "Right"
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        {
            "type": "ActionSet",
            "spacing": "Medium",
            "actions": [
                {
                    "type": "Action.Submit",
                    "title": "➕ Create Ticket",
                    "style": "positive",
                    "data": {"action": "show_create_form"}
                },
                {
                    "type": "Action.Submit",
                    "title": "🔄 Refresh",
                    "data": {"action": "view_board"}
                },
                {
                    "type": "Action.Submit",
                    "title": "🟠 In Progress",
                    "data": {"action": "filter_board", "status": "In Progress"}
                }
            ]
        },
        {
            "type": "TextBlock",
            "text": "TICKET OVERVIEW",
            "size": "Small",
            "weight": "Bolder",
            "color": "Accent",
            "spacing": "Medium"
        },
        {
            "type": "ColumnSet",
            "spacing": "Small",
            "columns": [
                stat_chip("Open", open_count, "Accent"),
                stat_chip("In Progress", inprogress_count, "Warning"),
                stat_chip("Closed", closed_count, "Good"),
            ]
        },
        {
            "type": "TextBlock",
            "text": "ALL TICKETS",
            "size": "Small",
            "weight": "Bolder",
            "color": "Accent",
            "spacing": "Medium"
        },
        {"type": "Separator", "spacing": "Small"}
    ]

    for t in tickets[:8]:
        body.append(make_row(t))

    if len(tickets) > 8:
        body.append({
            "type": "TextBlock",
            "text": f"Showing first 8 of {len(tickets)} tickets.",
            "isSubtle": True,
            "size": "Small",
            "spacing": "Medium"
        })

    return {
        "type": "AdaptiveCard",
        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.5",
        "body": body
    }