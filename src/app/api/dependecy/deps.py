from fastapi import Request
from src.app.services.coPilotServices import CoPilotServices

COPILOT_INSTANCE = None

async def getRceiveMessagePayload(request: Request):
    return await request.json()

def getCoPilotService():
    global COPILOT_INSTANCE

    if COPILOT_INSTANCE is None:
        COPILOT_INSTANCE = CoPilotServices()
    return COPILOT_INSTANCE

