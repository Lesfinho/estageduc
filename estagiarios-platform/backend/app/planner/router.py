from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Task, User
from app.schemas import Task as TaskSchema, TaskCreate, TaskUpdate
from app.auth.router import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TaskSchema])
async def get_tasks(
    status: str = None,
    assigned_to_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista tarefas com filtros opcionais"""
    query = db.query(Task)
    
    if status:
        query = query.filter(Task.status == status)
    
    if assigned_to_id:
        query = query.filter(Task.assigned_to_id == assigned_to_id)
    
    tasks = query.all()
    return tasks

@router.get("/my-tasks", response_model=List[TaskSchema])
async def get_my_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista tarefas atribuídas ao usuário atual"""
    tasks = db.query(Task).filter(Task.assigned_to_id == current_user.id).all()
    return tasks

@router.post("/", response_model=TaskSchema)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria uma nova tarefa"""
    db_task = Task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        due_date=task.due_date,
        assigned_to_id=task.assigned_to_id,
        created_by_id=current_user.id
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=TaskSchema)
async def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtém uma tarefa específica"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    return task

@router.put("/{task_id}", response_model=TaskSchema)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza uma tarefa"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    # Apenas o criador ou o responsável pode atualizar
    if task.created_by_id != current_user.id and task.assigned_to_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para atualizar esta tarefa"
        )
    
    # Atualiza apenas os campos fornecidos
    update_data = task_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Deleta uma tarefa (apenas o criador pode deletar)"""
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    if task.created_by_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o criador pode deletar a tarefa"
        )
    
    db.delete(task)
    db.commit()
    return None

@router.patch("/{task_id}/status", response_model=TaskSchema)
async def update_task_status(
    task_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza o status de uma tarefa"""
    if status not in ["todo", "doing", "done"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status deve ser 'todo', 'doing' ou 'done'"
        )
    
    task = db.query(Task).filter(Task.id == task_id).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    
    # Apenas o responsável pode atualizar o status
    if task.assigned_to_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas o responsável pode atualizar o status"
        )
    
    task.status = status
    db.commit()
    db.refresh(task)
    return task

