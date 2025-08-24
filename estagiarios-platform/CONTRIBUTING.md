# Contribuindo para a Plataforma Estagiários 🚀

Obrigado por considerar contribuir com a Plataforma Estagiários! Este é um projeto open source e toda contribuição é bem-vinda.

## 📋 Índice

- [Como Contribuir](#como-contribuir)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Fluxo de Trabalho](#fluxo-de-trabalho)
- [Padrões de Código](#padrões-de-código)
- [Testes](#testes)
- [Documentação](#documentação)
- [Reportando Bugs](#reportando-bugs)
- [Solicitando Features](#solicitando-features)
- [Perguntas Frequentes](#perguntas-frequentes)

## 🤝 Como Contribuir

### Tipos de Contribuição

1. **🐛 Reportar Bugs**
   - Use o template de bug report
   - Inclua passos para reproduzir
   - Adicione screenshots quando relevante

2. **✨ Solicitar Features**
   - Use o template de feature request
   - Explique o caso de uso
   - Sugira implementação se possível

3. **💻 Contribuir com Código**
   - Fork o repositório
   - Crie uma branch para sua feature
   - Implemente seguindo os padrões
   - Adicione testes
   - Abra um Pull Request

4. **📚 Melhorar Documentação**
   - Corrigir erros
   - Adicionar exemplos
   - Traduzir para outros idiomas
   - Melhorar clareza

5. **🎨 Melhorar UI/UX**
   - Sugerir melhorias de design
   - Implementar componentes
   - Otimizar responsividade

## 🛠️ Configuração do Ambiente

### Pré-requisitos

- Python 3.11+
- Node.js 18+
- Docker e Docker Compose
- Git

### Setup Local

```bash
# 1. Fork e clone o repositório
git clone https://github.com/SEU_USUARIO/estagiarios-platform.git
cd estagiarios-platform

# 2. Configure o ambiente
cp .env.example .env
# Edite o arquivo .env com suas configurações

# 3. Execute com Docker
docker-compose up --build

# 4. Acesse a aplicação
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Setup de Desenvolvimento

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start
```

## 🏗️ Estrutura do Projeto

```
estagiarios-platform/
├── backend/                 # API Python FastAPI
│   ├── app/
│   │   ├── auth/           # Autenticação JWT
│   │   ├── users/          # Gestão de usuários
│   │   ├── messages/       # Sistema de mensagens
│   │   ├── planner/        # Ferramenta de planning
│   │   └── integrations/   # Integrações (WhatsApp)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # Interface React
│   ├── src/
│   │   ├── components/     # Componentes reutilizáveis
│   │   ├── pages/          # Páginas principais
│   │   └── hooks/          # Custom hooks
│   ├── package.json
│   └── Dockerfile
├── docs/                    # Documentação
├── docker-compose.yml       # Setup Docker
└── CONTRIBUTING.md          # Este arquivo
```

## 🔄 Fluxo de Trabalho

### 1. Escolha uma Issue

- Verifique as issues abertas
- Escolha uma que você possa resolver
- Comente na issue para indicar interesse

### 2. Crie uma Branch

```bash
git checkout -b feature/nome-da-feature
# ou
git checkout -b fix/nome-do-bug
```

### 3. Desenvolva

- Implemente a funcionalidade
- Siga os padrões de código
- Adicione testes
- Atualize documentação

### 4. Commit e Push

```bash
git add .
git commit -m "feat: adiciona nova funcionalidade"
git push origin feature/nome-da-feature
```

### 5. Abra um Pull Request

- Use o template de PR
- Descreva as mudanças
- Link para issues relacionadas
- Adicione screenshots se relevante

## 📝 Padrões de Código

### Backend (Python)

- Siga PEP8
- Use type hints
- Documente funções com docstrings
- Trate erros adequadamente
- Use async/await quando apropriado

```python
async def create_user(user_data: UserCreate, db: Session) -> User:
    """
    Cria um novo usuário.
    
    Args:
        user_data: Dados do usuário
        db: Sessão do banco
        
    Returns:
        Usuário criado
        
    Raises:
        HTTPException: Se email já existe
    """
    # Implementação...
```

### Frontend (React)

- Use componentes funcionais
- Implemente TypeScript
- Use hooks personalizados
- Siga padrões de CSS
- Implemente responsividade

```typescript
interface UserCardProps {
  user: User;
  onEdit: (user: User) => void;
}

const UserCard: React.FC<UserCardProps> = ({ user, onEdit }) => {
  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <button onClick={() => onEdit(user)}>Editar</button>
    </div>
  );
};
```

## 🧪 Testes

### Backend

```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio

# Executar testes
pytest

# Com coverage
pytest --cov=app
```

### Frontend

```bash
# Executar testes
npm test

# Com coverage
npm test -- --coverage
```

### Padrões de Teste

- Teste casos de sucesso e erro
- Use mocks para dependências externas
- Teste edge cases
- Mantenha testes simples e legíveis

## 📚 Documentação

### Atualizando Documentação

- Mantenha README atualizado
- Documente APIs novas
- Adicione exemplos de uso
- Atualize guias de instalação

### Padrões de Documentação

- Use Markdown
- Inclua exemplos práticos
- Mantenha linguagem clara
- Adicione screenshots quando útil

## 🐛 Reportando Bugs

### Template de Bug Report

```markdown
## Descrição do Bug
Descrição clara e concisa do problema.

## Passos para Reproduzir
1. Vá para '...'
2. Clique em '...'
3. Role até '...'
4. Veja o erro

## Comportamento Esperado
O que deveria acontecer.

## Comportamento Atual
O que está acontecendo.

## Screenshots
Se aplicável, adicione screenshots.

## Ambiente
- OS: [ex: Windows 10, macOS]
- Browser: [ex: Chrome, Firefox]
- Versão: [ex: 22]

## Informações Adicionais
Qualquer contexto adicional sobre o problema.
```

## ✨ Solicitando Features

### Template de Feature Request

```markdown
## Descrição da Feature
Descrição clara da funcionalidade desejada.

## Problema que Resolve
Explicação de como isso resolve um problema existente.

## Solução Proposta
Descrição da solução desejada.

## Alternativas Consideradas
Outras soluções que você considerou.

## Contexto Adicional
Qualquer contexto adicional, screenshots, etc.
```

## ❓ Perguntas Frequentes

### Q: Posso contribuir mesmo sendo iniciante?
**A:** Sim! Todas as contribuições são bem-vindas. Comece com issues marcadas como "good first issue" ou "help wanted".

### Q: Como sei se minha contribuição está boa?
**A:** Leia os padrões de código, execute os testes e peça feedback em Pull Requests.

### Q: Posso contribuir com design/UI?
**A:** Absolutamente! Melhorias de UX são muito bem-vindas.

### Q: Como reportar problemas de segurança?
**A:** Para problemas de segurança, envie email para [email] em vez de abrir uma issue pública.

### Q: Posso contribuir com traduções?
**A:** Sim! Traduções para outros idiomas são muito bem-vindas.

## 🎯 Áreas para Contribuição

### Prioridade Alta
- [ ] Testes automatizados
- [ ] Documentação da API
- [ ] Melhorias de segurança
- [ ] Otimizações de performance

### Prioridade Média
- [ ] Novos componentes UI
- [ ] Integrações adicionais
- [ ] Melhorias de acessibilidade
- [ ] Internacionalização

### Prioridade Baixa
- [ ] Temas visuais
- [ ] Plugins de terceiros
- [ ] Funcionalidades experimentais

## 🏆 Reconhecimento

Contribuidores ativos serão:
- Adicionados ao README
- Convidados como colaboradores
- Reconhecidos em releases
- Incluídos no hall da fama

## 📞 Comunicação

- **Issues**: GitHub Issues
- **Discussões**: GitHub Discussions
- **Chat**: [Link para chat se existir]
- **Email**: [Email de contato]

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto.

---

**Obrigado por contribuir para a Plataforma Estagiários! 🎉**

Sua contribuição ajuda a criar uma ferramenta melhor para a comunidade de estagiários.

