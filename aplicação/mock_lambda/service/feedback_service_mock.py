import uuid
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedbackServiceMock:
    def __init__(self):
        logger.info("FeedbackServiceMock inicializado (sem AWS).")

    def process_feedback(self, feedback):
        try:
            feedback_id = getattr(feedback, 'feedback_id', None) or str(uuid.uuid4())
            data_envio = getattr(feedback, 'data_envio', None) or datetime.now().isoformat()
            logger.info(f"[MOCK] Feedback recebido: {feedback_id} | Nome: {getattr(feedback, 'nome', '')}")
            logger.info(f"[MOCK] Email: {getattr(feedback, 'email', '')}")
            logger.info(f"[MOCK] Mensagem: {getattr(feedback, 'mensagem', '')}")
            logger.info(f"[MOCK] Data de envio: {data_envio}")
            logger.info(f"[MOCK] Simulando publicação no SNS: Novo feedback de {getattr(feedback, 'nome', '')}: {getattr(feedback, 'mensagem', '')}")
            response = {"MessageId": str(uuid.uuid4()), "Status": "MOCKED"}
            logger.info(f"[MOCK] SNS publish response: {response}")
        except Exception as e:
            logger.error(f"[MOCK] Erro ao processar feedback: {e}", exc_info=True)
            raise
