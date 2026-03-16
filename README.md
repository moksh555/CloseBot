# CloseBot — Agent Service Microservice

## Overview

CloseBot is a **FastAPI-based AI Agent microservice** that receives WhatsApp messages and responds to them intelligently using **Anthropic's Claude Agent SDK**. The service integrates with multiple external tools via MCP (Model Context Protocol) servers, enabling the agent to read/write files, manage emails, and interact with Google Calendar — all autonomously.

> **Migration Notice:** This project was originally built on the **GitHub Copilot SDK** and has been fully migrated to the **Claude Agent SDK** (`claude-agent-sdk >= 0.1.48`). The agent now runs with multi-turn conversation support, MCP tool integration, and permission bypass mode for autonomous operation.

---

## What This Project Does

1. **Receives WhatsApp messages** via a webhook endpoint (`POST /agents/receive/message/whatsApp`).
2. **Extracts message data** — phone number, session ID, and message body — from the incoming payload.
3. **Passes the message to a Claude Agent** which processes it with access to integrated MCP tools.
4. **Sends the AI-generated response** back to the user over WhatsApp via an external messaging API.
5. All operations run **asynchronously** with background task processing and graceful error handling.

---

## Key Features

- **FastAPI REST API** with async support
- **WhatsApp message reception and response** via webhook
- **AI-powered responses using Claude Agent SDK** (migrated from GitHub Copilot SDK)
- **MCP Server Integration** for real-world tool use (files, Gmail, Google Calendar)
- **Multi-turn conversations** (up to 30 turns per session)
- **Session management** and background task execution
- **Dockerised** with multi-stage build using `uv` for fast dependency management
- **Pydantic-based configuration** with environment variable support

---

## MCP Servers Integrated

The agent has access to the following MCP (Model Context Protocol) servers, enabling it to interact with real-world services:

| MCP Server | Description |
|---|---|
| **Moksh-Laptop** | Local file system access — read, write, and manage files on the host machine |
| **Gmail** | Email integration — search, read, and send emails via Gmail |
| **Google-Calender** | Calendar integration — check availability, create, search, and update Google Calendar events |

MCP server URLs are configured via environment variables (`LOCAL_FILE_MCP_SERVER`, `GMAIL_MCP_SERVER`, `CALENDAR_MCP_SERVER`).

---

## Directory Structure

```
CloseBot/
├── main.py                          # FastAPI application entry point
├── pyproject.toml                   # Project dependencies and metadata
├── Dockerfile                       # Multi-stage Docker build
├── configurations/
│   └── config.py                    # Pydantic settings & environment config
└── src/app/
    ├── api/v1/routes/
    │   └── receiveMessage.py        # WhatsApp webhook endpoint
    ├── services/
    │   ├── AgentServices.py         # Core Claude Agent SDK integration
    │   └── WhatsAppServices.py      # WhatsApp outbound messaging
    ├── mcpServers/
    │   ├── mcpConfig.py             # MCP server definitions (Laptop, Gmail, Calendar)
    │   └── mcpConfigServices.py     # MCP helper utilities
    └── schemas/                     # Pydantic request/response models
```

---

## How It Works

```
WhatsApp User
     │
     ▼
POST /agents/receive/message/whatsApp
     │
     ▼
AgentServices.py  ──►  Claude Agent SDK
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
        Moksh-Laptop        Gmail       Google Calendar
        (Local Files)      (Email)       (Events)
              │               │               │
              └───────────────┼───────────────┘
                              │
                              ▼
                    Response generated
                              │
                              ▼
                   WhatsApp reply sent back
```

---

## Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | REST API framework |
| **Claude Agent SDK** (`claude-agent-sdk`) | AI agent with tool use |
| **FastMCP** (`fastmcp`) | MCP server communication |
| **Pydantic / Pydantic-Settings** | Data validation & config |
| **Docker + uv** | Containerisation & dependency management |
| **Python 3.10+** | Runtime |

---

## Environment Variables

Create a `configurations/.env` file with the following:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key
WHATS_APP_SEND_MESSAGE_URL=your_whatsapp_api_url
LOCAL_FILE_MCP_SERVER=http://your-local-mcp-server-url
GMAIL_MCP_SERVER=http://your-gmail-mcp-server-url
CALENDAR_MCP_SERVER=http://your-calendar-mcp-server-url
LOCAL_FILE_SECRET_TOKEN=your_secret_token
```

---

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/moksh555/CloseBot.git
   cd CloseBot
   ```

2. **Set up environment variables** — copy and fill in `configurations/.env`

3. **Install dependencies**
   ```bash
   pip install uv
   uv sync
   ```

4. **Run the FastAPI server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Or run with Docker**
   ```bash
   docker build -t closebot .
   docker run --env-file configurations/.env -p 8000:8000 closebot
   ```

---

## Use Cases

- **Customer support automation** over WhatsApp
- **AI-powered personal assistant** with calendar and email access
- **Autonomous task execution** via natural language WhatsApp messages
- **AI-driven project management** assistant

---

## Migration Note

This service was originally powered by the **GitHub Copilot SDK** for AI response generation. It has since been **fully migrated to Anthropic's Claude Agent SDK**, which provides:

- Native MCP (Model Context Protocol) server support
- Multi-turn agentic conversations
- Tool use with permission bypass for autonomous workflows
- Superior context handling and reasoning capabilities
