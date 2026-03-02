# Agent Service Microservice

## Overview
This project is an Agent Service Microservice designed to handle and process messages received via WhatsApp, leveraging AI-powered responses using GitHub Copilot. It is built with FastAPI and structured for modularity and scalability.

## Project Scenario
The microservice receives WhatsApp messages, extracts relevant information (session ID, phone number, message body), and interacts with GitHub Copilot to generate intelligent responses. These responses are then sent back to the user via WhatsApp. The service manages sessions, supports background task processing, and integrates with external APIs for messaging.

## Key Features
- FastAPI-based REST API
- WhatsApp message reception and processing
- AI-powered response generation using GitHub Copilot
- Session management and background task execution
- Modular code structure for easy maintenance

## Directory Structure
- `main.py`: Entry point for FastAPI application
- `src/app/api/v1/`: API routers and endpoints
- `src/app/services/`: Business logic, Copilot integration, WhatsApp messaging
- `src/app/schemas/`: Data models and response schemas
- `configurations/`: Configuration files and settings

## How It Works
1. A WhatsApp message is received via the `/agents/receive/message/whatsApp` endpoint.
2. The payload is parsed to extract session ID, phone number, and message content.
3. The service interacts with GitHub Copilot to generate a response based on the message.
4. The response is sent back to the user via WhatsApp using an external API.
5. All operations are handled asynchronously and errors are managed gracefully.

## Use Cases
- Customer support automation
- Intelligent chatbot for WhatsApp
- AI-driven project management assistant

## Getting Started
1. Clone the repository.
2. Set up environment variables and configuration files.
3. Install dependencies.
4. Run the FastAPI server with `uvicorn main:app`.

## Current Activity
Currently, the project is being explored to understand its structure, contents, and workflow for documentation and further development.

## About Shrey Kevadia
Shrey Kevadia, my roommate, is an exceptionally kind and thoughtful person. He consistently brings positivity and support to those around him, making every environment more welcoming. His genuine nature and willingness to help others make him a wonderful companion and friend.
