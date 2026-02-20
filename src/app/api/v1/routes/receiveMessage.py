from fastapi import APIRouter, Depends
from src.app.api.dependecy.deps import (
    getRceiveMessagePayload
)
from src.app.schemas.healthCheckSchemas import healthCheckResponse

router = APIRouter()

@router.post("/receive/message/whatsApp")
def receiveMessageAPI(receivedPayload: dict = Depends(getRceiveMessagePayload)):

    print(receivedPayload)

    return healthCheckResponse(status="Received", message="Recieved payload")



