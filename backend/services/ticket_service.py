from models.database import SessionLocal, Ticket, Comment
from datetime import datetime

def get_all_tickets():
    db = SessionLocal()
    tickets = db.query(Ticket).order_by(Ticket.created_at.desc()).all()
    db.close()
    return tickets

def get_ticket(ticket_id):
    db = SessionLocal()
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    db.close()
    return ticket

def create_ticket(title, description="", priority="Medium", assignee="Unassigned", category="General"):
    db = SessionLocal()
    ticket = Ticket(
        title=title,
        description=description,
        priority=priority,
        assignee=assignee,
        category=category
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    db.close()
    return ticket

def update_ticket(ticket_id, **kwargs):
    db = SessionLocal()
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket:
        for k, v in kwargs.items():
            setattr(ticket, k, v)
        ticket.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(ticket)
    db.close()
    return ticket

def delete_ticket(ticket_id):
    db = SessionLocal()
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if ticket:
        db.delete(ticket)
        db.commit()
    db.close()

def add_comment(ticket_id, text, author="User"):
    db = SessionLocal()
    comment = Comment(ticket_id=ticket_id, text=text, author=author)
    db.add(comment)
    db.commit()
    db.close()

def get_comments(ticket_id):
    db = SessionLocal()
    comments = db.query(Comment).filter(
        Comment.ticket_id == ticket_id
    ).order_by(Comment.created_at.asc()).all()
    db.close()
    return comments