import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import json
from unittest.mock import patch, MagicMock
import pytest

@patch("handler.feedback_handler.FeedbackService")
def test_lambda_handler_success(mock_service_class):
    mock_service = MagicMock()
    mock_service.process_feedback.return_value = None
    mock_service_class.return_value = mock_service

    from handler.feedback_handler import lambda_handler  # Import inside the test

    event = {
        "body": json.dumps({
            "nome": "Geovane",
            "email": "teste@teste.com",
            "mensagem": "Teste de feedback"
        })
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    assert "Feedback recebido para: Geovane" in response["body"]

@patch("handler.feedback_handler.FeedbackService")
def test_lambda_handler_error(mock_service_class):
    mock_service = MagicMock()
    mock_service.process_feedback.side_effect = Exception("Falha")
    mock_service_class.return_value = mock_service

    from handler.feedback_handler import lambda_handler  # Import inside the test

    event = {
        "body": json.dumps({
            "nome": "Erro",
            "email": "erro@teste.com",
            "mensagem": "Mensagem"
        })
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 500
    assert "Erro ao processar feedback" in response["body"]

def test_lambda_handler_invalid_email():
    from handler.feedback_handler import lambda_handler
    event = {
        "body": json.dumps({
            "nome": "Malicioso",
            "email": "email_invalido",
            "mensagem": "Teste"
        })
    }
    response = lambda_handler(event, None)
    body = json.loads(response["body"])
    assert response["statusCode"] == 400
    assert body["error"] == "E-mail inválido."

@patch("handler.feedback_handler.FeedbackService")
@pytest.mark.parametrize("event,expected_status,expected_error", [
    ({"body": json.dumps({"nome": "", "email": "teste@teste.com", "mensagem": "Teste"})}, 400, "Nome é obrigatório."),
    ({"body": json.dumps({"nome": "João", "email": "teste@teste.com", "mensagem": ""})}, 400, "Mensagem é obrigatória."),
    ({"body": json.dumps({"nome": "João", "email": "email_invalido", "mensagem": "Teste"})}, 400, "E-mail inválido."),
])
def test_lambda_handler_invalid_fields(mock_service_class, event, expected_status, expected_error):
    from handler.feedback_handler import lambda_handler
    response = lambda_handler(event, None)
    body = json.loads(response["body"])
    assert response["statusCode"] == expected_status
    assert body["error"] == expected_error

@patch("handler.feedback_handler.FeedbackService")
def test_lambda_handler_sanitization(mock_service_class):
    mock_service = MagicMock()
    mock_service.process_feedback.return_value = None
    mock_service_class.return_value = mock_service

    from handler.feedback_handler import lambda_handler
    event = {
        "body": json.dumps({
            "nome": "<script>alert('x')</script>",
            "email": "teste@teste.com",
            "mensagem": "<b>Mensagem</b>"
        })
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "Feedback recebido para: scriptalert('x')/script" in body["message"]

def test_lambda_handler_long_fields():
    from handler.feedback_handler import lambda_handler
    long_nome = "a" * 150
    long_email = "a" * 150 + "@teste.com"
    long_mensagem = "b" * 2000
    event = {
        "body": json.dumps({
            "nome": long_nome,
            "email": long_email,
            "mensagem": long_mensagem
        })
    }
    response = lambda_handler(event, None)
    assert response["statusCode"] == 400 or response["statusCode"] == 200
    # Se email for inválido, retorna 400, senão, nome e mensagem são cortados
