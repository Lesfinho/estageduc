import React from 'react';
import MessageBoard from '../components/MessageBoard';
import './Chat.css';

const Chat: React.FC = () => {
  return (
    <div className="chat-page">
      <div className="chat-header">
        <h1>Chat Colaborativo</h1>
        <p>Conecte-se com outros estagiários em tempo real</p>
      </div>
      
      <MessageBoard />
    </div>
  );
};

export default Chat;

