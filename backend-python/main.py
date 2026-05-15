# -*- coding: utf-8 -*-
import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI(title="Code Auditor Service", description="Audita código usando Groq")

# Cliente Groq
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY no está definida en el archivo .env")
client = Groq(api_key=api_key)

class CodeRequest(BaseModel):
    code: str
    language: str

class CodeResponse(BaseModel):
    severity: str   # "Crítico", "Advertencia", "Sugerencia"
    vulnerabilities: list[str]
    refactored_code: str
    explanation: str
    clean_code_tips: list[str]

@app.get("/")
def root():
    return {"message": "Code Auditor Service (Groq) - OK"}

@app.post("/analyze", response_model=CodeResponse)
async def analyze(request: CodeRequest):
    prompt = f"""Actúa como un Senior Developer experto en seguridad y clean code.
Analiza el siguiente código en {request.language}:

{request.code}

Debes responder ÚNICAMENTE con un JSON válido (sin texto adicional fuera del JSON) con esta estructura exacta:
{{
  "severity": "Crítico|Advertencia|Sugerencia",
  "vulnerabilities": ["vuln1", "vuln2"],
  "refactored_code": "código mejorado aquí",
  "explanation": "explicación pedagógica del problema",
  "clean_code_tips": ["tip1", "tip2"]
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Eres un auditor de código. Siempre respondes en JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        # validar que tenga todas las claves esperadas
        return CodeResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error con Groq: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)