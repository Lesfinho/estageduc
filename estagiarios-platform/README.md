# 🚀 Plataforma Estagiários

Uma plataforma colaborativa open source para estagiários se conectarem, compartilharem experiências e gerenciarem projetos juntos.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![React](https://img.shields.io/badge/React-18.0+-blue.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9+-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ Funcionalidades

- 🔐 **Autenticação JWT** - Sistema seguro de login e registro
- 💬 **Chat Colaborativo** - Comunicação em tempo real via WebSocket
- 📋 **Planner Colaborativo** - Quadro Kanban para gerenciar tarefas
- 📱 **Integração WhatsApp** - Notificações automáticas via Twilio
- 👥 **Gestão de Usuários** - Perfis e configurações personalizadas
- 🎨 **Interface Moderna** - Design responsivo e intuitivo

## 🏗️ Arquitetura

### Backend
- **Framework**: FastAPI (Python)
- **Banco de Dados**: PostgreSQL + SQLAlchemy
- **Autenticação**: JWT com Passlib
- **WebSocket**: Chat em tempo real
- **Validação**: Pydantic

### Frontend
- **Framework**: React 18 + TypeScript
- **Roteamento**: React Router
- **Estado**: React Query + Context API
- **UI**: Componentes customizados + Lucide Icons
- **Estilização**: CSS Modules

## 🚀 Quick Start

### Com Docker (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/estagiarios-platform.git
cd estagiarios-platform

# 2. Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env

# 3. Execute com Docker
docker-compose up --build

# 4. Acesse a aplicação
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Desenvolvimento Local

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (em outro terminal)
cd frontend
npm install
npm start
```

## 📱 Screenshots

### Dashboard
![Dashboard](docs/images/dashboard.png)

### Chat
![Chat](docs/images/chat.png)

### Planner
![Planner](docs/images/planner.png)

## 🛠️ Tecnologias

### Backend
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno e rápido
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para Python
- [PostgreSQL](https://www.postgresql.org/) - Banco de dados relacional
- [JWT](https://jwt.io/) - Autenticação stateless
- [WebSockets](https://websockets.readthedocs.io/) - Comunicação em tempo real

### Frontend
- [React](https://reactjs.org/) - Biblioteca para interfaces
- [TypeScript](https://www.typescriptlang.org/) - JavaScript tipado
- [React Router](https://reactrouter.com/) - Roteamento
- [React Query](https://tanstack.com/query) - Gerenciamento de estado
- [Lucide Icons](https://lucide.dev/) - Ícones modernos

### DevOps
- [Docker](https://www.docker.com/) - Containerização
- [Docker Compose](https://docs.docker.com/compose/) - Orquestração
- [GitHub Actions](https://github.com/features/actions) - CI/CD

## 📚 Documentação

- [🚀 Primeiros Passos](docs/GETTING_STARTED.md)
- [📝 Diretrizes de Código](docs/CODING_GUIDELINES.md)
- [🔌 API Reference](http://localhost:8000/docs)
- [🤝 Contribuindo](CONTRIBUTING.md)

## 🎯 Casos de Uso

### Para Estagiários
- Conectar com outros estagiários
- Compartilhar experiências e dicas
- Gerenciar projetos pessoais
- Receber notificações importantes

### Para Empresas
- Gerenciar equipes de estagiários
- Acompanhar progresso de projetos
- Facilitar comunicação interna
- Integrar com ferramentas existentes

### Para Educadores
- Acompanhar progresso dos alunos
- Facilitar colaboração em projetos
- Integrar com sistemas educacionais

## 🔧 Configuração

### Variáveis de Ambiente

```bash
# Backend
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=postgresql://user:password@localhost:5432/estagiarios

# WhatsApp (opcional)
TWILIO_ACCOUNT_SID=seu-account-sid
TWILIO_AUTH_TOKEN=seu-auth-token
TWILIO_WHATSAPP_NUMBER=seu-numero-whatsapp
```

### Banco de Dados

O projeto suporta tanto SQLite (desenvolvimento) quanto PostgreSQL (produção):

```bash
# Desenvolvimento (SQLite)
# O banco será criado automaticamente

# Produção (PostgreSQL)
docker-compose up db
```

## 🧪 Testes

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

## 🚀 Deploy

### Produção

```bash
# 1. Configure variáveis de produção
export DATABASE_URL="postgresql://user:pass@host:5432/db"
export SECRET_KEY="chave-super-secreta"

# 2. Build e deploy
docker-compose -f docker-compose.prod.yml up --build
```

### Heroku

```bash
# 1. Configure o Heroku CLI
heroku create estagiarios-platform

# 2. Configure variáveis
heroku config:set DATABASE_URL="postgresql://..."
heroku config:set SECRET_KEY="..."

# 3. Deploy
git push heroku main
```

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Veja nosso [guia de contribuição](CONTRIBUTING.md) para começar.

### Como Contribuir

1. 🍴 Faça um fork do projeto
2. 🌿 Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push para a branch (`git push origin feature/AmazingFeature`)
5. 🔀 Abra um Pull Request

### Áreas para Contribuição

- 🐛 Reportar bugs
- ✨ Sugerir novas features
- 💻 Implementar funcionalidades
- 📚 Melhorar documentação
- 🎨 Melhorar UI/UX
- 🧪 Adicionar testes

## 📊 Status do Projeto

- [x] Sistema de autenticação
- [x] Chat em tempo real
- [x] Planner colaborativo
- [x] Integração WhatsApp
- [x] API REST completa
- [x] Interface React
- [ ] Testes automatizados
- [ ] CI/CD pipeline
- [ ] Deploy automático
- [ ] Monitoramento

## 🏆 Roadmap

### v1.1 (Próxima versão)
- [ ] Sistema de notificações push
- [ ] Integração com calendário
- [ ] Relatórios e analytics
- [ ] Modo offline

### v1.2
- [ ] Múltiplas salas de chat
- [ ] Sistema de arquivos
- [ ] Integração com GitHub
- [ ] Mobile app

### v2.0
- [ ] IA para sugestões
- [ ] Gamificação
- [ ] Marketplace de templates
- [ ] API pública

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework incrível
- [React](https://reactjs.org/) - Biblioteca de UI
- [PostgreSQL](https://www.postgresql.org/) - Banco de dados robusto
- [Docker](https://www.docker.com/) - Containerização
- Todos os contribuidores da comunidade

## 📞 Contato

- **Projeto**: [GitHub Issues](https://github.com/seu-usuario/estagiarios-platform/issues)
- **Email**: [seu-email@exemplo.com]
- **Discord**: [Link para servidor Discord]
- **LinkedIn**: [Seu perfil LinkedIn]

---

**⭐ Se este projeto te ajudou, considere dar uma estrela!**

**🤝 Contribuições são sempre bem-vindas!**

**📱 Junte-se à comunidade de estagiários!**

