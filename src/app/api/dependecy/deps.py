from fastapi import Request
from src.app.services.coPilotServices import CoPilotSservices

async def getRceiveMessagePayload(request: Request):
    return await request.json ()

def getCoPilotService():
    return CoPilotSservices()

