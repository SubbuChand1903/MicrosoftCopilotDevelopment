from fastapi import APIRouter, Response
from models.request_models import GenerateUIRequest
from services.workflow_engine import handle_workflow
from cards.ticket_board import ticket_board_card
import json
import time
import hashlib

router = APIRouter()

# --- DEDUP CACHE ---
_request_cache = {}
DEDUP_WINDOW = 3  # seconds


def is_duplicate(query) -> bool:
    key = hashlib.md5(str(query).encode()).hexdigest()
    now = time.time()
    if key in _request_cache and now - _request_cache[key] < DEDUP_WINDOW:
        print("DUPLICATE REQUEST BLOCKED:", key)
        return True
    _request_cache[key] = now
    for k in [k for k, v in _request_cache.items() if now - v > DEDUP_WINDOW]:
        del _request_cache[k]
    return False


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

    # Normalize
    if isinstance(query, dict):
        normalized_query = query
    elif isinstance(query, str):
        normalized_query = {"text": query.strip()}
    else:
        normalized_query = {"text": str(query).strip()}

    print("NORMALIZED QUERY:", normalized_query)

    # --- DEDUP CHECK ---
    if is_duplicate(normalized_query):
        print("SKIPPING DUPLICATE - returning 204")
        return Response(status_code=204)

    try:
        card = handle_workflow(normalized_query)

        if not card:
            print("No card returned from workflow, sending fallback")
            return fallback_card("⚠️ Something went wrong")

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