from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class Feedback:
    feedback_id: Optional[str] = None
    nome: Optional[str] = None
    email: Optional[str] = None
    mensagem: Optional[str] = None
    data_envio: Optional[str] = None

    @staticmethod
    def from_dict(data):
        feedback = Feedback(
            feedback_id=data.get('feedbackId'),
            nome=data.get('nome'),
            email=data.get('email'),
            mensagem=data.get('mensagem'),
            data_envio=data.get('dataEnvio') or data.get('data_envio')
        )
        logger.info(f"Feedback criado: {feedback}")
        return feedback
