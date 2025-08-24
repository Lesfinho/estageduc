from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Schemas de Usuário
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas de Mensagem
class MessageBase(BaseModel):
    content: str
    room_id: int = 1

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas de Tarefa
class TaskBase(BaseModel):
    title: str
    description: str
    priority: str = "medium"
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    assigned_to_id: int

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to_id: Optional[int] = None
    due_date: Optional[datetime] = None

class Task(TaskBase):
    id: int
    status: str
    assigned_to_id: int
    created_by_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schemas de Autenticação
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
