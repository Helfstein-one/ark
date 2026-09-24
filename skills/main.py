from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any
from document_ingester import DocumentIngester

app = FastAPI(title="Project A.R.K. Skills Layer")
ingester = DocumentIngester()


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

    elif tool_input.name == "ingest_document":
        file_path = tool_input.arguments.get("file_path", "")
        chunk_size = tool_input.arguments.get("chunk_size", 500)
        chunk_overlap = tool_input.arguments.get("chunk_overlap", 50)

        if not file_path:
            raise HTTPException(status_code=400, detail="file_path argument is required")

        result = ingester.ingest_document(
            file_path=file_path,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        return ToolResponse(name=tool_input.name, result=result)

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
        },
        {
            "name": "ingest_document",
            "description": "Reads a document (PDF or text file), extracts its text, and splits it into semantic chunks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the document file"},
                    "chunk_size": {"type": "integer", "description": "Target max length per chunk", "default": 500},
                    "chunk_overlap": {"type": "integer", "description": "Overlap between chunks", "default": 50}
                },
                "required": ["file_path"]
            }
        }
    ]
