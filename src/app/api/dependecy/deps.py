from fastapi import Request #type: ignore
from src.app.services.AgentServices import AgentService

AGENT_INSTANCE = None

async def getRceiveMessagePayload(request: Request):
    return await request.json()

def getAgentService():
    global AGENT_INSTANCE

    if AGENT_INSTANCE is None:
        AGENT_INSTANCE = AgentService()
    return AGENT_INSTANCE

