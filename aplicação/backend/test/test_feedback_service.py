import sys
import os
import logging
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from unittest.mock import MagicMock, patch
from model.feedback import Feedback
from service.feedback_service import FeedbackService

@patch("service.feedback_service.boto3")
def test_process_feedback_success(mock_boto3):
    mock_table = MagicMock()
    mock_dynamodb = MagicMock()
    mock_dynamodb.Table.return_value = mock_table
    mock_sns = MagicMock()
    mock_boto3.resource.return_value = mock_dynamodb
    mock_boto3.client.return_value = mock_sns

    service = FeedbackService()
    feedback = Feedback(
        nome="Teste",
        email="teste@email.com",
        mensagem="Mensagem de teste"
    )

    logger.info("Executando test_process_feedback_success")
    service.process_feedback(feedback)

    assert mock_table.put_item.called
    assert mock_sns.publish.called
