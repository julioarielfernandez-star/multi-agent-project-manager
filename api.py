"""
API REST para el Sistema Multi-Agente
Permite control externo desde otras IAs o aplicaciones
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uvicorn

from database import DatabaseManager
from agents import ProjectCoordinator

# Inicializar FastAPI
app = FastAPI(
    title="Multi-Agent Project Manager API",
    description="API para gestionar proyectos con agentes especializados",
    version="1.0.0"
)

# Configurar CORS para permitir acceso desde otras aplicaciones
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar sistema
db = DatabaseManager()
coordinator = ProjectCoordinator(db)

# --- MODELOS PYDANTIC ---

class TaskCreate(BaseModel):
    project: str = Field(..., description="Proyecto: ConsorcioOpt, SocialConsorcio, SocialEmprendedores")
    title: str = Field(..., description="Título de la tarea")
    description: str = Field(..., description="Descripción detallada")
    priority: str = Field(default="medium", description="Prioridad: low, medium, high, urgent")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Metadatos adicionales")

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    notes: Optional[str] = None

class ChatMessage(BaseModel):
    message: str = Field(..., description="Mensaje para el agente")

class ContextUpdate(BaseModel):
    context: str = Field(..., description="Nuevo contexto para el agente")

# --- ENDPOINTS DE SALUD ---

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Multi-Agent Project Manager API",
        "version": "1.0.0",
        "status": "active",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Verificar salud del sistema"""
    try:
        # Verificar base de datos
        db.get_all_tasks()
        
        # Verificar agentes
        agents_status = coordinator.get_all_agents_status()
        
        return {
            "status": "healthy",
            "database": "connected",
            "agents": len(agents_status),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sistema no saludable: {str(e)}")

# --- ENDPOINTS DE TAREAS ---

@app.post("/api/tasks", response_model=Dict[str, Any])
async def create_task(task: TaskCreate):
    """Crear una nueva tarea"""
    try:
        # Validar proyecto
        valid_projects = ['ConsorcioOpt', 'SocialConsorcio', 'SocialEmprendedores']
        if task.project not in valid_projects:
            raise HTTPException(
                status_code=400,
                detail=f"Proyecto inválido. Debe ser uno de: {', '.join(valid_projects)}"
            )
        
        # Crear tarea en base de datos
        new_task = db.create_task(
            project=task.project,
            title=task.title,
            description=task.description,
            priority=task.priority,
            metadata=task.metadata
        )
        
        # Asignar automáticamente al agente
        result = coordinator.assign_task(new_task)
        
        return {
            "success": True,
            "task": new_task,
            "agent_response": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks", response_model=List[Dict[str, Any]])
async def get_all_tasks(project: Optional[str] = None, status: Optional[str] = None):
    """Obtener todas las tareas con filtros opcionales"""
    try:
        tasks = db.get_all_tasks(project=project, status=status)
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks/{task_id}", response_model=Dict[str, Any])
async def get_task(task_id: str):
    """Obtener una tarea específica"""
    try:
        task = db.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/tasks/{task_id}", response_model=Dict[str, Any])
async def update_task(task_id: str, task_update: TaskUpdate):
    """Actualizar una tarea"""
    try:
        # Filtrar solo campos no nulos
        update_data = {k: v for k, v in task_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay datos para actualizar")
        
        updated_task = db.update_task(task_id, **update_data)
        
        if not updated_task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str):
    """Eliminar una tarea"""
    try:
        success = db.delete_task(task_id)
        if not success:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        return {"success": True, "message": "Tarea eliminada"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINTS DE AGENTES ---

@app.get("/api/agents", response_model=Dict[str, Any])
async def get_all_agents():
    """Obtener estado de todos los agentes"""
    try:
        return coordinator.get_all_agents_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents/{project}", response_model=Dict[str, Any])
async def get_agent_info(project: str):
    """Obtener información de un agente específico"""
    try:
        agent = coordinator.get_agent(project)
        if not agent:
            raise HTTPException(status_code=404, detail="Agente no encontrado")
        
        memory = db.get_agent_memory(agent.agent_id)
        
        return {
            "agent_id": agent.agent_id,
            "project": agent.project,
            "personality": agent.personality,
            "memory": memory
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agents/{project}/chat", response_model=Dict[str, Any])
async def chat_with_agent(project: str, chat_msg: ChatMessage):
    """Conversar con un agente específico"""
    try:
        agent = coordinator.get_agent(project)
        if not agent:
            raise HTTPException(status_code=404, detail="Agente no encontrado")
        
        response = agent.chat(chat_msg.message)
        
        return {
            "agent_id": agent.agent_id,
            "user_message": chat_msg.message,
            "agent_response": response,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents/{project}/memory", response_model=Dict[str, Any])
async def get_agent_memory(project: str):
    """Obtener memoria de un agente"""
    try:
        agent = coordinator.get_agent(project)
        if not agent:
            raise HTTPException(status_code=404, detail="Agente no encontrado")
        
        memory = db.get_agent_memory(agent.agent_id)
        return memory if memory else {}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agents/{project}/context")
async def update_agent_context(project: str, context_update: ContextUpdate):
    """Actualizar contexto de un agente"""
    try:
        agent = coordinator.get_agent(project)
        if not agent:
            raise HTTPException(status_code=404, detail="Agente no encontrado")
        
        agent.update_context(context_update.context)
        
        return {
            "success": True,
            "agent_id": agent.agent_id,
            "message": "Contexto actualizado"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINTS DE PROYECTOS ---

@app.get("/api/projects", response_model=List[Dict[str, Any]])
async def get_all_projects():
    """Obtener lista de todos los proyectos"""
    projects = [
        {
            "id": "ConsorcioOpt",
            "name": "Optimización de Administración de Consorcios",
            "description": "Proyecto enfocado en optimizar procesos administrativos",
            "agent": "OptimizadorConsorcio"
        },
        {
            "id": "SocialConsorcio",
            "name": "Canal de Redes Sociales - Administración",
            "description": "Gestión de presencia en redes sociales para servicios de administración",
            "agent": "SocialManagerConsorcio"
        },
        {
            "id": "SocialEmprendedores",
            "name": "Canal de Redes Sociales - Emprendedores",
            "description": "Asesoramiento y mentoría para emprendedores en redes sociales",
            "agent": "MentorEmprendedor"
        }
    ]
    return projects

@app.get("/api/projects/{project_id}/tasks", response_model=List[Dict[str, Any]])
async def get_project_tasks(project_id: str):
    """Obtener todas las tareas de un proyecto"""
    try:
        tasks = db.get_all_tasks(project=project_id)
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects/{project_id}/status", response_model=Dict[str, Any])
async def get_project_status(project_id: str):
    """Obtener estado de un proyecto"""
    try:
        tasks = db.get_all_tasks(project=project_id)
        
        status_count = {}
        for task in tasks:
            status = task['status']
            status_count[status] = status_count.get(status, 0) + 1
        
        agent = coordinator.get_agent(project_id)
        agent_memory = db.get_agent_memory(agent.agent_id) if agent else None
        
        return {
            "project_id": project_id,
            "total_tasks": len(tasks),
            "tasks_by_status": status_count,
            "agent_status": {
                "agent_id": agent.agent_id if agent else None,
                "last_active": agent_memory.get('last_active') if agent_memory else None,
                "total_completed": agent_memory.get('total_tasks_completed', 0) if agent_memory else 0
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINTS DE COORDINACIÓN ---

@app.post("/api/coordinate/assign")
async def manually_assign_task(task_id: str = Body(...), project: str = Body(...)):
    """Asignar manualmente una tarea a un agente"""
    try:
        task = db.get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        
        # Actualizar proyecto si es diferente
        if task['project'] != project:
            db.update_task(task_id, project=project)
            task = db.get_task(task_id)
        
        result = coordinator.assign_task(task)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/coordinate/report", response_model=Dict[str, Any])
async def get_system_report():
    """Obtener reporte general del sistema"""
    try:
        return coordinator.generate_report()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ENDPOINTS DE LOGS ---

@app.get("/api/logs", response_model=List[Dict[str, Any]])
async def get_system_logs(limit: int = 50, agent_id: Optional[str] = None, event_type: Optional[str] = None):
    """Obtener logs del sistema"""
    try:
        logs = db.get_logs(limit=limit, agent_id=agent_id, event_type=event_type)
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- MAIN ---

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
