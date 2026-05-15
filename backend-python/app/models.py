from pydantic import BaseModel, field_validator

SUPPORTED_LANGUAGES = {"python", "java", "javascript", "typescript", "go", "rust", "c", "cpp"}
MAX_CODE_LENGTH = 10_000  # caracteres


class CodeRequest(BaseModel):
    code: str
    language: str

    @field_validator("code")
    @classmethod
    def code_not_empty(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El código no puede estar vacío")
        if len(v) > MAX_CODE_LENGTH:
            raise ValueError(f"El código supera el límite de {MAX_CODE_LENGTH} caracteres")
        return v

    @field_validator("language")
    @classmethod
    def language_supported(cls, v):
        v = v.strip().lower()
        if v not in SUPPORTED_LANGUAGES:
            raise ValueError(f"Lenguaje no soportado. Soportados: {', '.join(sorted(SUPPORTED_LANGUAGES))}")
        return v


class CodeResponse(BaseModel):
    severity: str           # "Crítico", "Advertencia", "Sugerencia"
    vulnerabilities: list[str]
    refactored_code: str
    explanation: str
    clean_code_tips: list[str]

    @field_validator("severity")
    @classmethod
    def severity_valid(cls, v):
        allowed = {"Crítico", "Advertencia", "Sugerencia"}
        if v not in allowed:
            return "Advertencia"  # fallback en lugar de explotar
        return v
