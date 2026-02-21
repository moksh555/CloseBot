from copilot import CopilotClient
from pathlib import Path


CURRENT_FILE_PATH = Path(__file__).parent.absolute()
TEMP_SESSION_DB = CURRENT_FILE_PATH / "tempSession.text"


class CoPilotServices:

    async def startClient(self):
        client = CopilotClient()
        await client.start()
        return client

    def getSessionId(self, payload : dict) -> str:
        return payload["entry"][0]["id"]
    
    async def checkSessionExists(self, client, sessionID):
        active_sessions = await client.list_sessions()
        print(active_sessions)
        exists = any(s.sessionId == sessionID for s in active_sessions)

        if not exists:
            await client.create_session({
                "session_id": sessionID, 
                "model": "gpt-4.1"}
            )
        return True
    
    def getHumanMessage(self, payload:dict) -> str:
        return payload["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
    
    def talkToCoPilot(self, client, sessionID, humanMessage):
        print("---------------------------")
        print(sessionID)
        session = client.resume_session(sessionID)
        response = session.send_and_wait({"prompt": humanMessage})
        print(response)
        print(response.data.content)
        return response
    
    def test(self,client, sessionID, humanMessage):
        print(sessionID)
        print(humanMessage)
        print("----------------------")
        return True

    

