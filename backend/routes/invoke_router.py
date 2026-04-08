from fastapi import APIRouter, Request
from services.workflow_engine import handle_workflow

router = APIRouter()

@router.post("/invoke")
async def invoke(request: Request):
    body = await request.json()

    print("INVOKE BODY:", body)

    # Action.Execute sends data inside value.action
    value = body.get("value", {})
    action = value.get("action") or body.get("action")

    print("INVOKE ACTION:", action)

    # Build query dict same as Action.Submit data
    query = value if value else body

    card = handle_workflow(query)

    # Action.Execute expects this specific response format
    return {
        "statusCode": 200,
        "type": "application/vnd.microsoft.card.adaptive",
        "value": card
    }