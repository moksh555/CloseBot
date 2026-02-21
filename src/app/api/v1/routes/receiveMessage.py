from fastapi import APIRouter, Depends
from src.app.api.dependecy.deps import (
    getRceiveMessagePayload,
    getCoPilotService
)
from src.app.services.coPilotServices import (
    CoPilotServices
)

from src.app.schemas.healthCheckSchemas import healthCheckResponse

router = APIRouter()

@router.post("/receive/message/whatsApp")
async def receiveMessageAPI(copilotService: CoPilotServices = Depends(getCoPilotService), receivedPayload: dict = Depends(getRceiveMessagePayload)):

    sessionID = copilotService.getSessionId(receivedPayload)
    humanMessage = copilotService.getHumanMessage(receivedPayload)
    
    newSession = await copilotService.checkNewSession(sessionID)
    response = await copilotService.talkToCoPilot(sessionID, humanMessage)

    print(response)

    return healthCheckResponse(status="Received", message="Recieved payload")



