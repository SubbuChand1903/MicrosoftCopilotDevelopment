from services.ticket_service import get_ticket, get_comments

PRIORITY_COLORS = {"High": "attention", "Medium": "warning", "Low": "good"}
STATUS_COLORS = {"Open": "accent", "In Progress": "warning", "Closed": "good"}
PRIORITY_ICONS = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
STATUS_ICONS = {"Open": "🔵", "In Progress": "🟠", "Closed": "✅"}


def ticket_detail_card(ticket_id):
    t = get_ticket(ticket_id)

    if not t:
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
                                        {"type": "TextBlock", "text": "SwiftDesk AI", "weight": "Bolder", "size": "Medium"},
                                        {"type": "TextBlock", "text": "Enterprise Ticket Workspace", "size": "Small", "isSubtle": True, "spacing": "None"}
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
                        {"type": "TextBlock", "text": "TICKET NOT FOUND", "size": "Small", "weight": "Bolder", "color": "Attention", "spacing": "None"},
                        {"type": "TextBlock", "text": f"Ticket {ticket_id} could not be found.", "isSubtle": True, "wrap": True, "spacing": "Small"}
                    ]
                }
            ],
            "actions": [
                {"type": "Action.Submit", "title": "← Back to Board", "data": {"action": "view_board"}}
            ]
        }

    comments = get_comments(ticket_id)

    p_icon = PRIORITY_ICONS.get(t.priority, "⚪")
    p_color = PRIORITY_COLORS.get(t.priority, "default")
    s_icon = STATUS_ICONS.get(t.status, "❓")
    s_color = STATUS_COLORS.get(t.status, "default")

    created = t.created_at.strftime("%b %d, %Y %H:%M") if hasattr(t.created_at, "strftime") else str(t.created_at)
    updated = t.updated_at.strftime("%b %d, %Y %H:%M") if hasattr(t.updated_at, "strftime") else str(t.updated_at)

    comment_items = []
    if comments:
        comment_items.append({
            "type": "TextBlock",
            "text": f"COMMENTS ({len(comments)})",
            "size": "Small",
            "weight": "Bolder",
            "color": "Accent",
            "spacing": "Medium"
        })
        comment_items.append({"type": "Separator", "spacing": "Small"})

        for c in comments[-4:]:
            c_time = c.created_at.strftime("%b %d, %H:%M") if hasattr(c.created_at, "strftime") else str(c.created_at)
            comment_items.append({
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
                                "items": [{"type": "TextBlock", "text": f"👤 {c.author}", "weight": "Bolder", "size": "Small"}]
                            },
                            {
                                "type": "Column",
                                "width": "auto",
                                "items": [{"type": "TextBlock", "text": c_time, "isSubtle": True, "size": "Small"}]
                            }
                        ]
                    },
                    {
                        "type": "TextBlock",
                        "text": c.text,
                        "wrap": True,
                        "size": "Small",
                        "isSubtle": True,
                        "spacing": "Small"
                    }
                ]
            })
    else:
        comment_items.append({
            "type": "TextBlock",
            "text": "COMMENTS",
            "size": "Small",
            "weight": "Bolder",
            "color": "Accent",
            "spacing": "Medium"
        })
        comment_items.append({"type": "Separator", "spacing": "Small"})
        comment_items.append({
            "type": "Container",
            "style": "emphasis",
            "spacing": "Small",
            "items": [
                {"type": "TextBlock", "text": "💬 No comments yet.", "isSubtle": True, "size": "Small"}
            ]
        })

    body = [
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
                            "items": [{"type": "TextBlock", "text": "🎫", "size": "Large"}]
                        },
                        {
                            "type": "Column",
                            "width": "stretch",
                            "verticalContentAlignment": "Center",
                            "items": [
                                {"type": "TextBlock", "text": "SwiftDesk AI", "weight": "Bolder", "size": "Medium", "wrap": True},
                                {"type": "TextBlock", "text": "Enterprise Ticket Workspace", "size": "Small", "isSubtle": True, "spacing": "None"}
                            ]
                        }
                    ]
                }
            ]
        },
        # --- NAV ACTIONS ---
        {
            "type": "ActionSet",
            "spacing": "Medium",
            "actions": [
                {"type": "Action.Submit", "title": "← Back", "data": {"action": "view_board"}},
                {"type": "Action.Submit", "title": "💬 Add Comment", "style": "positive", "data": {"action": "show_add_comment_form", "ticket_id": t.id}}
            ]
        },
        # --- TICKET TITLE + ID ---
        {
            "type": "Container",
            "spacing": "Small",
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
                                {"type": "TextBlock", "text": t.title, "weight": "Bolder", "size": "Medium", "wrap": True},
                                {"type": "TextBlock", "text": t.id, "color": "Accent", "weight": "Bolder", "size": "Small", "spacing": "None"}
                            ]
                        }
                    ]
                },
                {
                    "type": "ColumnSet",
                    "spacing": "Small",
                    "columns": [
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [{"type": "TextBlock", "text": f"{p_icon} {t.priority}", "color": p_color, "weight": "Bolder", "size": "Small"}]
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [{"type": "TextBlock", "text": "•", "isSubtle": True, "size": "Small"}]
                        },
                        {
                            "type": "Column",
                            "width": "auto",
                            "items": [{"type": "TextBlock", "text": f"{s_icon} {t.status}", "color": s_color, "weight": "Bolder", "size": "Small"}]
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
                        }
                    ]
                }
            ]
        },
        # --- STATUS ACTIONS ---
        {
            "type": "TextBlock",
            "text": "UPDATE STATUS",
            "size": "Small",
            "weight": "Bolder",
            "color": "Accent",
            "spacing": "Medium"
        },
        {
            "type": "ActionSet",
            "spacing": "Small",
            "actions": [
                {"type": "Action.Submit", "title": "🔵 Open", "data": {"action": "update_status", "ticket_id": t.id, "status": "Open"}},
                {"type": "Action.Submit", "title": "🟠 In Progress", "data": {"action": "update_status", "ticket_id": t.id, "status": "In Progress"}},
                {"type": "Action.Submit", "title": "✅ Closed", "data": {"action": "update_status", "ticket_id": t.id, "status": "Closed"}}
            ]
        },
        # --- META ---
        {
            "type": "TextBlock",
            "text": "METADATA",
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
                        {"title": "Category", "value": t.category},
                        {"title": "Created", "value": created},
                        {"title": "Last Updated", "value": updated}
                    ]
                }
            ]
        },
        # --- DESCRIPTION ---
        {
            "type": "TextBlock",
            "text": "DESCRIPTION",
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
                    "type": "TextBlock",
                    "text": t.description or "No description provided.",
                    "wrap": True,
                    "isSubtle": True,
                    "size": "Small"
                }
            ]
        },
        *comment_items
    ]

    return {
        "type": "AdaptiveCard",
        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.5",
        "body": body,
        "actions": [
            {
                "type": "Action.Submit",
                "title": "🗑 Delete Ticket",
                "data": {"action": "delete_ticket", "ticket_id": t.id}
            }
        ]
    }