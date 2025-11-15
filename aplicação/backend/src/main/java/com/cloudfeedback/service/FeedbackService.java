package com.cloudfeedback.service;

import com.cloudfeedback.model.Feedback;
import java.util.UUID;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;
import com.amazonaws.services.dynamodbv2.document.DynamoDB;
import com.amazonaws.services.dynamodbv2.document.Table;
import com.amazonaws.services.dynamodbv2.document.Item;
import com.amazonaws.services.sns.AmazonSNS;
import com.amazonaws.services.sns.AmazonSNSClientBuilder;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class FeedbackService {

    private static final Logger logger = LoggerFactory.getLogger(FeedbackService.class);

    private final DynamoDB dynamoDB;
    private final Table feedbackTable;
    private final AmazonSNS snsClient;
    private final String snsTopicArn = "arn:aws:sns:sa-east-1:120726684266:feedback-topic";

    public FeedbackService() {
        AmazonDynamoDB client = AmazonDynamoDBClientBuilder.standard().build();
        this.dynamoDB = new DynamoDB(client);
        this.feedbackTable = dynamoDB.getTable("Feedbacks");
        this.snsClient = AmazonSNSClientBuilder.standard().build();
    }

    public void processFeedback(Feedback feedback) {
        try {
            // Gerar UUID
            feedback.setFeedbackId(UUID.randomUUID().toString());

            // Preencher dataEnvio se vier nulo
            if (feedback.getDataEnvio() == null || feedback.getDataEnvio().isBlank()) {
                String agora = LocalDateTime.now().format(DateTimeFormatter.ISO_DATE_TIME);
                feedback.setDataEnvio(agora);
            }

            // Salvar no DynamoDB
            feedbackTable.putItem(new Item()
                    .withPrimaryKey("feedback_id", feedback.getFeedbackId())
                    .withString("nome", feedback.getNome())
                    .withString("email", feedback.getEmail())
                    .withString("mensagem", feedback.getMensagem())
                    .withString("data_envio", feedback.getDataEnvio())
            );

            // Enviar notificação SNS
            String mensagem = "Novo feedback de " + feedback.getNome() + ": " + feedback.getMensagem();
            snsClient.publish(snsTopicArn, mensagem, "Novo feedback recebido");

        } catch (Exception e) {
            // Logar erro para CloudWatch
            logger.error("Erro ao processar feedback: {}", e.getMessage(), e);
            // Aqui você pode lançar uma RuntimeException para que a Lambda retorne 500
            throw new RuntimeException("Falha ao processar feedback", e);
        }
    }
}
