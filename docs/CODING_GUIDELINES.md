# Diretrizes de Código - Plataforma Estagiários

## 🎯 Objetivo
Este documento estabelece padrões de código para manter a qualidade e consistência do projeto, facilitando a colaboração entre desenvolvedores.

## 🐍 Backend (Python)

### Convenções Gerais
- **Versão Python**: 3.11+
- **Formatação**: Siga as convenções PEP8
- **Tamanho de linha**: Máximo 88 caracteres (Black)
- **Imports**: Organize em ordem alfabética

### Type Hints
```python
# ✅ Correto
def create_user(user_data: UserCreate, db: Session) -> User:
    pass

# ❌ Incorreto
def create_user(user_data, db):
    pass
```

### Estrutura de Funções
```python
# ✅ Correto
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Busca um usuário pelo ID.
    
    Args:
        user_id: ID do usuário
        db: Sessão do banco de dados
        
    Returns:
        Usuário encontrado ou None
    """
    return db.query(User).filter(User.id == user_id).first()

# ❌ Incorreto
async def get_user_by_id(user_id, db):
    return db.query(User).filter(User.id == user_id).first()
```

### Tratamento de Erros
```python
# ✅ Correto
from fastapi import HTTPException, status

if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuário não encontrado"
    )

# ❌ Incorreto
if not user:
    return {"error": "Usuário não encontrado"}
```

### Documentação
- Use docstrings para todas as funções públicas
- Documente parâmetros, tipos de retorno e exceções
- Use exemplos quando apropriado

## ⚛️ Frontend (React)

### Componentes Funcionais
```typescript
// ✅ Correto
const UserCard: React.FC<UserCardProps> = ({ user, onEdit }) => {
  return (
    <div className="user-card">
      <h3>{user.name}</h3>
      <button onClick={onEdit}>Editar</button>
    </div>
  );
};

// ❌ Incorreto
class UserCard extends React.Component<UserCardProps> {
  render() {
    return (
      <div className="user-card">
        <h3>{this.props.user.name}</h3>
        <button onClick={this.props.onEdit}>Editar</button>
      </div>
    );
  }
}
```

### Hooks Personalizados
```typescript
// ✅ Correto
export function useUser(userId: number) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);
  
  return { user, loading };
}

// ❌ Incorreto
function useUser(userId: number) {
  // Lógica inline no componente
}
```

### TypeScript
```typescript
// ✅ Correto
interface User {
  id: number;
  name: string;
  email: string;
}

interface UserCardProps {
  user: User;
  onEdit: (user: User) => void;
}

// ❌ Incorreto
const UserCard = ({ user, onEdit }: any) => {
  // Sem tipagem
};
```

### CSS e Estilização
- Use CSS Modules para estilização
- Nomeie classes de forma semântica
- Evite estilos inline
- Use variáveis CSS para cores e espaçamentos

```css
/* ✅ Correto */
.user-card {
  padding: var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
}

/* ❌ Incorreto */
.user-card {
  padding: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
```

## 🗄️ Banco de Dados

### Modelos SQLAlchemy
```python
# ✅ Correto
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    messages = relationship("Message", back_populates="user")

# ❌ Incorreto
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String)
    created_at = Column(DateTime)
```

### Queries
```python
# ✅ Correto
users = db.query(User).filter(User.is_active == True).all()

# ❌ Incorreto
users = db.query(User).filter("is_active = true").all()
```

## 🔒 Segurança

### Autenticação
- Sempre valide tokens JWT
- Use HTTPS em produção
- Implemente rate limiting
- Valide inputs do usuário

### Validação de Dados
```python
# ✅ Correto
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

# ❌ Incorreto
class UserCreate(BaseModel):
    email: str
    password: str
    name: str
```

## 🧪 Testes

### Estrutura de Testes
```
tests/
├── unit/
│   ├── test_models.py
│   └── test_services.py
├── integration/
│   ├── test_api.py
│   └── test_database.py
└── conftest.py
```

### Exemplo de Teste
```python
# ✅ Correto
import pytest
from app.models import User
from app.services import create_user

def test_create_user_success():
    user_data = {
        "email": "test@example.com",
        "name": "Test User"
    }
    
    user = create_user(user_data)
    
    assert user.email == user_data["email"]
    assert user.name == user_data["name"]
    assert user.id is not None

# ❌ Incorreto
def test_create_user():
    # Teste sem assertions claras
    pass
```

## 📝 Commits

### Formato de Commit
```
tipo(escopo): descrição breve

- Use verbos no imperativo
- Primeira linha com máximo 50 caracteres
- Descrição detalhada após linha em branco

Exemplos:
feat(auth): adiciona autenticação JWT
fix(api): corrige validação de email
docs(readme): atualiza instruções de instalação
```

### Tipos de Commit
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação de código
- `refactor`: Refatoração
- `test`: Adição de testes
- `chore`: Tarefas de manutenção

## 🚀 Performance

### Backend
- Use async/await para operações I/O
- Implemente cache quando apropriado
- Otimize queries do banco de dados
- Use paginação para listas grandes

### Frontend
- Implemente lazy loading para componentes
- Use React.memo para componentes pesados
- Implemente virtualização para listas grandes
- Otimize re-renders desnecessários

## 🔍 Linting e Formatação

### Backend
```bash
# Instalar ferramentas
pip install black isort flake8 mypy

# Formatação automática
black .
isort .

# Verificação de qualidade
flake8 .
mypy .
```

### Frontend
```bash
# Instalar ferramentas
npm install --save-dev eslint prettier

# Formatação automática
npm run format

# Verificação de qualidade
npm run lint
```

## 📚 Recursos Adicionais

- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [React Best Practices](https://reactjs.org/docs/hooks-faq.html)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🤝 Contribuindo

1. Leia este guia antes de contribuir
2. Siga os padrões estabelecidos
3. Escreva testes para novas funcionalidades
4. Documente mudanças importantes
5. Use as ferramentas de linting configuradas

---

**Lembre-se**: Código limpo e bem documentado é mais fácil de manter e colaborar!


