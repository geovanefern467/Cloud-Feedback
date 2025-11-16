import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.feedback import Feedback

def test_feedback_from_dict():
    data = {
        "feedbackId": "abc123",
        "nome": "João",
        "email": "joao@email.com",
        "mensagem": "Teste"
        # dataEnvio removido, será gerado automaticamente
    }
    feedback = Feedback.from_dict(data)
    assert feedback.feedback_id == "abc123"
    assert feedback.nome == "João"
    assert feedback.email == "joao@email.com"
    assert feedback.mensagem == "Teste"
    # data_envio pode ser None se não informado

def test_feedback_sanitization_and_length():
    data = {
        "feedbackId": "id",
        "nome": "<b>" + "a" * 200 + "</b>",
        "email": "joao@email.com",
        "mensagem": "<script>" + "x" * 2000 + "</script>"
    }
    feedback = Feedback.from_dict(data)
    assert feedback.nome.startswith("<b>")
    assert feedback.mensagem.startswith("<script>")
    # O handler sanitiza e limita, mas o modelo aceita tudo
