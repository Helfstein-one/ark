from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any

app = FastAPI(title="Project A.R.K. Skills Layer")

class ToolInput(BaseModel):
    name: str
    arguments: dict

class ToolResponse(BaseModel):
    name: str
    result: Any

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/tools/call", response_model=ToolResponse)
def call_tool(tool_input: ToolInput):
    """
    Endpoint compatible with Open WebUI external tools.
    """
    if tool_input.name == "web_search":
        query = tool_input.arguments.get("query", "")
        # Mock web search result
        return ToolResponse(name=tool_input.name, result=f"Mocked search results for: {query}")

    elif tool_input.name == "fs_read":
        path = tool_input.arguments.get("path", "")
        # Mock file system read
        return ToolResponse(name=tool_input.name, result=f"Mocked file content for {path}")

    else:
        raise HTTPException(status_code=404, detail=f"Tool {tool_input.name} not found")

@app.get("/tools", response_model=List[dict])
def list_tools():
    """
    Returns the list of available tools.
    """
    return [
        {
            "name": "web_search",
            "description": "Performs a web search.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query"}
                },
                "required": ["query"]
            }
        },
        {
            "name": "fs_read",
            "description": "Reads a file from the mock file system.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "The file path"}
                },
                "required": ["path"]
            }
        }
    ]
