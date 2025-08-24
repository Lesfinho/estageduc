import React, { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { api } from '../services/api';
import { User, Mail, Calendar, Edit, Save, X } from 'lucide-react';
import './Profile.css';

const Profile: React.FC = () => {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    full_name: user?.full_name || '',
    email: user?.email || '',
    username: user?.username || ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      await api.put('/users/me', formData);
      setMessage('Perfil atualizado com sucesso!');
      setIsEditing(false);
      // Recarrega a página para atualizar os dados
      window.location.reload();
    } catch (error) {
      setMessage('Erro ao atualizar perfil. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setFormData({
      full_name: user?.full_name || '',
      email: user?.email || '',
      username: user?.username || ''
    });
    setIsEditing(false);
    setMessage('');
  };

  return (
    <div className="profile-page">
      <div className="profile-header">
        <h1>Meu Perfil</h1>
        <p>Gerencie suas informações pessoais</p>
      </div>

      {message && (
        <div className={`message ${message.includes('sucesso') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}

      <div className="profile-card">
        <div className="profile-avatar">
          <User size={48} />
        </div>

        {!isEditing ? (
          <div className="profile-info">
            <div className="info-row">
              <label>Nome completo:</label>
              <span>{user?.full_name}</span>
            </div>
            
            <div className="info-row">
              <label>Username:</label>
              <span>{user?.username}</span>
            </div>
            
            <div className="info-row">
              <label>Email:</label>
              <span>{user?.email}</span>
            </div>
            
            <div className="info-row">
              <label>Membro desde:</label>
              <span>Hoje</span>
            </div>

            <button 
              onClick={() => setIsEditing(true)}
              className="edit-btn"
            >
              <Edit size={16} />
              Editar Perfil
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="profile-form">
            <div className="form-group">
              <label>Nome completo:</label>
              <input
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="form-group">
              <label>Username:</label>
              <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleChange}
                required
              />
            </div>
            
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-actions">
              <button 
                type="submit" 
                className="save-btn"
                disabled={loading}
              >
                <Save size={16} />
                {loading ? 'Salvando...' : 'Salvar'}
              </button>
              
              <button 
                type="button" 
                onClick={handleCancel}
                className="cancel-btn"
              >
                <X size={16} />
                Cancelar
              </button>
            </div>
          </form>
        )}
      </div>

      <div className="profile-stats">
        <h3>Estatísticas da Conta</h3>
        <div className="stats-grid">
          <div className="stat-item">
            <div className="stat-icon">
              <Calendar size={24} />
            </div>
            <div className="stat-content">
              <h4>Membro desde</h4>
              <p>Hoje</p>
            </div>
          </div>
          
          <div className="stat-item">
            <div className="stat-icon">
              <Mail size={24} />
            </div>
            <div className="stat-content">
              <h4>Email verificado</h4>
              <p>Sim</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;

