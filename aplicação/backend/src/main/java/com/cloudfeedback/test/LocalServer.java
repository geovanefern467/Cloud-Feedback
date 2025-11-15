// src/main/java/com/cloudfeedback/test/LocalServer.java
package com.cloudfeedback.test;

import com.cloudfeedback.model.Feedback;
import com.cloudfeedback.service.FeedbackService;
import com.google.gson.Gson;
import spark.Spark;

public class LocalServer {
    public static void main(String[] args) {
        Spark.port(8080);
        FeedbackService service = new FeedbackService();
        Gson gson = new Gson();

        Spark.post("/feedback", (req, res) -> {
            Feedback feedback = gson.fromJson(req.body(), Feedback.class);
            service.processFeedback(feedback);
            res.type("application/json");
            return gson.toJson("Feedback recebido com sucesso");
        });
    }
}
