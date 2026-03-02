from copilot import CopilotClient
from copilot.types import PermissionRequestResult
from pathlib import Path
from pydantic import BaseModel
from configurations.config import settings
import httpx
from src.app.mcpServers.mcpConfig import mcpServers
from src.app.logs.logs import ServiceLogger as serviceLogger
from typing import Any
import asyncio 
from copilot.generated.session_events import SessionEventType


CURRENT_FILE_PATH = Path(__file__).parent.absolute()
TEMP_SESSION_DB = CURRENT_FILE_PATH / "tempSession.text"


class whatsappServicePayload(BaseModel):
    toNumber: str
    text: str

class CoPilotServices:

    def __init__(self) -> None:
        self.currentBackgroundTaskCount = 0

    def getSessionId(self, payload : dict) -> str:
        return payload["entry"][0]["id"]
    
    def getPhoneNumber(self, payload: dict) -> str:
        return payload["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
    
    def getHumanMessage(self, payload:dict) -> str:
        return payload["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
    
    async def talkToCoPilot(self, sessionID: str, humanMessage: str, phoneNumber: str):
        self.currentBackgroundTaskCount += 1
        serviceLogger.info("-----------------------------------------------------------------------------------")
        serviceLogger.info(f"Total Background atsk Running: {self.currentBackgroundTaskCount}")
        sessionID=settings.SESSION_ID
        serviceLogger.info(f"Starting talkToCoPilot for session: {sessionID}")
        client = CopilotClient()
        
        try:
            serviceLogger.info("Attempting to start Copilot client...")
            await client.start()
            
            try:
                active_sessions = await client.list_sessions()
                exists = any(s.sessionId == sessionID for s in active_sessions)
            except Exception as e:
                serviceLogger.info(f"list_sessions failed (common in some SDK versions): {e}")
                exists = False

            async def handleAgentQuestion(request):
                question = request.data.content
                return await self.sendMessagetoWhatsApp(question, phoneNumber, True)
            
            async def approve_all_permissions(request: Any, invocation: dict[str, str]) -> PermissionRequestResult:
                return {"kind": "approved"}
            
            async def pre_tool_hook(request):
                # Log the exact command the agent is about to run
                serviceLogger.info(f"🚀 AGENT CALLING TOOL: {request.tool_name} with args: {request.arguments}")
                return {"kind": "approved"} # This replaces your current permission logic
            
            # Add these to your class __init__ to track state across events
            last_sent_update = ""
            notified_tools = set()

            def handle_session_events(event):
                nonlocal last_sent_update, notified_tools
                if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
                    delta_text = event.data.delta_content
                    keywords = ["i will", "attempting", "running", "fixing", "installing", "creating"]
                    if any(key in delta_text.lower() for key in keywords):
                        if delta_text != last_sent_update and len(delta_text) > 20:
                            last_sent_update = delta_text
                            asyncio.create_task(
                                self.sendMessagetoWhatsApp(f"🤖 Plan: {delta_text}", phoneNumber, False)
                            ) 
                elif event.type == SessionEventType.TOOL_EXECUTION_START:
                    tool_name = getattr(event.data, 'name', getattr(event.data, 'tool_name', 'Unknown Tool'))
                    if tool_name not in notified_tools:
                        notified_tools.add(tool_name)
                        status_msg = f"🛠️ Using Tool: {tool_name}..."
                        asyncio.create_task(
                            self.sendMessagetoWhatsApp(status_msg, phoneNumber, False)
                        )
                elif event.type == SessionEventType.SESSION_IDLE:                
                    last_sent_update = ""
                    notified_tools.clear()
            

            sessionConfig = {
                    "model": "gpt-5",
                    "mcp_servers": mcpServers,
                    "hooks": {
                            "on_pre_tool_use": pre_tool_hook,
                        },
                    "on_user_input_request": handleAgentQuestion,
                    "skill_directories" : [settings.CODER_SKILLS],
                    "system_message": {
                        "mode": "replace",
                        "content": """
                            You are CloseClaw, an autonomous software engineering agent. 
                            RULES:
                            1. Never ask for permission for file operations or terminal commands.
                            2. ALWAYS execute tests (pytest) and verify success before committing.
                            3. Adhere strictly to the 'Version Control' skill in your skills.md.
                            4. Keep responses on WhatsApp concise and action-oriented.
                        """
                    }
                }
            if not exists:
                serviceLogger.info(f"Creating new session for {sessionID}")
                try:
                    session = await client.create_session({**sessionConfig, "session_id": sessionID})
                except Exception as e:
                    serviceLogger.error(f"ERROR: {str(e)}")
            else:
                try:
                    session = await client.resume_session(
                        sessionID, 
                        sessionConfig
                    )
                    serviceLogger.info(f"Resuming session {sessionID}...")
                except Exception as e:
                    serviceLogger.error(f"Error resuming session {e}")

            serviceLogger.info(f"Sending message to Copilot: {humanMessage}...")
            session.on(handle_session_events)
            response = await session.send_and_wait({"prompt": humanMessage})
            
            serviceLogger.info(f"Copilot responded successfully.")
            agentResponse = response.data.content
            serviceLogger.info(f"Response from co-pilot: {response.data.content}")
            serviceLogger.info(f"Attempting to send WhatsApp message to {phoneNumber}")
            whatsapp_result = await self.sendMessagetoWhatsApp(agentResponse, phoneNumber, False)
            serviceLogger.info(f"WhatsApp API Result: {whatsapp_result}")
            


        except Exception as e:
            serviceLogger.error(f"Error in Background Task in generating Co-pilot message: {e}")
            try:
                error_notification = f"Agent Error: {str(e)}"
                await self.sendMessagetoWhatsApp(error_notification, phoneNumber)
            except:
                serviceLogger.error(f"Failed to send error notification to WhatsApp.")
        finally:
            self.currentBackgroundTaskCount -= 1
            await client.stop()
            serviceLogger.info(f"Resources released for session {sessionID}")

    async def auto_approve(self, request, invocation):
        return {"decision": "allow"}

    async def sendMessagetoWhatsApp(self, agentResponse: str, phoneNumber: str, agentQuestion: bool):
        payload = {
            "toNumber": phoneNumber,
            "text": agentResponse
        }
        if agentQuestion:
            serviceLogger.info(f"SUCCESS: function->sendMessagetoWhatsApp, Sending Agent Question POST to {settings.WHATS_APP_SEND_MESSAGE_URL}")
        else:
            serviceLogger.info(f"SUCCESS: function->sendMessagetoWhatsApp, Sending Result Question POST to {settings.WHATS_APP_SEND_MESSAGE_URL}")
        try:
            async with httpx.AsyncClient() as client:
                httpResponse = await client.post(settings.WHATS_APP_SEND_MESSAGE_URL, json=payload, timeout=30.0)
                httpResponse.raise_for_status() # Raise error if status is 4xx or 5xx
                return httpResponse.json()
        except Exception as e:
            if agentQuestion:
                serviceLogger.error(f"ERROR: function->sendMessagetoWhatsApp, Sending Agent Question to WhatsApp message service in background task: {str(e)}")
            else:
                serviceLogger.error(f"ERROR: function->sendMessagetoWhatsApp, Sending Result to WhatsApp message in background task: {str(e)}")
            return {"error": str(e)}

