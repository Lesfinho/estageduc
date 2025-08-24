import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../services/api';
import { Send, Trash2 } from 'lucide-react';
import './MessageBoard.css';

interface Message {
  id: number;
  content: string;
  user_id: number;
  username: string;
  created_at: string;
}

const MessageBoard: React.FC = () => {
  const { user } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [ws, setWs] = useState<WebSocket | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Carrega mensagens existentes
    loadMessages();
    
    // Conecta ao WebSocket
    const websocket = new WebSocket('ws://localhost:8000/messages/ws/1');
    
    websocket.onopen = () => {
      console.log('Conectado ao chat');
    };
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'message') {
        setMessages(prev => [...prev, {
          id: Date.now(), // ID temporário
          content: data.content,
          user_id: data.user_id,
          username: data.username,
          created_at: data.created_at || new Date().toISOString()
        }]);
      }
    };
    
    websocket.onerror = (error) => {
      console.error('Erro WebSocket:', error);
    };
    
    setWs(websocket);
    
    return () => {
      websocket.close();
    };
  }, []);

  useEffect(() => {
    // Scroll para a última mensagem
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadMessages = async () => {
    try {
      const response = await api.get('/messages/');
      setMessages(response.data);
    } catch (error) {
      console.error('Erro ao carregar mensagens:', error);
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim() || !user) return;
    
    try {
      // Envia via WebSocket para tempo real
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({
          content: newMessage,
          user_id: user.id,
          username: user.username,
          timestamp: new Date().toISOString()
        }));
      }
      
      // Também salva no backend
      await api.post('/messages/', {
        content: newMessage,
        room_id: 1
      });
      
      setNewMessage('');
    } catch (error) {
      console.error('Erro ao enviar mensagem:', error);
    }
  };

  const deleteMessage = async (messageId: number) => {
    try {
      await api.delete(`/messages/${messageId}`);
      setMessages(prev => prev.filter(msg => msg.id !== messageId));
    } catch (error) {
      console.error('Erro ao deletar mensagem:', error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="message-board">
      <div className="messages-container">
        {messages.map((message) => (
          <div 
            key={message.id} 
            className={`message ${message.user_id === user?.id ? 'own' : 'other'}`}
          >
            <div className="message-header">
              <span className="username">{message.username}</span>
              <span className="timestamp">
                {new Date(message.created_at).toLocaleTimeString()}
              </span>
            </div>
            
            <div className="message-content">
              {message.content}
            </div>
            
            {message.user_id === user?.id && (
              <button 
                onClick={() => deleteMessage(message.id)}
                className="delete-btn"
                title="Deletar mensagem"
              >
                <Trash2 size={16} />
              </button>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      
      <div className="message-input">
        <textarea
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Digite sua mensagem..."
          rows={2}
        />
        <button 
          onClick={sendMessage}
          disabled={!newMessage.trim()}
          className="send-btn"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
};

export default MessageBoard;

