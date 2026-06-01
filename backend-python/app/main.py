# -*- coding: utf-8 -*-
import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.models import CodeRequest, CodeResponse
from app.services.groq_service import GroqService

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Validar API key al arrancar
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY no está definida en el archivo .env")

groq_service = GroqService(api_key=api_key)

app = FastAPI(
    title="Code Auditor Service",
    description="Audita código usando Groq + LLaMA",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "Code Auditor Service"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/analyze", response_model=CodeResponse)
async def analyze(request: CodeRequest):
    try:
        return await groq_service.analyze_code(request)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Error inesperado en /analyze: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno al procesar el análisis")
