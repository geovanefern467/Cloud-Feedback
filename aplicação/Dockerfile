# Usa a imagem base da AWS Lambda para Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Instala dependências
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt

# Copia o código da Lambda para o diretório de trabalho padrão
COPY backend ./

# Define o handler (ajuste o caminho conforme seu arquivo principal)
CMD ["mock_lambda.handler.feedback_handler_mock.lambda_handler"]
