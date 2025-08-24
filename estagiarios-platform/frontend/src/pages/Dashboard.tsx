import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../services/api';
import { Calendar, MessageSquare, CheckCircle, Clock, TrendingUp } from 'lucide-react';
import './Dashboard.css';

interface Task {
  id: number;
  title: string;
  status: string;
  priority: string;
  due_date: string | null;
}

interface Message {
  id: number;
  content: string;
  username: string;
  created_at: string;
}

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalTasks: 0,
    completedTasks: 0,
    pendingTasks: 0,
    recentMessages: 0
  });
  const [recentTasks, setRecentTasks] = useState<Task[]>([]);
  const [recentMessages, setRecentMessages] = useState<Message[]>([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      // Carrega estatísticas
      const tasksResponse = await api.get('/planner/');
      const messagesResponse = await api.get('/messages/');
      
      const tasks = tasksResponse.data;
      const messages = messagesResponse.data;
      
      setStats({
        totalTasks: tasks.length,
        completedTasks: tasks.filter((t: Task) => t.status === 'done').length,
        pendingTasks: tasks.filter((t: Task) => t.status === 'todo').length,
        recentMessages: messages.length
      });
      
      // Tarefas recentes
      setRecentTasks(tasks.slice(0, 5));
      
      // Mensagens recentes
      setRecentMessages(messages.slice(0, 5));
      
    } catch (error) {
      console.error('Erro ao carregar dados do dashboard:', error);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return '#ef4444';
      case 'medium': return '#f59e0b';
      case 'low': return '#10b981';
      default: return '#6b7280';
    }
  };

  const getPriorityLabel = (priority: string) => {
    switch (priority) {
      case 'high': return 'Alta';
      case 'medium': return 'Média';
      case 'low': return 'Baixa';
      default: return priority;
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'todo': return 'Para Fazer';
      case 'doing': return 'Fazendo';
      case 'done': return 'Concluído';
      default: return status;
    }
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Bem-vindo, {user?.full_name}!</h1>
        <p>Resumo da sua atividade na plataforma</p>
      </div>

      {/* Cards de estatísticas */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <CheckCircle size={24} />
          </div>
          <div className="stat-content">
            <h3>{stats.totalTasks}</h3>
            <p>Total de Tarefas</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Clock size={24} />
          </div>
          <div className="stat-content">
            <h3>{stats.pendingTasks}</h3>
            <p>Pendentes</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <TrendingUp size={24} />
          </div>
          <div className="stat-content">
            <h3>{stats.completedTasks}</h3>
            <p>Concluídas</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <MessageSquare size={24} />
          </div>
          <div className="stat-content">
            <h3>{stats.recentMessages}</h3>
            <p>Mensagens</p>
          </div>
        </div>
      </div>

      {/* Conteúdo principal */}
      <div className="dashboard-content">
        <div className="dashboard-section">
          <h2>Tarefas Recentes</h2>
          <div className="tasks-list">
            {recentTasks.length > 0 ? (
              recentTasks.map((task) => (
                <div key={task.id} className="task-item">
                  <div className="task-info">
                    <h4>{task.title}</h4>
                    <div className="task-meta">
                      <span className={`status status-${task.status}`}>
                        {getStatusLabel(task.status)}
                      </span>
                      <span 
                        className="priority"
                        style={{ color: getPriorityColor(task.priority) }}
                      >
                        {getPriorityLabel(task.priority)}
                      </span>
                      {task.due_date && (
                        <span className="due-date">
                          <Calendar size={16} />
                          {new Date(task.due_date).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p className="no-data">Nenhuma tarefa encontrada</p>
            )}
          </div>
        </div>

        <div className="dashboard-section">
          <h2>Mensagens Recentes</h2>
          <div className="messages-list">
            {recentMessages.length > 0 ? (
              recentMessages.map((message) => (
                <div key={message.id} className="message-item">
                  <div className="message-content">
                    <p>{message.content}</p>
                    <div className="message-meta">
                      <span className="username">{message.username}</span>
                      <span className="timestamp">
                        {new Date(message.created_at).toLocaleString()}
                      </span>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p className="no-data">Nenhuma mensagem encontrada</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

