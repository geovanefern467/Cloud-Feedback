package com.cloudfeedback.test;

import com.cloudfeedback.handler.FeedbackHandler;
import com.cloudfeedback.model.Feedback;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.CognitoIdentity;
import com.amazonaws.services.lambda.runtime.ClientContext;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.fasterxml.jackson.databind.ObjectMapper;

public class TestLambda {
    public static void main(String[] args) {
        FeedbackHandler handler = new FeedbackHandler();
        Feedback feedback = new Feedback();
        feedback.setNome("Geovane");
        feedback.setEmail("teste@teste.com");
        feedback.setMensagem("Teste de feedback");

        ObjectMapper mapper = new ObjectMapper();
        String feedbackJson;
        try {
            feedbackJson = mapper.writeValueAsString(feedback);
        } catch (Exception e) {
            throw new RuntimeException("Erro ao serializar feedback", e);
        }

        java.util.Map<String, Object> event = new java.util.HashMap<>();
        event.put("body", feedbackJson);

        java.util.Map<String, Object> resultado = handler.handleRequest(event, new Context() {
            public String getAwsRequestId() { return "test-request"; }
            public String getLogGroupName() { return "test-log"; }
            public String getLogStreamName() { return "test-stream"; }
            public String getFunctionName() { return "test-function"; }
            public String getFunctionVersion() { return "1.0"; }
            public String getInvokedFunctionArn() { return "test-arn"; }
            public CognitoIdentity getIdentity() { return null; }
            public ClientContext getClientContext() { return null; }
            public int getRemainingTimeInMillis() { return 3000; }
            public int getMemoryLimitInMB() { return 512; }
            public LambdaLogger getLogger() { 
                return new LambdaLogger() {
                    @Override
                    public void log(String message) {
                        System.out.println(message);
                    }
                    @Override
                    public void log(byte[] message) {
                        System.out.println(new String(message));
                    }
                };
            }
        });

        try {
            System.out.println("RESULTADO: " + mapper.writeValueAsString(resultado));
        } catch (Exception e) {
            System.out.println("Erro ao serializar resultado: " + e.getMessage());
        }
    }
}
