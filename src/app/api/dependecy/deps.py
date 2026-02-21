from fastapi import Request

from src.app.services.coPilotServices import CoPilotServices


async def getRceiveMessagePayload(request: Request):
    return await request.json()

def getCoPilotService():
    return CoPilotServices()

