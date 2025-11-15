package com.cloudfeedback.handler;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.Map;
import java.util.HashMap;
import com.cloudfeedback.service.FeedbackService;
import com.cloudfeedback.model.Feedback;

public class FeedbackHandler implements RequestHandler<Map<String,Object>, Map<String,Object>> {
    private final FeedbackService service = new FeedbackService();
    private final ObjectMapper mapper = new ObjectMapper();

    @Override
    public Map<String,Object> handleRequest(Map<String,Object> event, Context context) {
        Map<String, String> headers = new HashMap<>();
        headers.put("Content-Type", "application/json");
        headers.put("Access-Control-Allow-Origin", "*");
        headers.put("Access-Control-Allow-Headers", "Content-Type");
        headers.put("Access-Control-Allow-Methods", "POST,OPTIONS");

        try {
            // Parse do body
            String bodyStr = (String) event.get("body");
            Feedback feedback = mapper.readValue(bodyStr, Feedback.class);

            service.processFeedback(feedback);

            return Map.of(
                "statusCode", 200,
                "headers", headers,
                "body", "{\"message\":\"Feedback recebido para: " + feedback.getNome() + "\"}"
            );
        } catch (Exception e) {
            e.printStackTrace();
            return Map.of(
                "statusCode", 500,
                "headers", headers,
                "body", "{\"error\":\"Erro ao processar feedback: " + e.getMessage() + "\"}"
            );
        }
    }
}
