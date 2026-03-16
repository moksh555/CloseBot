
from pathlib import Path
from pydantic import BaseModel
from configurations.config import settings
import httpx
from src.app.mcpServers.mcpConfig import mcpServers
from src.app.logs.logs import ServiceLogger as serviceLogger
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions,AssistantMessage, TextBlock, ResultMessage #type: ignore

CURRENT_FILE_PATH = Path(__file__).parent.absolute()

class whatsappServicePayload(BaseModel):
    toNumber: str
    text: str

class AgentService:

    _instance = None

    # def __new__(cls):
    #     if cls._instance is None:
    #         cls._instance = super().__new__(cls)
    #     return cls._instance
    
    def __init__(self) -> None:
        options = ClaudeAgentOptions(
            max_turns = 30,
            permission_mode="bypassPermissions",
            effort="high",
            env={
            "CLAUDE_CODE_COMPLETED_ONBOARDING": "true",
            "ANTHROPIC_API_KEY": settings.ANTHROPIC_API_KEY
            },
            mcp_servers=mcpServers,
            allowed_tools=["mcp__Moksh-Laptop__*"]
        )
        self.client = ClaudeSDKClient(options)
        
        
    
    def getPhoneNumber(self, payload: dict) -> str:
        return payload["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
    
    def getHumanMessage(self, payload:dict) -> str:
        return payload["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
    
    async def talkToAgent(self, humanMessage: str, phoneNumber: str):    
        await self.client.connect()        
        async with self.client as agent:
            await agent.query(humanMessage)

            async for message in agent.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"AgentMessage: {block.text}")
                elif isinstance(message, ResultMessage):
                    sessionId = message.session_id
                    if message.subtype == "success":
                        print(f"Done: {message.result}")
                    elif message.subtype == "error_max_turns":
                        print(f"Hit turn limit. Resume session {sessionId} to continue.")
                    elif message.subtype == "error_max_budget_usd":
                        print("Hit budget limit.")
                    else:
                        print(f"Stopped: {message.subtype}")
                    if message.total_cost_usd is not None:
                        print(f"Cost: ${message.total_cost_usd:.4f}")
        self.client.disconnect()        

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

