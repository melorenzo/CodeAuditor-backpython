import json
import logging
from groq import Groq
from app.models import CodeRequest, CodeResponse
from app.prompts import SYSTEM_PROMPT, build_audit_prompt

logger = logging.getLogger(__name__)

GROQ_MODEL = "llama-3.3-70b-versatile"


class GroqService:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    async def analyze_code(self, request: CodeRequest) -> CodeResponse:
        prompt = build_audit_prompt(request.code, request.language)

        logger.info(f"Analizando código en {request.language} ({len(request.code)} chars)")

        try:
            response = self.client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"},
                timeout=30,  # segundos
            )

            raw = response.choices[0].message.content
            logger.debug(f"Respuesta Groq: {raw[:200]}...")

            result = json.loads(raw)
            return CodeResponse(**result)

        except json.JSONDecodeError as e:
            logger.error(f"Groq devolvió JSON inválido: {e}")
            raise ValueError("La IA devolvió una respuesta mal formada")

        except KeyError as e:
            logger.error(f"Falta clave en respuesta de Groq: {e}")
            raise ValueError(f"La respuesta de la IA está incompleta: falta '{e}'")
