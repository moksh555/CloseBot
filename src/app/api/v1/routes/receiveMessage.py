from fastapi import APIRouter, Depends, BackgroundTasks

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
async def receiveMessageAPI(
    backgroundTasks: BackgroundTasks,
    copilotService: CoPilotServices = Depends(getCoPilotService), 
    receivedPayload: dict = Depends(getRceiveMessagePayload),
    
    ):

    sessionID = copilotService.getSessionId(receivedPayload)
    print("---------------------------")
    print(sessionID)
    humanMessage = copilotService.getHumanMessage(receivedPayload)
    # client = await copilotService.startClient()
    # newSession = await copilotService.checkSessionExists(client, sessionID)
    backgroundTasks.add_task(copilotService.test, sessionID, humanMessage)

    return healthCheckResponse(status="Received", message="Recieved payload")



