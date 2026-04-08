import re
from services.ticket_service import (
    get_all_tickets, get_ticket, create_ticket,
    update_ticket, delete_ticket, add_comment, get_comments
)

LAST_CREATED_TICKET_ID = None


def extract_ticket_id(text):
    match = re.search(r'TCKT-[A-F0-9]{6}', text, re.IGNORECASE)
    return match.group(0).upper() if match else None


def handle_workflow(query):
    global LAST_CREATED_TICKET_ID

    # --------------------------------------------------
    # STEP 1: Normalize {"text": "..."} into actions
    # --------------------------------------------------
    if isinstance(query, dict) and "text" in query and "action" not in query:
        q = query["text"].strip()
        ql = q.lower()
        ticket_id = extract_ticket_id(q)

        # Button / text-driven commands
        if ticket_id and any(w in ql for w in ["open", "view", "show", "details", "detail"]):
            query = {"action": "view_ticket", "ticket_id": ticket_id}

        elif any(p in ql for p in ["create ticket", "new ticket", "add ticket", "raise ticket"]):
            query = {"action": "show_create_form"}

        elif any(
            p in ql
            for p in [
                "show all tickets",
                "show tickets",
                "list tickets",
                "view board",
                "back to dashboard",
                "back to board",
                "refresh"
            ]
        ):
            query = {"action": "view_board"}

        elif "in progress" in ql and "ticket" not in ql:
            query = {"action": "filter_board", "status": "In Progress"}

        elif "closed" in ql and "ticket" not in ql:
            query = {"action": "filter_board", "status": "Closed"}

        elif "open tickets" in ql:
            query = {"action": "filter_board", "status": "Open"}

        else:
            # Keep it as text payload for later NL routing
            query = {"text": q}

    # --------------------------------------------------
    # STEP 2: STRUCTURED ACTION PAYLOADS
    # --------------------------------------------------
    if isinstance(query, dict) and "action" in query:
        action = query.get("action")

        if action in ("view_board", "back_to_board"):
            from cards.ticket_board import ticket_board_card
            return ticket_board_card()

        if action == "filter_board":
            from cards.ticket_board import ticket_board_card
            return ticket_board_card(
                filter_status=query.get("status"),
                filter_priority=query.get("priority"),
                filter_assignee=query.get("assignee")
            )

        if action == "show_create_form":
            from cards.create_ticket import create_ticket_form
            return create_ticket_form()

        if action == "create_ticket":
            ticket = create_ticket(
                title=query.get("title", "Untitled"),
                description=query.get("description", ""),
                priority=query.get("priority", "Medium"),
                assignee=query.get("assignee", "Unassigned"),
                category=query.get("category", "General")
            )
            LAST_CREATED_TICKET_ID = ticket.id
            from cards.ticket_created import ticket_created_card
            return ticket_created_card(ticket)

        if action in ("view_ticket", "open_ticket"):
            from cards.ticket_detail import ticket_detail_card
            return ticket_detail_card(query.get("ticket_id"))

        if action == "show_add_comment_form":
            from cards.add_comment import add_comment_card
            return add_comment_card(query.get("ticket_id"))

        if action == "update_status":
            ticket = update_ticket(query.get("ticket_id"), status=query.get("status"))
            if ticket:
                from cards.ticket_updated import ticket_updated_card
                return ticket_updated_card(ticket, update_type="status")
            from cards.ticket_board import ticket_board_card
            return ticket_board_card()

        if action == "assign_ticket":
            ticket = update_ticket(query.get("ticket_id"), assignee=query.get("assignee"))
            if ticket:
                from cards.ticket_updated import ticket_updated_card
                return ticket_updated_card(ticket, update_type="assigned")
            from cards.ticket_board import ticket_board_card
            return ticket_board_card()

        if action == "delete_ticket":
            delete_ticket(query.get("ticket_id"))
            from cards.ticket_board import ticket_board_card
            return ticket_board_card()

        if action in ("add_comment", "submit_comment"):
            ticket_id = query.get("ticket_id")
            author = query.get("author", "User")
            text = query.get("comment", query.get("text", ""))

            add_comment(ticket_id=ticket_id, text=text, author=author)

            from cards.comment_added import comment_added_card
            return comment_added_card(ticket_id, author, text)

    # --------------------------------------------------
    # STEP 3: NATURAL LANGUAGE
    # --------------------------------------------------
    if isinstance(query, str):
        q = query.strip()
        ql = q.lower()

        ticket_id = extract_ticket_id(q)

        # FOLLOW-UP REFERENCE TO LAST CREATED TICKET
        if any(phrase in ql for phrase in [
            "created above",
            "created earlier",
            "created just now",
            "that was created above",
            "ticket above",
            "the above ticket"
        ]):
            if LAST_CREATED_TICKET_ID:
                from cards.ticket_detail import ticket_detail_card
                return ticket_detail_card(LAST_CREATED_TICKET_ID)

            from cards.ticket_board import ticket_board_card
            return ticket_board_card()

        # VIEW SPECIFIC TICKET
        if ticket_id and any(w in ql for w in ["show", "view", "open", "get", "detail", "display", "fetch"]):
            from cards.ticket_detail import ticket_detail_card
            return ticket_detail_card(ticket_id)

        # UPDATE STATUS
        if ticket_id and any(w in ql for w in ["close", "closed", "resolve", "resolved", "complete", "done"]):
            ticket = update_ticket(ticket_id, status="Closed")
            from cards.ticket_updated import ticket_updated_card
            return ticket_updated_card(ticket, update_type="status")

        if ticket_id and ("in progress" in ql or "start" in ql or "begin" in ql or "working" in ql):
            ticket = update_ticket(ticket_id, status="In Progress")
            from cards.ticket_updated import ticket_updated_card
            return ticket_updated_card(ticket, update_type="status")

        if ticket_id and ("reopen" in ql or "open" in ql) and "status" in ql:
            ticket = update_ticket(ticket_id, status="Open")
            from cards.ticket_updated import ticket_updated_card
            return ticket_updated_card(ticket, update_type="status")

        if any(w in ql for w in ["update status", "change status", "mark as", "set status"]):
            if ticket_id:
                if "close" in ql or "closed" in ql:
                    status = "Closed"
                elif "progress" in ql:
                    status = "In Progress"
                else:
                    status = "Open"

                ticket = update_ticket(ticket_id, status=status)
                from cards.ticket_updated import ticket_updated_card
                return ticket_updated_card(ticket, update_type="status")

        # ASSIGN TICKET
        if ticket_id and ("assign" in ql or "reassign" in ql):
            assign_match = re.search(
                r'(?:assign(?:ed)?(?:\s+the\s+ticket)?|reassign|update(?:\s+the\s+ticket)?\s+assignee|change\s+assignee|set\s+assignee)\s+(?:ticket\s+)?(?:TCKT-[A-F0-9]{6}\s+)?to\s+([A-Za-z\s@.]+?)(?:\s*$|\.|,)',
                q,
                re.IGNORECASE
            )
            if assign_match:
                assignee = assign_match.group(1).strip()
                ticket = update_ticket(ticket_id, assignee=assignee)
                from cards.ticket_updated import ticket_updated_card
                return ticket_updated_card(ticket, update_type="assigned")

        # DELETE TICKET
        if ticket_id and any(w in ql for w in ["delete", "remove", "cancel", "discard"]):
            delete_ticket(ticket_id)
            from cards.ticket_board import ticket_board_card
            return ticket_board_card()

        # ADD COMMENT
        if ticket_id and any(w in ql for w in ["comment", "note", "add note", "add comment"]):
            comment_match = re.search(r'(?:comment|note)[:\s]+(.+)', q, re.IGNORECASE)
            if comment_match:
                comment_text = comment_match.group(1).strip()
                add_comment(ticket_id=ticket_id, text=comment_text, author="User")

                from cards.comment_added import comment_added_card
                return comment_added_card(ticket_id, "User", comment_text)

        # CREATE TICKET
        create_intent = re.search(
            r'(\b(create|new|add|open|raise|log|submit)\b.*\bticket\b)|(\bticket\b.*\b(create|new|add|open|raise|log|submit)\b)',
            ql,
            re.IGNORECASE
        )

        if create_intent:
            has_details = any([
                "for " in ql,
                "about " in ql,
                "assign" in ql,
                "priority" in ql,
                "high" in ql,
                "low" in ql,
                "bug" in ql,
                "feature" in ql,
                "issue" in ql
            ])

            if not has_details:
                from cards.create_ticket import create_ticket_form
                return create_ticket_form()

            title = q
            priority = "Medium"
            assignee = "Unassigned"
            category = "General"
            description = ""

            title_match = re.search(
                r'(?:for|about|titled?|called?|:)\s+["\']?(.+?)["\']?(?:\s+(?:with|for|assign|priority|$))',
                q,
                re.IGNORECASE
            )
            if title_match:
                title = title_match.group(1).strip()

            if "high" in ql:
                priority = "High"
            elif "low" in ql:
                priority = "Low"
            elif "medium" in ql or "mid" in ql:
                priority = "Medium"

            if "bug" in ql:
                category = "Bug"
            elif "feature" in ql:
                category = "Feature"
            elif "security" in ql:
                category = "Security"

            assign_match = re.search(
                r'assign(?:ed)? to\s+([A-Za-z\s@.]+?)(?:\s*$|\.|\,)',
                q,
                re.IGNORECASE
            )
            if assign_match:
                assignee = assign_match.group(1).strip()

            desc_match = re.search(
                r'description[:\s]+(.+?)(?:\s+priority|\s+assign|$)',
                q,
                re.IGNORECASE
            )
            if desc_match:
                description = desc_match.group(1).strip()
            else:
                description = q

            ticket = create_ticket(
                title=title,
                description=description,
                priority=priority,
                assignee=assignee,
                category=category
            )

            LAST_CREATED_TICKET_ID = ticket.id

            from cards.ticket_created import ticket_created_card
            return ticket_created_card(ticket)

        # FILTERED BOARD VIEWS
        if any(w in ql for w in ["high priority", "critical", "urgent"]):
            from cards.ticket_board import ticket_board_card
            return ticket_board_card(filter_priority="High")

        if any(w in ql for w in ["in progress", "active", "ongoing"]):
            from cards.ticket_board import ticket_board_card
            return ticket_board_card(filter_status="In Progress")

        if "closed" in ql and "ticket" in ql:
            from cards.ticket_board import ticket_board_card
            return ticket_board_card(filter_status="Closed")

        if "open" in ql and "ticket" in ql:
            from cards.ticket_board import ticket_board_card
            return ticket_board_card(filter_status="Open")

        assign_filter = re.search(
            r'(?:assigned to|tickets for|tickets by)\s+([A-Za-z\s@.]+?)(?:\s*$|\.)',
            q,
            re.IGNORECASE
        )
        if assign_filter:
            from cards.ticket_board import ticket_board_card
            return ticket_board_card(filter_assignee=assign_filter.group(1).strip())

        # SHOW ALL TICKETS / BOARD
        if any(w in ql for w in ["board", "all ticket", "my ticket", "show ticket", "list ticket", "view ticket", "get ticket", "fetch ticket"]):
            from cards.ticket_board import ticket_board_card
            return ticket_board_card()

    # --------------------------------------------------
    # STEP 4: NATURAL LANGUAGE FROM {"text": "..."} THAT DID NOT NORMALIZE
    # --------------------------------------------------
    if isinstance(query, dict) and "text" in query:
        q = query["text"].strip()
        ql = q.lower()

        ticket_id = extract_ticket_id(q)

        # FOLLOW-UP REFERENCE TO LAST CREATED TICKET
        if any(phrase in ql for phrase in [
            "created above",
            "created earlier",
            "created just now",
            "that was created above",
            "ticket above",
            "the above ticket"
        ]):
            if LAST_CREATED_TICKET_ID:
                from cards.ticket_detail import ticket_detail_card
                return ticket_detail_card(LAST_CREATED_TICKET_ID)

            from cards.ticket_board import ticket_board_card
            return ticket_board_card()

        # VIEW SPECIFIC TICKET
        if ticket_id and any(w in ql for w in ["show", "view", "open", "get", "detail", "display", "fetch"]):
            from cards.ticket_detail import ticket_detail_card
            return ticket_detail_card(ticket_id)

        # UPDATE STATUS
        if ticket_id and any(w in ql for w in ["close", "closed", "resolve", "resolved", "complete", "done"]):
            ticket = update_ticket(ticket_id, status="Closed")
            from cards.ticket_updated import ticket_updated_card
            return ticket_updated_card(ticket, update_type="status")

        if ticket_id and ("in progress" in ql or "start" in ql or "begin" in ql or "working" in ql):
            ticket = update_ticket(ticket_id, status="In Progress")
            from cards.ticket_updated import ticket_updated_card
            return ticket_updated_card(ticket, update_type="status")

        if ticket_id and ("reopen" in ql or "open" in ql) and "status" in ql:
            ticket = update_ticket(ticket_id, status="Open")
            from cards.ticket_updated import ticket_updated_card
            return ticket_updated_card(ticket, update_type="status")

        if any(w in ql for w in ["update status", "change status", "mark as", "set status"]):
            if ticket_id:
                if "close" in ql or "closed" in ql:
                    status = "Closed"
                elif "progress" in ql:
                    status = "In Progress"
                else:
                    status = "Open"

                ticket = update_ticket(ticket_id, status=status)
                from cards.ticket_updated import ticket_updated_card
                return ticket_updated_card(ticket, update_type="status")

        # ASSIGN TICKET
        if ticket_id and ("assign" in ql or "reassign" in ql):
            assign_match = re.search(
                r'(?:assign(?:ed)?(?:\s+the\s+ticket)?|reassign|update(?:\s+the\s+ticket)?\s+assignee|change\s+assignee|set\s+assignee)\s+(?:ticket\s+)?(?:TCKT-[A-F0-9]{6}\s+)?to\s+([A-Za-z\s@.]+?)(?:\s*$|\.|,)',
                q,
                re.IGNORECASE
            )
            if assign_match:
                assignee = assign_match.group(1).strip()
                ticket = update_ticket(ticket_id, assignee=assignee)
                from cards.ticket_updated import ticket_updated_card
                return ticket_updated_card(ticket, update_type="assigned")

        # DELETE TICKET
        if ticket_id and any(w in ql for w in ["delete", "remove", "cancel", "discard"]):
            delete_ticket(ticket_id)
            from cards.ticket_board import ticket_board_card
            return ticket_board_card()

        # ADD COMMENT
        if ticket_id and any(w in ql for w in ["comment", "note", "add note", "add comment"]):
            comment_match = re.search(r'(?:comment|note)[:\s]+(.+)', q, re.IGNORECASE)
            if comment_match:
                comment_text = comment_match.group(1).strip()
                add_comment(ticket_id=ticket_id, text=comment_text, author="User")

                from cards.comment_added import comment_added_card
                return comment_added_card(ticket_id, "User", comment_text)

        # CREATE TICKET
        create_intent = re.search(
            r'(\b(create|new|add|open|raise|log|submit)\b.*\bticket\b)|(\bticket\b.*\b(create|new|add|open|raise|log|submit)\b)',
            ql,
            re.IGNORECASE
        )

        if create_intent:
            has_details = any([
                "for " in ql,
                "about " in ql,
                "assign" in ql,
                "priority" in ql,
                "high" in ql,
                "low" in ql,
                "bug" in ql,
                "feature" in ql,
                "issue" in ql
            ])

            if not has_details:
                from cards.create_ticket import create_ticket_form
                return create_ticket_form()

            title = q
            priority = "Medium"
            assignee = "Unassigned"
            category = "General"
            description = ""

            title_match = re.search(
                r'(?:for|about|titled?|called?|:)\s+["\']?(.+?)["\']?(?:\s+(?:with|for|assign|priority|$))',
                q,
                re.IGNORECASE
            )
            if title_match:
                title = title_match.group(1).strip()

            if "high" in ql:
                priority = "High"
            elif "low" in ql:
                priority = "Low"
            elif "medium" in ql or "mid" in ql:
                priority = "Medium"

            if "bug" in ql:
                category = "Bug"
            elif "feature" in ql:
                category = "Feature"
            elif "security" in ql:
                category = "Security"

            assign_match = re.search(
                r'assign(?:ed)? to\s+([A-Za-z\s@.]+?)(?:\s*$|\.|\,)',
                q,
                re.IGNORECASE
            )
            if assign_match:
                assignee = assign_match.group(1).strip()

            desc_match = re.search(
                r'description[:\s]+(.+?)(?:\s+priority|\s+assign|$)',
                q,
                re.IGNORECASE
            )
            if desc_match:
                description = desc_match.group(1).strip()
            else:
                description = q

            ticket = create_ticket(
                title=title,
                description=description,
                priority=priority,
                assignee=assignee,
                category=category
            )

            LAST_CREATED_TICKET_ID = ticket.id

            from cards.ticket_created import ticket_created_card
            return ticket_created_card(ticket)

        # FILTERED BOARD VIEWS
        if any(w in ql for w in ["high priority", "critical", "urgent"]):
            from cards.ticket_board import ticket_board_card
            return ticket_board_card(filter_priority="High")

        if any(w in ql for w in ["in progress", "active", "ongoing"]):
            from cards.ticket_board import ticket_board_card
            return ticket_board_card(filter_status="In Progress")

        if "closed" in ql and "ticket" in ql:
            from cards.ticket_board import ticket_board_card
            return ticket_board_card(filter_status="Closed")

        if "open" in ql and "ticket" in ql:
            from cards.ticket_board import ticket_board_card
            return ticket_board_card(filter_status="Open")

        assign_filter = re.search(
            r'(?:assigned to|tickets for|tickets by)\s+([A-Za-z\s@.]+?)(?:\s*$|\.)',
            q,
            re.IGNORECASE
        )
        if assign_filter:
            from cards.ticket_board import ticket_board_card
            return ticket_board_card(filter_assignee=assign_filter.group(1).strip())

        # SHOW ALL TICKETS / BOARD
        if any(w in ql for w in ["board", "all ticket", "my ticket", "show ticket", "list ticket", "view ticket", "get ticket", "fetch ticket"]):
            from cards.ticket_board import ticket_board_card
            return ticket_board_card()

    # --------------------------------------------------
    # DEFAULT
    # --------------------------------------------------
    from cards.ticket_board import ticket_board_card
    return ticket_board_card()