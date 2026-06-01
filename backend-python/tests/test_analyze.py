import pytest
from unittest.mock import AsyncMock, patch
from app.models import CodeResponse

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

VALID_PAYLOAD = {
    "code": "import os\nos.system(input())",
    "language": "python"
}

MOCK_RESPONSE = CodeResponse(
    severity="Crítico",
    vulnerabilities=["Inyección de comandos"],
    refactored_code="# código seguro",
    explanation="Se detectó inyección de comandos.",
    clean_code_tips=["Validar inputs", "Usar subprocess"]
)


# --------------------------------------------------------------------------- #
# Casos felices
# --------------------------------------------------------------------------- #

def test_analyze_success(client, mock_groq_service):
    """Respuesta exitosa con payload válido."""
    mock_groq_service.analyze_code = AsyncMock(return_value=MOCK_RESPONSE)

    response = client.post("/analyze", json=VALID_PAYLOAD)

    assert response.status_code == 200
    data = response.json()
    assert data["severity"] == "Crítico"
    assert "Inyección de comandos" in data["vulnerabilities"]
    assert data["explanation"] != ""
    assert isinstance(data["clean_code_tips"], list)
    assert isinstance(data["vulnerabilities"], list)


def test_analyze_all_languages(client, mock_groq_service):
    """Todos los lenguajes soportados deben ser aceptados."""
    mock_groq_service.analyze_code = AsyncMock(return_value=MOCK_RESPONSE)

    languages = ["python", "java", "javascript", "typescript", "go", "rust", "c", "cpp"]
    for lang in languages:
        response = client.post("/analyze", json={"code": "x = 1", "language": lang})
        assert response.status_code == 200, f"Falló para lenguaje: {lang}"


def test_analyze_response_structure(client, mock_groq_service):
    """La respuesta siempre tiene todas las claves requeridas."""
    mock_groq_service.analyze_code = AsyncMock(return_value=MOCK_RESPONSE)

    response = client.post("/analyze", json=VALID_PAYLOAD)
    data = response.json()

    required_keys = {"severity", "vulnerabilities", "refactored_code", "explanation", "clean_code_tips"}
    assert required_keys.issubset(data.keys())


# --------------------------------------------------------------------------- #
# Validación de inputs
# --------------------------------------------------------------------------- #

def test_analyze_empty_code(client):
    """Código vacío debe devolver 422."""
    response = client.post("/analyze", json={"code": "", "language": "python"})
    assert response.status_code == 422


def test_analyze_whitespace_only_code(client):
    """Código con solo espacios debe devolver 422."""
    response = client.post("/analyze", json={"code": "   \n\t  ", "language": "python"})
    assert response.status_code == 422


def test_analyze_code_too_long(client):
    """Código que supera el límite de caracteres debe devolver 422."""
    long_code = "x = 1\n" * 2000  # ~12000 chars
    response = client.post("/analyze", json={"code": long_code, "language": "python"})
    assert response.status_code == 422


def test_analyze_unsupported_language(client):
    """Lenguaje no soportado debe devolver 422."""
    response = client.post("/analyze", json={"code": "x = 1", "language": "cobol"})
    assert response.status_code == 422


def test_analyze_missing_code_field(client):
    """Falta el campo code debe devolver 422."""
    response = client.post("/analyze", json={"language": "python"})
    assert response.status_code == 422


def test_analyze_missing_language_field(client):
    """Falta el campo language debe devolver 422."""
    response = client.post("/analyze", json={"code": "x = 1"})
    assert response.status_code == 422


def test_analyze_empty_body(client):
    """Body vacío debe devolver 422."""
    response = client.post("/analyze", json={})
    assert response.status_code == 422


# --------------------------------------------------------------------------- #
# Manejo de errores del servicio
# --------------------------------------------------------------------------- #

def test_analyze_groq_value_error(client, mock_groq_service):
    """Si GroqService lanza ValueError debe devolver 422."""
    mock_groq_service.analyze_code = AsyncMock(
        side_effect=ValueError("La IA devolvió una respuesta mal formada")
    )

    response = client.post("/analyze", json=VALID_PAYLOAD)
    assert response.status_code == 422
    assert "mal formada" in response.json()["detail"]


def test_analyze_groq_unexpected_error(client, mock_groq_service):
    """Si GroqService lanza una excepción inesperada debe devolver 500."""
    mock_groq_service.analyze_code = AsyncMock(
        side_effect=Exception("Timeout de red")
    )

    response = client.post("/analyze", json=VALID_PAYLOAD)
    assert response.status_code == 500
