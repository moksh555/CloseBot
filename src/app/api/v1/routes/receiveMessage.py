from fastapi import APIRouter, Depends, BackgroundTasks #type: ignore
from src.app.logs.logs import APIlogger as apiLogger


from src.app.api.dependecy.deps import (
    getRceiveMessagePayload,
    getAgentService
)
from src.app.services.AgentServices import (
    AgentService
)

from src.app.schemas.healthCheckSchemas import healthCheckResponse

router = APIRouter()

@router.post("/receive/message/whatsApp")
async def receiveMessageAPI(
    backgroundTasks: BackgroundTasks,
    agentService: AgentService = Depends(getAgentService), 
    receivedPayload: dict = Depends(getRceiveMessagePayload),   # This logs the HTTP request
    ):

    try:
        apiLogger.info("--------------------------------------------------------------------------")
        humanMessage = agentService.getHumanMessage(receivedPayload)
        phoneNumber = agentService.getPhoneNumber(receivedPayload)
        apiLogger.info("Starting Background tasks")
        backgroundTasks.add_task(agentService.talkToAgent, humanMessage, phoneNumber)
        apiLogger.info("SUCCESS: Background Task Running now!")

        return healthCheckResponse(status="Received", message="Recieved payload")
    except Exception as e:
        apiLogger.error(f"FAIL: Failed to parse WhatsApp payload: {str(e)}")
        return healthCheckResponse(status="Error", message="Payload parsing failed")



