from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import os
from urllib.parse import urlparse, parse_qs
import hashlib
import secrets
import time

# Configuração do banco
DB_FILE = "estagiarios.db"

def init_db():
    """Inicializa o banco de dados SQLite"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de mensagens
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Tabela de tarefas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash da senha usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verifica se a senha está correta"""
    return hash_password(password) == password_hash

def generate_token():
    """Gera um token JWT simples"""
    return secrets.token_urlsafe(32)

class EstagiariosHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def send_cors_headers(self):
        """Adiciona headers CORS"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    
    def send_json_response(self, data, status=200):
        """Envia resposta JSON"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode())
    
    def get_request_body(self):
        """Lê o corpo da requisição"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            return self.rfile.read(content_length).decode('utf-8')
        return ""
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/':
            self.send_json_response({
                "message": "API Estagiários Platform",
                "version": "1.0.0",
                "endpoints": [
                    "/users",
                    "/messages", 
                    "/tasks",
                    "/health"
                ]
            })
        
        elif path == '/health':
            self.send_json_response({"status": "healthy"})
        
        elif path == '/users':
            # Lista usuários (simplificado)
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, email, created_at FROM users')
            users = []
            for row in cursor.fetchall():
                users.append({
                    "id": row[0],
                    "username": row[1],
                    "email": row[2],
                    "created_at": row[3]
                })
            conn.close()
            self.send_json_response(users)
        
        elif path == '/messages':
            # Lista mensagens
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT m.id, m.content, m.created_at, u.username 
                FROM messages m 
                JOIN users u ON m.user_id = u.id 
                ORDER BY m.created_at DESC
            ''')
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    "id": row[0],
                    "content": row[1],
                    "created_at": row[2],
                    "username": row[3]
                })
            conn.close()
            self.send_json_response(messages)
        
        elif path == '/tasks':
            # Lista tarefas
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT t.id, t.title, t.description, t.status, t.created_at, u.username 
                FROM tasks t 
                JOIN users u ON t.user_id = u.id 
                ORDER BY t.created_at DESC
            ''')
            tasks = []
            for row in cursor.fetchall():
                tasks.append({
                    "id": row[0],
                    "title": row[1],
                    "description": row[2],
                    "status": row[3],
                    "created_at": row[4],
                    "username": row[5]
                })
            conn.close()
            self.send_json_response(tasks)
        
        else:
            self.send_json_response({"error": "Endpoint não encontrado"}, 404)
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/register':
            # Registro de usuário
            try:
                body = self.get_request_body()
                data = json.loads(body)
                
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')
                
                if not all([username, email, password]):
                    self.send_json_response({"error": "Dados incompletos"}, 400)
                    return
                
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                
                # Verifica se usuário já existe
                cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
                if cursor.fetchone():
                    conn.close()
                    self.send_json_response({"error": "Usuário já existe"}, 400)
                    return
                
                # Cria usuário
                password_hash = hash_password(password)
                cursor.execute(
                    'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                    (username, email, password_hash)
                )
                user_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
                self.send_json_response({
                    "message": "Usuário criado com sucesso",
                    "user_id": user_id
                })
                
            except Exception as e:
                self.send_json_response({"error": str(e)}, 500)
        
        elif path == '/login':
            # Login
            try:
                body = self.get_request_body()
                data = json.loads(body)
                
                username = data.get('username')
                password = data.get('password')
                
                if not all([username, password]):
                    self.send_json_response({"error": "Dados incompletos"}, 400)
                    return
                
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
                user = cursor.fetchone()
                conn.close()
                
                if user and verify_password(password, user[1]):
                    token = generate_token()
                    self.send_json_response({
                        "message": "Login realizado com sucesso",
                        "token": token,
                        "user_id": user[0]
                    })
                else:
                    self.send_json_response({"error": "Credenciais inválidas"}, 401)
                    
            except Exception as e:
                self.send_json_response({"error": str(e)}, 500)
        
        elif path == '/messages':
            # Criar mensagem
            try:
                body = self.get_request_body()
                data = json.loads(body)
                
                user_id = data.get('user_id')
                content = data.get('content')
                
                if not all([user_id, content]):
                    self.send_json_response({"error": "Dados incompletos"}, 400)
                    return
                
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO messages (user_id, content) VALUES (?, ?)',
                    (user_id, content)
                )
                message_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
                self.send_json_response({
                    "message": "Mensagem criada com sucesso",
                    "message_id": message_id
                })
                
            except Exception as e:
                self.send_json_response({"error": str(e)}, 500)
        
        elif path == '/tasks':
            # Criar tarefa
            try:
                body = self.get_request_body()
                data = json.loads(body)
                
                user_id = data.get('user_id')
                title = data.get('title')
                description = data.get('description', '')
                
                if not all([user_id, title]):
                    self.send_json_response({"error": "Dados incompletos"}, 400)
                    return
                
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)',
                    (user_id, title, description)
                )
                task_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
                self.send_json_response({
                    "message": "Tarefa criada com sucesso",
                    "task_id": task_id
                })
                
            except Exception as e:
                self.send_json_response({"error": str(e)}, 500)
        
        else:
            self.send_json_response({"error": "Endpoint não encontrado"}, 404)

if __name__ == "__main__":
    # Inicializa o banco
    init_db()
    
    # Configura o servidor
    PORT = 8000
    server = HTTPServer(('localhost', PORT), EstagiariosHandler)
    
    print(f"🚀 Servidor rodando em http://localhost:{PORT}")
    print(f"📊 Banco de dados: {DB_FILE}")
    print("📝 Endpoints disponíveis:")
    print("  GET  / - Informações da API")
    print("  GET  /health - Status do servidor")
    print("  GET  /users - Lista usuários")
    print("  GET  /messages - Lista mensagens")
    print("  GET  /tasks - Lista tarefas")
    print("  POST /register - Registro de usuário")
    print("  POST /login - Login")
    print("  POST /messages - Criar mensagem")
    print("  POST /tasks - Criar tarefa")
    print("\nPressione Ctrl+C para parar")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor parado")
        server.server_close()
