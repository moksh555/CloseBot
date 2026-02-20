from fastapi import Request


async def getRceiveMessagePayload(request: Request):
    return await request.json ()

