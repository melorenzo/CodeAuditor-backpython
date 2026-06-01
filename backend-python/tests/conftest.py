import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app
from app.models import CodeResponse


# Respuesta mock que simula lo que devolvería Groq
MOCK_RESPONSE = CodeResponse(
    severity="Crítico",
    vulnerabilities=["Inyección de comandos", "Falta de validación de input"],
    refactored_code="def safe():\n    pass",
    explanation="El código original permite inyección de comandos.",
    clean_code_tips=["Validar inputs", "Usar subprocess con lista de args"]
)


@pytest.fixture
def client():
    """Cliente de test para FastAPI."""
    return TestClient(app)


@pytest.fixture
def mock_groq_service():
    """Mockea GroqService para no llamar a la API real en tests."""
    with patch("app.main.groq_service") as mock:
        mock.analyze_code = MagicMock(return_value=MOCK_RESPONSE)
        yield mock
