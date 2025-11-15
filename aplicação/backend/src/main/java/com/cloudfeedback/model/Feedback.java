package com.cloudfeedback.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Feedback {
    private String feedbackId;
    private String nome;
    private String email;
    private String mensagem;

    @JsonProperty("dataEnvio")
    private String dataEnvio;

    public String getFeedbackId() { return feedbackId; }
    public void setFeedbackId(String feedbackId) { this.feedbackId = feedbackId; }

    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getMensagem() { return mensagem; }
    public void setMensagem(String mensagem) { this.mensagem = mensagem; }

    public String getDataEnvio() { return dataEnvio; }
    public void setDataEnvio(String dataEnvio) { this.dataEnvio = dataEnvio; }
}
