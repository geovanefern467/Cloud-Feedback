import json
import re
import logging
from datetime import datetime
from service.feedback_service import FeedbackService
from model.feedback import Feedback


logger = logging.getLogger(__name__)

# FLUXO PRINCIPAL
def lambda_handler(event, context):
    try:
        data = parse_body(event)
        error = validate_fields(data)
        if error:
            logger.warning(f"Validação falhou: {error} | Dados recebidos: {data}")
            return error_response(error, 400)

        feedback = build_feedback(data)
        process_feedback(feedback)
    
        logger.info(f"Feedback recebido com sucesso para: {feedback.nome}")
        return success_response(feedback.nome)

    except Exception as e:
        error_message = str(e)
        logger.error(f"Erro inesperado ao processar feedback: {error_message}", exc_info=True)
        return error_response(f"Erro ao processar feedback: {error_message}", 500)




# FUNÇÕES DA REGRA DE NEGÓCIO
def parse_body(event):
    """Converte o body da requisição em dicionário."""
    body = event.get("body")

    if isinstance(body, str):
        return json.loads(body)

    return body or {}


def validate_fields(data):
    """Valida os campos obrigatórios do feedback. Retorna mensagem de erro ou None."""
    nome = sanitize_text(data.get("nome", ""), 100)
    email = sanitize_text(data.get("email", ""), 100)
    mensagem = sanitize_text(data.get("mensagem", ""), 1000)

    if not nome:
        return "Nome é obrigatório."
    if not mensagem:
        return "Mensagem é obrigatória."
    if not is_valid_email(email):
        return "E-mail inválido."
    return None


def build_feedback(data):
    """Cria objeto Feedback sanitizado e pronto para uso."""
    return Feedback.from_dict({
        "nome": sanitize_text(data.get("nome", ""), 100),
        "email": sanitize_text(data.get("email", ""), 100),
        "mensagem": sanitize_text(data.get("mensagem", ""), 1000),
        "dataEnvio": datetime.utcnow().isoformat()
    })


def process_feedback(feedback):
    """Chama o serviço responsável por processar o feedback."""
    service = FeedbackService()
    service.process_feedback(feedback)



# FUNÇÕES DE RESPOSTA
def success_response(nome):
    return {
        "statusCode": 200,
        "headers": default_headers(),
        "body": json.dumps({"message": f"Feedback recebido para: {nome}"})
    }


def error_response(message, status_code=400):
    return {
        "statusCode": status_code,
        "headers": default_headers(),
        "body": json.dumps({"error": message})
    }




# FUNÇÕES AUXILIARES
def default_headers():
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "POST,OPTIONS"
    }


def is_valid_email(email: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))


def sanitize_text(text: str, max_length: int) -> str:
    if not isinstance(text, str):
        return ""
    cleaned = re.sub(r"[<>]", "", text.strip())
    return cleaned[:max_length]
