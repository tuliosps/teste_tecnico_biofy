# Sistema de Análise de Contratos com IA

Sistema para upload, processamento e análise automática de contratos utilizando IA (Gemini) desenvolvido com FastAPI.

## Funcionalidades

- **Autenticação JWT**: Login seguro com tokens
- **Upload de Contratos**: Suporte para PDF e DOCX
- **Análise com IA**: Extração automática de informações usando Gemini
- **Persistência**: Armazenamento em PostgreSQL
- **Consulta**: API para recuperar contratos processados

## Stack Tecnológica

- **Backend**: Python 3.13+, FastAPI
- **Banco de Dados**: PostgreSQL
- **IA**: Google Gemini API
- **Autenticação**: JWT (PyJWT)
- **Processamento**: PyPDF2, python-docx

## Configuração e Execução

### 1. Pré-requisitos

- Docker
- Python 3.13+
- Conta Google para API Gemini

### 2. Configurar API Gemini

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Gere sua chave API

### 3. configurando ambiente

1. Vai no Arquivo docker-compose.yml e preencha as variaveis do segundo serviço.
SECRET_KEY(so criar uma hash aleatoria de preferencia use alguma lib para criação da chave) ja deixei uma configurada caso não queira gerar nova
GEMINI_API_KEY(chave gemini que você acabou de gerar)

**com docker aberto na maquina**

### 4. Passo a passo no terminal

1. Primeiramente abra o terminal ja na pasta Teste_Biofy
2. Comando no terminal :
  
docker-compose up --build -d 
docker-compose logs -f backend

#o primeiro comando é pra por os conteiners do banco de dados postgres e da aplicação up, e o segundo comando é pra visualizar os logs.

### 5. Teste
Basta acessar o swagger em 
localhost:8000/docs

Primeiro tem que executar a api de login que ja esta com os valores padrões setados e pegar o token para colocar na autenticação do swagger.



