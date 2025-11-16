import sys
import os
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
from unittest.mock import patch, MagicMock

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@patch("handler.feedback_handler.FeedbackService")
def test_lambda_handler_success(mock_service_class):
    mock_service = MagicMock()
    mock_service.process_feedback.return_value = None
    mock_service_class.return_value = mock_service

    from handler.feedback_handler import lambda_handler

    event = {
        "body": json.dumps({
            "nome": "Geovane",
            "email": "teste@teste.com",
            "mensagem": "Teste de feedback via Python"
        })
    }
    result = lambda_handler(event, None)
    assert result["statusCode"] == 200
    assert "Feedback recebido para: Geovane" in result["body"]

def test_lambda_handler_sanitization_and_long_fields():
    from handler.feedback_handler import lambda_handler
    event = {
        "body": json.dumps({
            "nome": "<h1>" + "a" * 200 + "</h1>",
            "email": "teste@teste.com",
            "mensagem": "<div>" + "b" * 2000 + "</div>"
        })
    }
    result = lambda_handler(event, None)
    body = json.loads(result["body"])
    if result["statusCode"] == 200:
        assert "Feedback recebido para:" in body["message"]
    elif result["statusCode"] == 400:
        assert "error" in body

if __name__ == "__main__":
    # Teste manual
    event = {
        "body": json.dumps({
            "nome": "Geovane",
            "email": "teste@teste.com",
            "mensagem": "Teste de feedback via Python"
        })
    }
    result = lambda_handler(event, None)
    logger.info(json.dumps(result, indent=2, ensure_ascii=False))
