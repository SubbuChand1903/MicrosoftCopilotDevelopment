from fastapi import APIRouter
from models.request_models import GenerateUIRequest
from services.workflow_engine import handle_workflow
from cards.ticket_board import ticket_board_card
import json

router = APIRouter()


def fallback_card(message: str):
    return {
        "type": "AdaptiveCard",
        "$schema": "https://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.5",
        "body": [
            {
                "type": "TextBlock",
                "text": message,
                "weight": "Bolder",
                "color": "Attention",
                "wrap": True
            }
        ]
    }


@router.post("/generate-ui")
def generate_ui(req: GenerateUIRequest):
    query = req.query

    print("RAW TYPE:", type(query))
    print("RAW VALUE:", query)

    # Guard: Copilot sometimes sends back junk/system text
    if isinstance(query, str) and "[System:" in query:
        print("SYSTEM INJECTION DETECTED - returning board")
        return ticket_board_card()

    # Try parsing JSON only if input is string
    if isinstance(query, str):
        try:
            parsed = json.loads(query)
            query = parsed
            print("PARSED TO DICT:", query)
        except Exception as e:
            print("JSON parse failed:", e)

    # Normalize query before sending to workflow
    normalized_query = None

    if isinstance(query, dict):
        # Already structured payload
        normalized_query = query

    elif isinstance(query, str):
        # Natural language / imBack text / plain text input
        normalized_query = {
            "text": query.strip()
        }

    else:
        # Unknown format fallback
        normalized_query = {
            "text": str(query).strip()
        }

    print("NORMALIZED QUERY:", normalized_query)

    try:
        card = handle_workflow(normalized_query)

        if not card:
            print("No card returned from workflow, sending fallback")
            return fallback_card("⚠️ Something went wrong")

        # Safety: ensure full adaptive card is returned
        if not isinstance(card, dict):
            print("Workflow returned non-dict response, sending fallback")
            return fallback_card("⚠️ Invalid card response from backend")

        if card.get("type") != "AdaptiveCard":
            print("Workflow returned incomplete card, sending fallback")
            return fallback_card("⚠️ Backend did not return a full Adaptive Card")

        print("RETURN TYPE:", type(card))
        return card

    except Exception as e:
        print("ERROR IN WORKFLOW:", str(e))
        return fallback_card("❌ Backend error occurred")