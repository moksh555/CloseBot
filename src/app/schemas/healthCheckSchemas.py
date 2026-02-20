from pydantic import BaseModel


class healthCheckResponse(BaseModel):
    status: str
    message: str


