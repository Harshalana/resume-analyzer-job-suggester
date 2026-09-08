"""
Tests for PDF and DOCX binary file uploads
"""

import io
from fastapi.testclient import TestClient
from backend.main import app
from pypdf import PdfWriter
from docx import Document
from backend.samples import SAMPLE_RESUMES

client = TestClient(app)


def create_mock_docx(text: str) -> bytes:
    """Create a mock docx in memory."""
    doc = Document()
    for line in text.splitlines():
        if line.strip():
            doc.add_paragraph(line)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


def test_docx_upload():
    """Verify DOCX upload and parsing."""
    sample_text = SAMPLE_RESUMES[2]["text"] # Marcus Vance (DevOps)
    docx_bytes = create_mock_docx(sample_text)

    response = client.post(
        "/api/analyze",
        files={"file": ("marcus_resume.docx", docx_bytes, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    )

    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    assert res_json["parsed"]["contact"]["name"] == "Marcus Vance"
    assert "DevOps & Cloud Infrastructure Engineer" in [j["title"] for j in res_json["job_matches"][:2]]

