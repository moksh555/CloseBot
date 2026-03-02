from fastapi import APIRouter, Depends, BackgroundTasks
from src.app.logs.logs import APIlogger as apiLogger


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
    receivedPayload: dict = Depends(getRceiveMessagePayload),   # This logs the HTTP request
    ):

    try:
        apiLogger.info("--------------------------------------------------------------------------")
        apiLogger.info("SUCCESS: Receieved Message from Whats App")
        sessionID = copilotService.getSessionId(receivedPayload)
        humanMessage = copilotService.getHumanMessage(receivedPayload)
        phoneNumber = copilotService.getPhoneNumber(receivedPayload)
        apiLogger.info(f"SUCCESS: sessionID: {sessionID} -> humanMessage: {humanMessage} -> phoneNumber: {phoneNumber} ")
        apiLogger.info("Starting Background tasks")
        backgroundTasks.add_task(copilotService.talkToCoPilot, sessionID, humanMessage, phoneNumber)
        apiLogger.info("SUCCESS: Background Task Running now!")

        return healthCheckResponse(status="Received", message="Recieved payload")
    except Exception as e:
        apiLogger.error(f"FAIL: Failed to parse WhatsApp payload: {str(e)}")
        return healthCheckResponse(status="Error", message="Payload parsing failed")



