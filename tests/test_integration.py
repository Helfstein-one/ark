import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def test_ollama_port_restricted_from_host():
    try:
        requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        assert False, "Ollama port 11434 should not be directly exposed to the host interface"
    except requests.exceptions.ConnectionError:
        pass # Successfully blocked/restricted

def test_open_webui_via_proxy_https():
    response = requests.get("https://127.0.0.1", verify=False)
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

def test_prometheus_is_running():
    response = requests.get("http://127.0.0.1:9090/-/healthy")
    assert response.status_code == 200

def test_grafana_is_running():
    response = requests.get("http://127.0.0.1:3000/api/health")
    assert response.status_code == 200
