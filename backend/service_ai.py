import base64
import os
import json
import logging
from google import genai
from google.genai import types
from config import settings
from schemas import ContractAnalysis
from docx import Document

logger = logging.getLogger(__name__)

def analyze_contract_file(file_content: bytes, mime_type: str, file_path: str = None) -> ContractAnalysis:
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "sua-chave-gemini-aqui":
        raise Exception("API key do Gemini não configurada")
    
    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        model = "gemini-2.0-flash-exp"
        
        if mime_type == "application/pdf":
            return _analyze_pdf_file(client, model, file_content)
        else:
            return _analyze_docx_file(client, model, file_path)
            
    except Exception as e:
        logger.error(f"Erro na analise: {e}")
        raise Exception(f"Erro na análise do contrato: {str(e)}")

def _analyze_pdf_file(client, model: str, file_content: bytes) -> ContractAnalysis:
    ba64doc = base64.b64encode(file_content).decode('utf-8')
    
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_bytes(
                    mime_type="application/pdf",
                    data=base64.b64decode(ba64doc),
                ),
                types.Part.from_text(text="Analise este contrato e extraia as informações solicitadas."),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        system_instruction=[
            types.Part.from_text(text="""Analise o contrato fornecido e retorne APENAS um JSON válido com as seguintes informações:

{
    "nome_partes": "Nome das partes envolvidas no contrato",
    "valores_monetarios": "Valores monetários mencionados",
    "obrigacoes_principais": "Principais obrigações de cada parte",
    "dados_adicionais": "Objeto do contrato, vigência e outros dados importantes",
    "clausula_rescisao": "Condições de rescisão do contrato"
}

Retorne apenas o JSON, sem texto adicional."""),
        ],
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.text:
            response_text += chunk.text

    analysis_data = json.loads(response_text.strip())
    return ContractAnalysis(**analysis_data)

def _analyze_docx_file(client, model: str, file_path: str) -> ContractAnalysis:
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"Analise este contrato e extraia as informações solicitadas:\n\n{text}"),
            ],
        ),
    ]
    
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        system_instruction=[
            types.Part.from_text(text="""Analise o contrato fornecido e retorne APENAS um JSON válido com as seguintes informações:

{
    "nome_partes": "Nome das partes envolvidas no contrato",
    "valores_monetarios": "Valores monetários mencionados",
    "obrigacoes_principais": "Principais obrigações de cada parte",
    "dados_adicionais": "Objeto do contrato, vigência e outros dados importantes",
    "clausula_rescisao": "Condições de rescisão do contrato"
}

Retorne apenas o JSON, sem texto adicional."""),
        ],
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.text:
            response_text += chunk.text

    analysis_data = json.loads(response_text.strip())
    return ContractAnalysis(**analysis_data)