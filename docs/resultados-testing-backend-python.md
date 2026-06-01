#  Resultados de Testing Backend Python

## Ejecución de Tests con Pytest

Se ejecutó la suite completa de pruebas automatizadas del backend Python dentro del contenedor Docker `auditoria-python`.

###  Comando utilizado

```bash
docker exec -it auditoria-python sh -c "cd /app && python -m pytest -v"
```

---

# Resumen General

| Métrica | Resultado |
|---|---|
| Total de tests | 23 |
| Tests aprobados | 23  |
| Tests fallidos | 0  |
| Tiempo de ejecución | 0.10s  |
| Cobertura principal | Endpoints, validaciones y modelos |

---

# Estructura de Tests Ejecutados

## `tests/test_analyze.py`

Pruebas relacionadas al endpoint de análisis de código.

| Test | Estado |
|---|---|
| `test_analyze_success` |  PASSED |
| `test_analyze_all_languages` |  PASSED |
| `test_analyze_response_structure` |  PASSED |
| `test_analyze_empty_code` |  PASSED |
| `test_analyze_whitespace_only_code` |  PASSED |
| `test_analyze_code_too_long` |  PASSED |
| `test_analyze_unsupported_language` |  PASSED |
| `test_analyze_missing_code_field` |  PASSED |
| `test_analyze_missing_language_field` |  PASSED |
| `test_analyze_empty_body` |  PASSED |
| `test_analyze_groq_value_error` |  PASSED |
| `test_analyze_groq_unexpected_error` |  PASSED |

### Cobertura validada

- Análisis exitoso de código
- Compatibilidad multi lenguaje
- Validación de estructura JSON
- Manejo de errores
- Validaciones de entrada
- Control de payloads inválidos
- Manejo de excepciones del servicio Groq

---

## `tests/test_health.py`

Pruebas de salud de la API.

| Test | Estado |
|---|---|
| `test_root` |  PASSED |
| `test_health` |  PASSED |

### Cobertura validada

- Endpoint raíz operativo
- Endpoint `/health` funcionando correctamente
- Estado general de la API

---

## `tests/test_models.py`

Pruebas de validación de modelos Pydantic.

| Test | Estado |
|---|---|
| `test_code_request_valid` |  PASSED |
| `test_code_request_language_case_insensitive` |  PASSED |
| `test_code_request_code_stripped` |  PASSED |
| `test_code_request_empty_code_raises` |  PASSED |
| `test_code_request_whitespace_code_raises` |  PASSED |
| `test_code_request_code_too_long_raises` |  PASSED |
| `test_code_request_invalid_language_raises` |  PASSED |
| `test_code_response_valid` |  PASSED |
| `test_code_response_invalid_severity_fallback` |  PASSED |

### Cobertura validada

- Validaciones Pydantic
- Sanitización de inputs
- Normalización de lenguaje
- Restricciones de tamaño
- Validación de severidad
- Manejo de datos inválidos

---

# Warning Detectado

Durante la ejecución apareció el siguiente warning relacionado con `pytest-asyncio`:

```text
PytestDeprecationWarning: The configuration option
"asyncio_default_fixture_loop_scope" is unset.
```

## Recomendación

Agregar la siguiente configuración en `pytest.ini` para evitar problemas futuros de compatibilidad:

```ini
[pytest]
asyncio_mode = strict
asyncio_default_fixture_loop_scope = function
```

---

# Entorno de Ejecución

| Componente | Versión |
|---|---|
| Python | 3.11.15 |
| pytest | 8.3.5 |
| pytest-asyncio | 0.24.0 |
| Docker |  |
| Sistema operativo contenedor | Linux |

---




