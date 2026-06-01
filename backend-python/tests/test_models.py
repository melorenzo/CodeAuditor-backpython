import pytest
from pydantic import ValidationError
from app.models import CodeRequest, CodeResponse


# --------------------------------------------------------------------------- #
# CodeRequest
# --------------------------------------------------------------------------- #

def test_code_request_valid():
    req = CodeRequest(code="print('hola')", language="python")
    assert req.language == "python"


def test_code_request_language_case_insensitive():
    """El lenguaje se normaliza a minúsculas."""
    req = CodeRequest(code="x = 1", language="Python")
    assert req.language == "python"


def test_code_request_code_stripped():
    """El código se trimea de espacios."""
    req = CodeRequest(code="  x = 1  ", language="python")
    assert req.code == "x = 1"


def test_code_request_empty_code_raises():
    with pytest.raises(ValidationError):
        CodeRequest(code="", language="python")


def test_code_request_whitespace_code_raises():
    with pytest.raises(ValidationError):
        CodeRequest(code="   ", language="python")


def test_code_request_code_too_long_raises():
    with pytest.raises(ValidationError):
        CodeRequest(code="x" * 10_001, language="python")


def test_code_request_invalid_language_raises():
    with pytest.raises(ValidationError):
        CodeRequest(code="x = 1", language="fortran")


# --------------------------------------------------------------------------- #
# CodeResponse
# --------------------------------------------------------------------------- #

def test_code_response_valid():
    resp = CodeResponse(
        severity="Crítico",
        vulnerabilities=["inyección SQL"],
        refactored_code="SELECT * FROM users WHERE id = ?",
        explanation="Se detectó inyección SQL.",
        clean_code_tips=["Usar queries parametrizadas"]
    )
    assert resp.severity == "Crítico"


def test_code_response_invalid_severity_fallback():
    """Severity inválido hace fallback a Advertencia en lugar de explotar."""
    resp = CodeResponse(
        severity="Desconocido",
        vulnerabilities=[],
        refactored_code="",
        explanation="",
        clean_code_tips=[]
    )
    assert resp.severity == "Advertencia"
