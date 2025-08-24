from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Message, User
from app.schemas import Message as MessageSchema, MessageCreate
from app.auth.router import get_current_user
import json

router = APIRouter()

# Gerenciador de conexões WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

@router.get("/", response_model=List[MessageSchema])
async def get_messages(
    room_id: int = 1,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista mensagens de uma sala específica"""
    messages = db.query(Message).filter(Message.room_id == room_id).offset(skip).limit(limit).all()
    return messages

@router.post("/", response_model=MessageSchema)
async def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria uma nova mensagem"""
    db_message = Message(
        content=message.content,
        user_id=current_user.id,
        room_id=message.room_id
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    # Broadcast da mensagem para todos os usuários conectados
    await manager.broadcast(json.dumps({
        "type": "message",
        "content": db_message.content,
        "user_id": db_message.user_id,
        "username": current_user.username,
        "created_at": db_message.created_at.isoformat()
    }))
    
    return db_message

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int):
    """Endpoint WebSocket para chat em tempo real"""
    await manager.connect(websocket)
    
    try:
        while True:
            # Recebe mensagem do cliente
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Broadcast da mensagem para todos os usuários conectados
            await manager.broadcast(json.dumps({
                "type": "message",
                "content": message_data.get("content", ""),
                "user_id": message_data.get("user_id"),
                "username": message_data.get("username", "Anônimo"),
                "room_id": room_id,
                "timestamp": message_data.get("timestamp")
            }))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Usuário saiu da sala {room_id}")

@router.delete("/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deleta uma mensagem (apenas o autor pode deletar)"""
    message = db.query(Message).filter(Message.id == message_id).first()
    
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mensagem não encontrada"
        )
    
    if message.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode deletar suas próprias mensagens"
        )
    
    db.delete(message)
    db.commit()
    return None
