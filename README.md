# Agents Playground

My personal playground for understanding how LLMs and agents actually work under the hood.

## What's Built

**[streamlit_chat/](streamlit_chat/)** - Universal web UI that plugs into any agent I build. Handles chat, streaming responses, thread management, and backend API integration.

**[plan_exec/](plan_exec/)** - LangGraph-based planning/execution agent with web search (Tavily) and task management. Includes Phoenix tracing for observability.

**[food_mcp/](food_mcp/)** - MCP server for Claude Desktop that manages pantry inventory. Parses receipt images, tracks expiration dates, and handles CRUD operations on grocery items.

## Stack
LangChain, LangGraph, OpenAI GPT-4o, Streamlit, FastMCP, Arize Phoenix
