import requests

def test_ollama_is_running():
    response = requests.get("http://127.0.0.1:11434/api/tags")
    assert response.status_code == 200
    assert "models" in response.json()

def test_open_webui_is_running():
    response = requests.get("http://127.0.0.1:8000")
    # Open WebUI returns 200 for the index HTML
    assert response.status_code == 200

def test_skills_layer_health():
    response = requests.get("http://127.0.0.1:8001/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_skills_layer_list_tools():
    response = requests.get("http://127.0.0.1:8001/tools")
    assert response.status_code == 200
    tools = response.json()
    assert isinstance(tools, list)
    assert any(tool["name"] == "web_search" for tool in tools)

def test_skills_layer_call_tool():
    response = requests.post(
        "http://127.0.0.1:8001/tools/call",
        json={"name": "web_search", "arguments": {"query": "AI Agents"}}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "web_search"
    assert "Mocked search results for: AI Agents" in data["result"]
