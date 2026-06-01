# Backend Python - Microservicio de Análisis de Código con IA

## Tecnologías

* Python 3.11+
* FastAPI
* Groq API (modelo `llama-3.3-70b-versatile`)
* Uvicorn (servidor ASGI)
* python-dotenv
* Docker
* Docker Compose

---

## Estructura de proyecto

```text
backend-python/
├── app/
│   ├── __init__.py
│   └── main.py                # Código principal con endpoints
├── requirements.txt
├── .env                       # Contiene GROQ_API_KEY (no se sube a git)
├── Dockerfile
└── docker-compose.yml
```

---

## Endpoint principal

| Método | Endpoint   | Descripción                                       |
| ------ | ---------- | ------------------------------------------------- |
| POST   | `/analyze` | Recibe código y lenguaje, devuelve auditoría JSON |

### Formato de request

```json
{
  "code": "código fuente a analizar",
  "language": "python"
}
```

### Formato de response

```json
{
  "severity": "Crítico|Advertencia|Sugerencia",
  "vulnerabilities": [
    "vulnerabilidad1",
    "vulnerabilidad2"
  ],
  "refactored_code": "código mejorado",
  "explanation": "explicación pedagógica del problema",
  "clean_code_tips": [
    "tip1",
    "tip2"
  ]
}
```

---

## Configuración

Obtener una API Key gratuita en:

https://console.groq.com

Crear archivo `.env` en la raíz del proyecto:

```env
GROQ_API_KEY=gsk_tu_clave_aqui
```

---

## Instalación y ejecución local

### Windows (Git Bash o CMD)

```bash
cd backend-python

python -m venv venv

# Git Bash
source venv/Scripts/activate

# CMD
venv\Scripts\activate

pip install -r requirements.txt

python app/main.py
```

La API quedará disponible en:

```text
http://localhost:8000
```

---

## Requisitos (`requirements.txt`)

```text
fastapi==0.115.11
uvicorn==0.34.0
python-dotenv==1.0.1
groq==0.23.1
httpx==0.28.1
```

---

# Dockerización

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Docker Compose

Archivo `docker-compose.yml`:

```yaml
services:
  backend-python:
    build: .
    container_name: backend-python
    restart: unless-stopped

    ports:
      - "8000:8000"

    env_file:
      - .env
```

---

## Construcción manual de la imagen

```bash
docker build -t backend-python .
```

Verificar imagen creada:

```bash
docker images
```

---

## Ejecución manual del contenedor

```bash
docker run -d \
  --name backend-python \
  -p 8000:8000 \
  --env-file .env \
  backend-python
```

Ver logs:

```bash
docker logs -f backend-python
```

Detener contenedor:

```bash
docker stop backend-python
```

Eliminar contenedor:

```bash
docker rm backend-python
```

---

## Ejecución con Docker Compose

Levantar el servicio:

```bash
docker compose up -d
```

Ver logs:

```bash
docker compose logs -f
```

Detener el servicio:

```bash
docker compose down
```

Reconstruir la imagen luego de cambios:

```bash
docker compose up -d --build
```

Ver estado:

```bash
docker compose ps
```

---

## Acceso a la API

Una vez iniciado el servicio:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

Documentación ReDoc:

```text
http://localhost:8000/redoc
```

---

## Prueba exitosa (SQL Injection)

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"code":"query = \"SELECT * FROM users WHERE id = \" + input", "language":"python"}'
```

### Respuesta obtenida

```json
{
  "severity": "Crítico",
  "vulnerabilities": [
    "Inyección SQL"
  ],
  "refactored_code": "query = 'SELECT * FROM users WHERE id = %s'; cursor.execute(query, (input,))",
  "explanation": "El código original es vulnerable a inyección SQL ya que concatena directamente la entrada del usuario dentro de la consulta.",
  "clean_code_tips": [
    "Utilizar parámetros en consultas SQL",
    "Validar y sanitizar las entradas del usuario"
  ]
}
```

---

## Modelo de IA

Se utiliza:

```text
llama-3.3-70b-versatile
```

Configuración recomendada:

```python
temperature=0.2
```

Para forzar respuestas JSON válidas:

```python
response_format={"type": "json_object"}
```

---

## Ventajas de Docker

* Entorno reproducible en cualquier sistema operativo.
* No requiere instalar Python ni dependencias en el host.
* Facilita el despliegue en servidores Linux.
* Simplifica la integración con CI/CD.
* Aísla dependencias y versiones.
* Permite escalar fácilmente con Docker Compose o Kubernetes.
* Reduce problemas de compatibilidad entre entornos.
* Facilita la migración entre desarrollo, testing y producción.
