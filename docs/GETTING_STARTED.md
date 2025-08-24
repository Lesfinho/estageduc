# Primeiros Passos - Plataforma Estagiários

## 🚀 Setup Inicial (1-2 horas)

### Pré-requisitos
- Docker e Docker Compose instalados
- Git instalado
- Editor de código (VS Code recomendado)

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd estagiarios-platform
```

### 2. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```bash
# Backend
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=postgresql://user:password@localhost:5432/estagiarios

# WhatsApp (opcional)
TWILIO_ACCOUNT_SID=seu-account-sid
TWILIO_AUTH_TOKEN=seu-auth-token
TWILIO_WHATSAPP_NUMBER=seu-numero-whatsapp
```

### 3. Execute com Docker
```bash
docker-compose up --build
```

### 4. Acesse a aplicação
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

## 🏗️ Estrutura do Projeto

### Backend (Python - FastAPI)
- **Localização**: `./backend/`
- **Framework**: FastAPI
- **Banco de dados**: PostgreSQL (SQLite para desenvolvimento)
- **Autenticação**: JWT
- **WebSocket**: Chat em tempo real

### Frontend (React + TypeScript)
- **Localização**: `./frontend/`
- **Framework**: React 18
- **Linguagem**: TypeScript
- **Roteamento**: React Router
- **Estado**: React Query + Context API

### Banco de Dados
- **Desenvolvimento**: SQLite (padrão)
- **Produção**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrações**: Alembic

## 🔧 Desenvolvimento

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Banco de Dados
```bash
# Para desenvolvimento (SQLite)
# O banco será criado automaticamente

# Para produção (PostgreSQL)
docker-compose up db
```

## 📱 Funcionalidades Principais

### 1. Sistema de Autenticação
- Registro de usuários
- Login com JWT
- Perfil de usuário

### 2. Chat Colaborativo
- Mensagens em tempo real
- WebSocket para comunicação
- Histórico de mensagens

### 3. Planner Colaborativo
- Quadro Kanban (To Do, Doing, Done)
- Criação e gerenciamento de tarefas
- Drag & Drop para mudança de status
- Prioridades e prazos

### 4. Integração WhatsApp
- Notificações automáticas
- Lembretes de tarefas
- API Twilio

## 🐛 Troubleshooting

### Problemas comuns

#### Backend não inicia
```bash
# Verifique se as portas estão livres
netstat -an | grep 8000

# Verifique os logs
docker-compose logs backend
```

#### Frontend não carrega
```bash
# Verifique se o backend está rodando
curl http://localhost:8000/health

# Verifique os logs
docker-compose logs frontend
```

#### Banco de dados não conecta
```bash
# Verifique se o PostgreSQL está rodando
docker-compose ps db

# Verifique os logs
docker-compose logs db
```

### Logs e Debug
```bash
# Todos os serviços
docker-compose logs

# Serviço específico
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db

# Logs em tempo real
docker-compose logs -f
```

## 📚 Próximos Passos

1. **Explore a API**: Acesse http://localhost:8000/docs
2. **Teste o frontend**: Navegue pelas páginas
3. **Crie um usuário**: Teste o sistema de autenticação
4. **Envie mensagens**: Teste o chat
5. **Crie tarefas**: Teste o planner

## 🤝 Contribuindo

Veja o arquivo [CONTRIBUTING.md](../CONTRIBUTING.md) para detalhes sobre como contribuir com o projeto.

## 📞 Suporte

- **Issues**: Use o GitHub Issues
- **Documentação**: Consulte esta pasta `docs/`
- **API**: Use o Swagger em `/docs`

