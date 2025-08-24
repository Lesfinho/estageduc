from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.router import get_current_user
from app.models import User
from app.integrations.whatsapp import send_whatsapp_message, send_task_notification
from pydantic import BaseModel

router = APIRouter()

class WhatsAppMessageRequest(BaseModel):
    to: str
    message: str

class TaskNotificationRequest(BaseModel):
    to: str
    task_title: str
    status: str

@router.post("/whatsapp/send")
async def send_whatsapp(
    request: WhatsAppMessageRequest,
    current_user: User = Depends(get_current_user)
):
    """Envia mensagem via WhatsApp (apenas para testes)"""
    success = await send_whatsapp_message(request.to, request.message)
    
    if success:
        return {"message": "Mensagem enviada com sucesso"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao enviar mensagem"
        )

@router.post("/whatsapp/notify-task")
async def notify_task_status(
    request: TaskNotificationRequest,
    current_user: User = Depends(get_current_user)
):
    """Envia notificação sobre mudança de status de tarefa"""
    success = await send_task_notification(
        request.to, 
        request.task_title, 
        request.status
    )
    
    if success:
        return {"message": "Notificação enviada com sucesso"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao enviar notificação"
        )

@router.get("/whatsapp/status")
async def get_whatsapp_status(current_user: User = Depends(get_current_user)):
    """Verifica o status da integração WhatsApp"""
    # Verifica se as variáveis de ambiente estão configuradas
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
    
    if account_sid and auth_token and from_number:
        return {
            "status": "configurado",
            "message": "WhatsApp integração ativa"
        }
    else:
        return {
            "status": "não configurado",
            "message": "Configure as variáveis TWILIO_* no arquivo .env"
        }

