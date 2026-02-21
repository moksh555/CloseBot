from copilot import CopilotClient
from pathlib import Path

CURRENT_FILE_PATH = Path(__file__).parent.absolute()
TEMP_SESSION_DB = CURRENT_FILE_PATH / "tempSession.text"


class CoPilotSservices:
    def __init__(self):
        self.client = CopilotClient()
    
    @classmethod
    async def create(cls):
        """Factory method to handle the async startup of the client."""
        instance = cls()
        await instance.client.start()
        return instance

    def getSessionId(self, payload : dict) -> str:
        return payload["entry"][0]["id"]
    
    async def checkSessionExists(self, sessionID):
        active_sessions = await self.client.list_sessions()
        exists = any(s['sessionId'] == sessionID for s in active_sessions)

        if not exists:
            await self.client.create_session({
                "session_id": sessionID, 
                "model": "gpt-4.1"}
            )
        return True
    
    def getHumanMessage(self, payload:dict) -> str:
        return payload["entry"][0]["changes"][0]["messages"][0]["text"]["body"]
    
    async def talkToCoPilot(self, sessionID, humanMessage):
        session = await self.client.resume_session({
            "session_id": sessionID
            }
        )
        response = await session.send_and_wait({"prompt": humanMessage})
        return response

