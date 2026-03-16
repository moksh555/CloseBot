from src.app.mcpServers.mcpConfigServices import McpConfigServices
from configurations.config import settings

mcpServers = {
    "Moksh-Laptop": {
      "type": "http",
      "url": settings.LOCAL_FILE_MCP_SERVER,
    }, 

    "Gmail": {
      "type": "http",
      "url": settings.GMAIL_MCP_SERVER,
    },

    "Google-Calender": {
      "type": "http",
      "url": settings.CALENDAR_MCP_SERVER,
    },
}