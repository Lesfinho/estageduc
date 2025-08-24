from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.messages.router import router as messages_router
from app.planner.router import router as planner_router
from app.integrations.router import router as integrations_router

app = FastAPI(
    title="Plataforma Estagiários",
    description="Plataforma colaborativa para estagiários",
    version="1.0.0"
)

# Configuração CORS mais permissiva para desenvolvimento
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Inclusão dos roteadores
app.include_router(auth_router, prefix="/auth", tags=["autenticação"])
app.include_router(users_router, prefix="/users", tags=["usuários"])
app.include_router(messages_router, prefix="/messages", tags=["mensagens"])
app.include_router(planner_router, prefix="/planner", tags=["planner"])
app.include_router(integrations_router, prefix="/integrations", tags=["integrações"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo à Plataforma Estagiários!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
