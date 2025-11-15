# Usa a imagem base da AWS Lambda para Java 17
FROM public.ecr.aws/lambda/java:17

# Copia o fat JAR gerado pelo Maven para o diretório de trabalho da Lambda
COPY backend/target/feedback-lambda-1.0-SNAPSHOT-all.jar ${LAMBDA_TASK_ROOT}/app.jar

# Define o handler correto
# O formato é "package.ClassName::methodName"
# No seu caso, a classe é FeedbackHandler e o método é handleRequest
CMD ["com.cloudfeedback.handler.FeedbackHandler::handleRequest"]
