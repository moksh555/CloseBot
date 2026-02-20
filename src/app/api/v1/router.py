from fastapi import APIRouter # type:ignore
from src.app.api.v1.routes.receiveMessage import router as receiveMessage


mainApiRouter = APIRouter()

mainApiRouter.include_router(receiveMessage, tags=["ReceiveMessage"])



