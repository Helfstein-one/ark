import os
import sys
import tempfile
import requests
import pytest
import PyPDF2

# Add skills directory to python path for direct imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../skills")))
from document_ingester import DocumentIngester, Tools

def test_ollama_is_running():
    try:
        response = requests.get("http://127.0.0.1:11434/api/tags")
        assert response.status_code == 200
        assert "models" in response.json()
    except requests.exceptions.ConnectionError:
        pytest.skip("Ollama service not running locally.")

def test_open_webui_is_running():
    try:
        response = requests.get("http://127.0.0.1:8000")
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.skip("Open WebUI service not running locally.")

def test_skills_layer_health():
    try:
        response = requests.get("http://127.0.0.1:8001/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
    except requests.exceptions.ConnectionError:
        pytest.skip("Skills Layer service not running locally.")

def test_skills_layer_list_tools():
    try:
        response = requests.get("http://127.0.0.1:8001/tools")
        assert response.status_code == 200
        tools = response.json()
        assert isinstance(tools, list)
        assert any(tool["name"] == "web_search" for tool in tools)
        assert any(tool["name"] == "ingest_document" for tool in tools)
    except requests.exceptions.ConnectionError:
        pytest.skip("Skills Layer service not running locally.")

def test_skills_layer_call_tool():
    try:
        response = requests.post(
            "http://127.0.0.1:8001/tools/call",
            json={"name": "web_search", "arguments": {"query": "AI Agents"}}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "web_search"
        assert "Mocked search results for: AI Agents" in data["result"]
    except requests.exceptions.ConnectionError:
        pytest.skip("Skills Layer service not running locally.")

def helper_create_dummy_pdf(path: str, content_pages: list):
    """Utility to generate a dummy PDF with text using PyPDF2."""
    writer = PyPDF2.PdfWriter()
    for text in content_pages:
        page = writer.add_blank_page(width=612, height=792)
        # Note: PyPDF2 blank pages don't have text unless written or imported.
        # To test PyPDF2 extraction cleanly with text content without extra heavy dependencies like ReportLab,
        # we can write a plain text file or use pypdf structures. Let's create a minimal PDF stream or test plain text & mock PDF extraction.
    # Alternatively, PyPDF2 can write simple PDF annotations or page streams.
    # Let's create a valid PDF file stream with text content stream:
    pdf_bytes = (
        b"%PDF-1.4\n"
        b"1 0 obj <</Type /Catalog /Pages 2 0 R>> endobj\n"
        b"2 0 obj <</Type /Pages /Kids [3 0 R] /Count 1>> endobj\n"
        b"3 0 obj <</Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj\n"
        b"4 0 obj <</Length 55>> stream\n"
        b"BT\n/F1 12 Tf\n100 700 Td\n(Project A.R.K. Dummy PDF Content) Tj\nET\n"
        b"endstream\nendobj\n"
        b"5 0 obj <</Type /Font /Subtype /Type1 /BaseFont /Helvetica>> endobj\n"
        b"xref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000244 00000 n \n0000000348 00000 n \n"
        b"trailer <</Size 6 /Root 1 0 R>>\nstartxref\n425\n%%EOF\n"
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
