import os
import sys
import tempfile
import requests
import pytest
import PyPDF2
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add skills directory to python path for direct imports
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../skills"))
)
from document_ingester import DocumentIngester, Tools  # noqa: E402


def test_ollama_port_restricted_from_host():
    try:
        requests.get("http://127.0.0.1:11434/api/tags", timeout=2)
        assert False, "Ollama port 11434 should not be directly exposed"
    except requests.exceptions.ConnectionError:
        pass  # Successfully blocked/restricted


def test_open_webui_via_proxy_https():
    try:
        response = requests.get("https://127.0.0.1", verify=False, timeout=2)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.skip("Open WebUI proxy service not running locally.")


def test_skills_layer_health():
    try:
        response = requests.get("http://127.0.0.1:8001/health", timeout=2)
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
    except requests.exceptions.ConnectionError:
        pytest.skip("Skills Layer service not running locally.")


def test_skills_layer_list_tools():
    try:
        response = requests.get("http://127.0.0.1:8001/tools", timeout=2)
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
            json={"name": "web_search", "arguments": {"query": "AI Agents"}},
            timeout=2,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "web_search"
        assert "Mocked search results for: AI Agents" in data["result"]
    except requests.exceptions.ConnectionError:
        pytest.skip("Skills Layer service not running locally.")


def test_prometheus_is_running():
    try:
        response = requests.get("http://127.0.0.1:9090/-/healthy", timeout=2)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.skip("Prometheus service not running locally.")


def test_grafana_is_running():
    try:
        response = requests.get("http://127.0.0.1:3000/api/health", timeout=2)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.skip("Grafana service not running locally.")


def helper_create_dummy_pdf(path: str, content_pages: list):
    """Utility to generate a dummy PDF with text using PyPDF2."""
    writer = PyPDF2.PdfWriter()
    for _ in content_pages:
        writer.add_blank_page(width=612, height=792)

    pdf_bytes = (
        b"%PDF-1.4\n"
        b"1 0 obj <</Type /Catalog /Pages 2 0 R>> endobj\n"
        b"2 0 obj <</Type /Pages /Kids [3 0 R] /Count 1>> endobj\n"
        b"3 0 obj <</Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >> endobj\n"
        b"4 0 obj <</Length 55>> stream\n"
        b"BT\n/F1 12 Tf\n100 700 Td\n(Project A.R.K. Dummy PDF Content) Tj\nET\n"
        b"endstream\nendobj\n"
        b"5 0 obj <</Type /Font /Subtype /Type1 /BaseFont /Helvetica>> endobj\n"
        b"xref\n0 6\n0000000000 65535 f \n0000000009 00000 n \n"
        b"0000000058 00000 n \n0000000115 00000 n \n0000000244 00000 n \n"
        b"0000000348 00000 n \n"
        b"trailer <</Size 6 /Root 1 0 R>>\nstartxref\n425\n%%EOF\n"
    )
    with open(path, "wb") as f:
        f.write(pdf_bytes)


def test_document_ingestion_text_file():
    ingester = DocumentIngester()
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".txt", delete=False) as f:
        f.write(
            "Paragraph 1: Project A.R.K. modular skills layer.\n\n"
            "Paragraph 2: Ingesting heavy document files into chunks."
        )
        f_path = f.name

    try:
        res = ingester.ingest_document(f_path, chunk_size=50, chunk_overlap=10)
        assert res["status"] == "SUCCESS"
        assert res["total_chunks"] > 0
        assert "Project A.R.K." in res["chunks"][0]["text"]
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)


def test_document_ingestion_pdf_file():
    ingester = DocumentIngester()
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        f_path = f.name

    try:
        helper_create_dummy_pdf(f_path, ["Dummy content"])
        res = ingester.ingest_document(f_path)
        assert res["status"] == "SUCCESS"
        assert res["total_chunks"] >= 1
        assert "Project A.R.K. Dummy PDF Content" in res["chunks"][0]["text"]
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)


def test_document_ingestion_tools_class():
    tools = Tools()
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".txt", delete=False) as f:
        f.write("Testing Tools class wrapper for document ingestion.")
        f_path = f.name

    try:
        res = tools.ingest_document(f_path)
        assert res["status"] == "SUCCESS"
        assert len(res["chunks"]) == 1
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)
