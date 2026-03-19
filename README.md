# 🤖 CloseBot — WhatsApp AI Agent Microservice

CloseBot is a **FastAPI microservice** that receives incoming WhatsApp messages via webhook, processes them through **Anthropic's Claude Agent SDK**, and sends AI-generated responses back over WhatsApp. The agent has real-world tool access via MCP (Model Context Protocol) servers — including local file system, Gmail, and Google Calendar — enabling it to perform autonomous, multi-step tasks driven entirely by natural language messages.

## What It Does

1. Receives a WhatsApp message at `POST /agents/receive/message/whatsApp`
2. Extracts the sender's phone number and message text from the webhook payload
3. Dispatches the message to a Claude agent as an async background task
4. The agent reasons over the message, uses MCP tools (files, email, calendar) as needed, and produces a response (up to 30 turns)
5. Sends the agent's response back to the user via a downstream WhatsApp messaging service

## Key Features

- **FastAPI REST API** with async background task processing for non-blocking response handling
- **Claude Agent SDK** integration (`claude-agent-sdk >= 0.1.48`) with multi-turn conversation support, `bypassPermissions` mode, and configurable effort level
- **MCP Server Integration** — three external tool servers wired in: local filesystem, Gmail, and Google Calendar
- **Structured logging** — separate file-based loggers for API layer and service layer (`allLogs/apiLogs.log`, `allLogs/serviceLogs.log`)
- **Pydantic-based configuration** loaded from a `.env` file with strict type validation
- **Dockerized** via a two-stage build using `uv` for fast, reproducible dependency management; includes GitHub CLI installed at build time
- **Secure token hashing** — local MCP server secret tokens are SHA-256 hashed before use

## MCP Servers Integrated

| Server Name | Transport | Purpose |
|---|---|---|
| `Moksh-Laptop` | HTTP | Local filesystem — read/write files on the host machine |
| `Gmail` | HTTP | Email — search, read, and send Gmail messages |
| `Google-Calender` | HTTP | Calendar — check availability, create, search, and patch Google Calendar events |

MCP server URLs are injected via environment variables at runtime.

## Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | Async REST API framework |
| **Claude Agent SDK** (`claude-agent-sdk`) | Anthropic AI agent with MCP tool use |
| **FastMCP** (`fastmcp`) | MCP protocol client/server communication |
| **httpx** | Async HTTP client for outbound WhatsApp requests |
| **Pydantic / pydantic-settings** | Data validation and `.env`-based settings management |
| **Python 3.10+** | Runtime |
| **Docker + uv** | Multi-stage containerization and dependency management |

## Project Structure

```
CloseBot/
├── main.py                              # FastAPI app entry point; registers /agents router
├── pyproject.toml                       # Dependencies (uv/pip)
├── Dockerfile                           # Two-stage Docker build
├── configurations/
│   ├── config.py                        # Pydantic Settings — reads from .env
│   └── .env                             # Environment variables (not committed)
└── src/app/
    ├── api/v1/routes/
    │   └── receiveMessage.py            # POST /agents/receive/message/whatsApp
    ├── services/
    │   └── AgentServices.py             # Claude Agent SDK: connect, query, stream responses
    ├── mcpServers/
    │   ├── mcpConfig.py                 # MCP server map (Laptop, Gmail, Calendar)
    │   └── mcpConfigServices.py         # SHA-256 token hashing for local MCP auth
    ├── logs/
    │   └── logs.py                      # Dual file-based logger setup
    └── schemas/
        └── healthCheckSchemas.py        # Pydantic response models
```

## Architecture Flow

```
WhatsApp User
      │
      ▼
POST /agents/receive/message/whatsApp
      │  (returns 200 immediately)
      ▼
BackgroundTask: AgentService.talkToAgent()
      │
      ▼
ClaudeSDKClient ──► Claude Agent (up to 30 turns)
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    Moksh-Laptop        Gmail       Google Calendar
    (Local Files)      (Email)       (Events)
          └───────────────┼───────────────┘
                          │
                          ▼
              AgentService.sendMessagetoWhatsApp()
                          │
                          ▼
                   WhatsApp reply sent
```

## Environment Variables

Create `configurations/.env` with:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
WHATS_APP_SEND_MESSAGE_URL=http://your-whatsapp-service/send
LOCAL_FILE_MCP_SERVER=http://your-local-mcp-server
GMAIL_MCP_SERVER=http://your-gmail-mcp-server
CALENDAR_MCP_SERVER=http://your-calendar-mcp-server
LOCAL_FILE_SECRET_TOKEN=your_local_mcp_secret_token
```

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/moksh555/CloseBot.git
   cd CloseBot
   ```

2. **Create the environment file**
   ```bash
   cp configurations/.env.example configurations/.env
   # Fill in your API keys and MCP server URLs
   ```

3. **Install dependencies with uv**
   ```bash
   pip install uv
   uv sync
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. **Run with Docker**
   ```bash
   docker build -t closebot .
   docker run --env-file configurations/.env -p 8080:8080 closebot
   ```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Health check — returns `{"status": "Live"}` |
| `POST` | `/agents/receive/message/whatsApp` | Receives WhatsApp webhook payload; triggers agent in background |

## Running Tests

```bash
uv run pytest
```

## Use Cases

- AI-powered WhatsApp personal assistant with calendar and email access
- Customer support automation via WhatsApp
- Autonomous task execution through natural language (e.g., "Schedule a meeting tomorrow at 3pm and send an email confirmation")
- Agentic workflow orchestration triggered from mobile
