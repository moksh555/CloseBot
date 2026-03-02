from src.app.mcpServers.mcpConfigServices import McpConfigServices
from configurations.config import settings

mcpServers = {
    "Moksh-Laptop": {
      "type": "http",
      "url": settings.LOCAL_FILE_MCP_SERVER,
      "headers": {
        "Authorization": f"Bearer {McpConfigServices.getHashedLocalFileSecretToken()}"
      },
      "tools": ["*"]
    }
}