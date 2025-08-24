import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../services/api';
import { Plus, Edit, Trash2, Calendar, Flag } from 'lucide-react';
import './Planner.css';

interface Task {
  id: number;
  title: string;
  description: string;
  status: string;
  priority: string;
  assigned_to_id: number;
  created_by_id: number;
  due_date: string | null;
  created_at: string;
}

interface Column {
  id: string;
  title: string;
  tasks: Task[];
}

const Planner: React.FC = () => {
  const { user } = useAuth();
  const [columns, setColumns] = useState<Column[]>([
    { id: 'todo', title: 'Para Fazer', tasks: [] },
    { id: 'doing', title: 'Fazendo', tasks: [] },
    { id: 'done', title: 'Concluído', tasks: [] }
  ]);
  const [showNewTaskForm, setShowNewTaskForm] = useState(false);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    priority: 'medium',
    assigned_to_id: user?.id || 0,
    due_date: ''
  });

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      const response = await api.get('/planner/');
      const tasks = response.data;
      
      // Organiza tarefas por coluna
      const updatedColumns = columns.map(col => ({
        ...col,
        tasks: tasks.filter((task: Task) => task.status === col.id)
      }));
      
      setColumns(updatedColumns);
    } catch (error) {
      console.error('Erro ao carregar tarefas:', error);
    }
  };

  const createTask = async () => {
    if (!newTask.title.trim()) return;
    
    try {
      await api.post('/planner/', {
        ...newTask,
        due_date: newTask.due_date || null
      });
      
      setNewTask({
        title: '',
        description: '',
        priority: 'medium',
        assigned_to_id: user?.id || 0,
        due_date: ''
      });
      setShowNewTaskForm(false);
      loadTasks();
    } catch (error) {
      console.error('Erro ao criar tarefa:', error);
    }
  };

  const updateTaskStatus = async (taskId: number, newStatus: string) => {
    try {
      await api.patch(`/planner/${taskId}/status`, newStatus);
      loadTasks();
    } catch (error) {
      console.error('Erro ao atualizar status:', error);
    }
  };

  const deleteTask = async (taskId: number) => {
    try {
      await api.delete(`/planner/${taskId}`);
      loadTasks();
    } catch (error) {
      console.error('Erro ao deletar tarefa:', error);
    }
  };

  const handleDragStart = (e: React.DragEvent, task: Task) => {
    e.dataTransfer.setData('taskId', task.id.toString());
  };

  const handleDrop = (e: React.DragEvent, status: string) => {
    e.preventDefault();
    const taskId = parseInt(e.dataTransfer.getData('taskId'));
    updateTaskStatus(taskId, status);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
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

  return (
    <div className="planner">
      <div className="planner-header">
        <h2>Planner Colaborativo</h2>
        <button 
          onClick={() => setShowNewTaskForm(true)}
          className="new-task-btn"
        >
          <Plus size={20} />
          Nova Tarefa
        </button>
      </div>

      {showNewTaskForm && (
        <div className="new-task-form">
          <h3>Nova Tarefa</h3>
          <div className="form-row">
            <input
              type="text"
              placeholder="Título da tarefa"
              value={newTask.title}
              onChange={(e) => setNewTask({...newTask, title: e.target.value})}
            />
          </div>
          <div className="form-row">
            <textarea
              placeholder="Descrição"
              value={newTask.description}
              onChange={(e) => setNewTask({...newTask, description: e.target.value})}
              rows={3}
            />
          </div>
          <div className="form-row">
            <select
              value={newTask.priority}
              onChange={(e) => setNewTask({...newTask, priority: e.target.value})}
            >
              <option value="low">Baixa Prioridade</option>
              <option value="medium">Média Prioridade</option>
              <option value="high">Alta Prioridade</option>
            </select>
            <input
              type="date"
              value={newTask.due_date}
              onChange={(e) => setNewTask({...newTask, due_date: e.target.value})}
            />
          </div>
          <div className="form-actions">
            <button onClick={createTask} className="save-btn">
              Criar Tarefa
            </button>
            <button 
              onClick={() => setShowNewTaskForm(false)}
              className="cancel-btn"
            >
              Cancelar
            </button>
          </div>
        </div>
      )}

      <div className="kanban-board">
        {columns.map((column) => (
          <div 
            key={column.id}
            className="column"
            onDrop={(e) => handleDrop(e, column.id)}
            onDragOver={handleDragOver}
          >
            <div className="column-header">
              <h3>{column.title}</h3>
              <span className="task-count">{column.tasks.length}</span>
            </div>
            
            <div className="column-content">
              {column.tasks.map((task) => (
                <div
                  key={task.id}
                  className="task-card"
                  draggable
                  onDragStart={(e) => handleDragStart(e, task)}
                >
                  <div className="task-header">
                    <h4>{task.title}</h4>
                    <div className="task-actions">
                      <Flag 
                        size={16} 
                        color={getPriorityColor(task.priority)}
                      />
                      {task.due_date && (
                        <Calendar size={16} />
                      )}
                    </div>
                  </div>
                  
                  {task.description && (
                    <p className="task-description">{task.description}</p>
                  )}
                  
                  {task.due_date && (
                    <div className="task-due-date">
                      Prazo: {new Date(task.due_date).toLocaleDateString()}
                    </div>
                  )}
                  
                  <div className="task-footer">
                    <span className="task-priority">
                      {getPriorityLabel(task.priority)}
                    </span>
                    
                    {task.created_by_id === user?.id && (
                      <button
                        onClick={() => deleteTask(task.id)}
                        className="delete-task-btn"
                        title="Deletar tarefa"
                      >
                        <Trash2 size={16} />
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Planner;

