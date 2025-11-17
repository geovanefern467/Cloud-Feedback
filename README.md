# Cloud Feedback

Sistema completo para coleta de feedbacks via web, utilizando AWS Lambda como backend serverless, Python para lógica de negócio, frontend em HTML/JS, testes automatizados, simulação local com Docker e integração com AWS (DynamoDB/SNS).

---

## 📦 Estrutura do Projeto

```
aplicação/
├── backend/
│   ├── handler/
│   │   └── feedback_handler.py
│   ├── model/
│   │   └── feedback.py
│   ├── service/
│   │   └── feedback_service.py
│   ├── test/
│   │   ├── test_feedback.py
│   │   ├── test_feedback_handler.py
│   │   ├── test_feedback_service.py
│   │   └── test_lambda.py
│   └── requirements.txt
├── docs/
│   └── Arquitetura_Cloud_Feedback.png
├── frontend/
│   ├── index.html
│   └── main.js
├── mock_lambda/
│   ├── handler/
│   │   └── feedback_handler_mock.py
│   └── service/
│       └── feedback_service_mock.py
├── .gitignore
├── Dockerfile
└── docker-compose.yml
```

---

## 🖼️ Arquitetura

![Arquitetura Cloud Feedback](/aplicação/docs/Arquitetura_Cloud_Feedback.png)

---

## 🖥️ Frontend

- **frontend/index.html**  
  Página web para envio de feedbacks.
- **frontend/main.js**  
  Validação de campos, integração com API, UX responsiva.

## 🐍 Backend (AWS Lambda)

- **backend/handler/feedback_handler.py**  
  Função Lambda principal.  
  - Recebe requisições, valida dados, instancia modelos, chama o serviço de negócio e retorna resposta.
- **backend/model/feedback.py**  
  Define o modelo de dados `Feedback` (campos, métodos utilitários).
- **backend/service/feedback_service.py**  
  Implementa a lógica de negócio:  
  - Salva feedback no DynamoDB.
  - Publica notificação no SNS.
- **backend/test/**  
  Testes unitários e de integração para cada camada do backend.
- **backend/requirements.txt**  
  Lista de dependências Python para o backend.

## 🧪 Mock & Simulação

- **mock_lambda/handler/feedback_handler_mock.py**  
  Handler alternativo para simulação local (não acessa AWS real).
- **mock_lambda/service/feedback_service_mock.py**  
  Serviço mock: apenas loga ações, útil para testes sem AWS.

## 🐳 Docker & LocalStack

- **Dockerfile**  
  Containeriza a Lambda Python para testes locais.
- **docker-compose.yml**  
  Orquestra containers:
  - `lambda-local`: roda a Lambda (real ou mock).
  - `localstack`: simula serviços AWS (DynamoDB, SNS).

## 📄 docs

- **docs/Arquitetura_Cloud_Feedback.png**  
  Imagem salva do Diagrama da arquitetura do sistema.

## ⚙️ .gitignore

- Ignora arquivos sensíveis, dependências, configs de IDE, etc.

---

## 🚀 Como rodar localmente

1. **Build e start dos containers**
   ```sh
   docker-compose build
   docker-compose up
   ```

2. **Testar Lambda local**
   ```sh
   curl -X POST http://localhost:9000/2015-03-31/functions/function/invocations \
     -H "Content-Type: application/json" \
     -d '{"body": "{\"nome\": \"Teste\", \"email\": \"teste@email.com\", \"mensagem\": \"Mensagem de teste\"}"}'
   ```

3. **Acessar frontend**
   - Abra `frontend/index.html` no navegador.

4. **Testes**
   - Execute os testes Python na pasta `backend/test`.

---

## 📝 Observações

- O código real do backend nunca é alterado para testes; mocks ficam em `mock_lambda`.
- Para simular AWS, use LocalStack (já configurado no docker-compose).
- Para produção, use apenas o handler e serviço reais.
- Documentação e diagramas estão em `docs/`.

---

## 👨‍💻 Autor

**Geovane Ribeiro.**

---

## 🏗️ Contribuição

Sinta-se livre para abrir issues, sugerir melhorias ou enviar PRs!
