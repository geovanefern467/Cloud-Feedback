import uuid
from datetime import datetime
import boto3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeedbackService:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('Feedbacks')
        self.sns = boto3.client('sns')
        self.sns_topic_arn = 'arn:aws:sns:sa-east-1:120726684266:feedback-topic'

    def process_feedback(self, feedback):
        try:
            feedback_id = feedback.feedback_id or str(uuid.uuid4())
            data_envio = feedback.data_envio or datetime.now().isoformat()
            logger.info(f"Inserindo feedback no DynamoDB: {feedback_id} | Nome: {feedback.nome}")
            self.table.put_item(Item={
                'feedback_id': feedback_id,
                'nome': feedback.nome,
                'email': feedback.email,
                'mensagem': feedback.mensagem,
                'data_envio': data_envio
            })
            assunto = "Novo feedback recebido"
            mensagem_sns = f"Novo feedback de {feedback.nome}:\n\n{feedback.mensagem}"
            logger.info(f"Publicando feedback no SNS: {self.sns_topic_arn}")
            response = self.sns.publish(
                TopicArn=self.sns_topic_arn,
                Message=mensagem_sns,
                Subject=assunto
            )
            logger.info(f"SNS publish response: {response}")
        except Exception as e:
            logger.error(f"Erro ao processar feedback: {e}", exc_info=True)
            raise
