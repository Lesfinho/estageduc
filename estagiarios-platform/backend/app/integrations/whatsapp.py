import os
from twilio.rest import Client
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class WhatsAppService:
    def __init__(self):
        # Configurações do Twilio
        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None
    
    async def send_message(self, to: str, message: str) -> bool:
        """Envia mensagem via WhatsApp"""
        if not self.client:
            print("Twilio não configurado. Verifique as variáveis de ambiente.")
            return False
        
        try:
            # Formata o número para WhatsApp
            if not to.startswith("whatsapp:"):
                to = f"whatsapp:{to}"
            
            # Envia a mensagem
            message_obj = self.client.messages.create(
                from_=f"whatsapp:{self.from_number}",
                body=message,
                to=to
            )
            
            print(f"Mensagem enviada com sucesso: {message_obj.sid}")
            return True
            
        except Exception as e:
            print(f"Erro ao enviar mensagem WhatsApp: {e}")
            return False
    
    async def send_notification(self, to: str, task_title: str, status: str) -> bool:
        """Envia notificação sobre mudança de status de tarefa"""
        message = f"📋 Atualização de Tarefa\n\n"
        message += f"Tarefa: {task_title}\n"
        message += f"Status: {status}\n\n"
        message += f"Verifique na plataforma: http://localhost:3000/planner"
        
        return await self.send_message(to, message)
    
    async def send_reminder(self, to: str, task_title: str, due_date: str) -> bool:
        """Envia lembrete sobre tarefa próxima do prazo"""
        message = f"⏰ Lembrete de Tarefa\n\n"
        message += f"Tarefa: {task_title}\n"
        message += f"Prazo: {due_date}\n\n"
        message += f"Complete na plataforma: http://localhost:3000/planner"
        
        return await self.send_message(to, message)

# Instância global do serviço
whatsapp_service = WhatsAppService()

async def send_whatsapp_message(to: str, message: str) -> bool:
    """Função auxiliar para enviar mensagem WhatsApp"""
    return await whatsapp_service.send_message(to, message)

async def send_task_notification(to: str, task_title: str, status: str) -> bool:
    """Função auxiliar para enviar notificação de tarefa"""
    return await whatsapp_service.send_notification(to, task_title, status)

async def send_task_reminder(to: str, task_title: str, due_date: str) -> bool:
    """Função auxiliar para enviar lembrete de tarefa"""
    return await whatsapp_service.send_reminder(to, task_title, due_date)

