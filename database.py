"""
Sistema de Base de Datos para Multi-Agent Project Manager
Gestiona memoria persistente de tareas, agentes y contexto
"""

from sqlalchemy import create_engine, Column, String, DateTime, Text, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
import uuid

Base = declarative_base()

class Task(Base):
    """Modelo de Tarea"""
    __tablename__ = 'tasks'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    project = Column(String, nullable=False)  # ConsorcioOpt, SocialConsorcio, SocialEmprendedores
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(String, default='pending')  # pending, in_progress, completed, blocked
    priority = Column(String, default='medium')  # low, medium, high, urgent
    assigned_agent = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    notes = Column(Text)
    subtasks = Column(JSON, default=list)
    extra_data = Column(JSON, default=dict)
    
    def to_dict(self):
        return {
            'id': self.id,
            'project': self.project,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'assigned_agent': self.assigned_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'notes': self.notes,
            'subtasks': self.subtasks,
            'metadata': self.extra_data
        }


class AgentMemory(Base):
    """Memoria del Agente"""
    __tablename__ = 'agent_memory'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = Column(String, nullable=False, unique=True)
    project = Column(String, nullable=False)
    context = Column(Text)
    personality_traits = Column(JSON, default=dict)
    conversation_history = Column(JSON, default=list)
    decisions_made = Column(JSON, default=list)
    last_active = Column(DateTime, default=datetime.utcnow)
    total_tasks_completed = Column(Integer, default=0)
    extra_data = Column(JSON, default=dict)
    
    def to_dict(self):
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'project': self.project,
            'context': self.context,
            'personality_traits': self.personality_traits,
            'conversation_history': self.conversation_history[-10:],  # Últimas 10 conversaciones
            'decisions_made': self.decisions_made[-10:],  # Últimas 10 decisiones
            'last_active': self.last_active.isoformat() if self.last_active else None,
            'total_tasks_completed': self.total_tasks_completed,
            'metadata': self.extra_data
        }


class SystemLog(Base):
    """Log del Sistema"""
    __tablename__ = 'system_logs'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_type = Column(String)  # task_created, task_updated, agent_action, etc.
    agent_id = Column(String)
    task_id = Column(String, nullable=True)
    description = Column(Text)
    extra_data = Column(JSON, default=dict)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'event_type': self.event_type,
            'agent_id': self.agent_id,
            'task_id': self.task_id,
            'description': self.description,
            'metadata': self.extra_data
        }


class DatabaseManager:
    """Gestor de Base de Datos"""
    
    def __init__(self, db_path='sqlite:///multi_agent_system.db'):
        self.engine = create_engine(db_path, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()
    
    # --- TAREAS ---
    
    def create_task(self, project, title, description, priority='medium', metadata=None):
        session = self.get_session()
        try:
            task = Task(
                project=project,
                title=title,
                description=description,
                priority=priority,
                extra_data=metadata or {}
            )
            session.add(task)
            session.commit()
            result = task.to_dict()
            return result
        finally:
            session.close()
    
    def get_task(self, task_id):
        session = self.get_session()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            return task.to_dict() if task else None
        finally:
            session.close()
    
    def get_all_tasks(self, project=None, status=None):
        session = self.get_session()
        try:
            query = session.query(Task)
            if project:
                query = query.filter(Task.project == project)
            if status:
                query = query.filter(Task.status == status)
            tasks = query.order_by(Task.created_at.desc()).all()
            return [task.to_dict() for task in tasks]
        finally:
            session.close()
    
    def update_task(self, task_id, **kwargs):
        session = self.get_session()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                task.updated_at = datetime.utcnow()
                session.commit()
                return task.to_dict()
            return None
        finally:
            session.close()
    
    def delete_task(self, task_id):
        session = self.get_session()
        try:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task:
                session.delete(task)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    # --- MEMORIA DE AGENTES ---
    
    def get_or_create_agent_memory(self, agent_id, project, personality_traits=None):
        session = self.get_session()
        try:
            memory = session.query(AgentMemory).filter(AgentMemory.agent_id == agent_id).first()
            if not memory:
                memory = AgentMemory(
                    agent_id=agent_id,
                    project=project,
                    personality_traits=personality_traits or {}
                )
                session.add(memory)
                session.commit()
            return memory.to_dict()
        finally:
            session.close()
    
    def update_agent_memory(self, agent_id, **kwargs):
        session = self.get_session()
        try:
            memory = session.query(AgentMemory).filter(AgentMemory.agent_id == agent_id).first()
            if memory:
                for key, value in kwargs.items():
                    if hasattr(memory, key):
                        if key in ['conversation_history', 'decisions_made']:
                            # Agregar a la lista existente
                            current = getattr(memory, key) or []
                            current.append(value)
                            setattr(memory, key, current)
                        else:
                            setattr(memory, key, value)
                memory.last_active = datetime.utcnow()
                session.commit()
                return memory.to_dict()
            return None
        finally:
            session.close()
    
    def get_agent_memory(self, agent_id):
        session = self.get_session()
        try:
            memory = session.query(AgentMemory).filter(AgentMemory.agent_id == agent_id).first()
            return memory.to_dict() if memory else None
        finally:
            session.close()
    
    # --- LOGS ---
    
    def log_event(self, event_type, agent_id, description, task_id=None, metadata=None):
        session = self.get_session()
        try:
            log = SystemLog(
                event_type=event_type,
                agent_id=agent_id,
                task_id=task_id,
                description=description,
                extra_data=metadata or {}
            )
            session.add(log)
            session.commit()
            return log.to_dict()
        finally:
            session.close()
    
    def get_logs(self, limit=50, agent_id=None, event_type=None):
        session = self.get_session()
        try:
            query = session.query(SystemLog)
            if agent_id:
                query = query.filter(SystemLog.agent_id == agent_id)
            if event_type:
                query = query.filter(SystemLog.event_type == event_type)
            logs = query.order_by(SystemLog.timestamp.desc()).limit(limit).all()
            return [log.to_dict() for log in logs]
        finally:
            session.close()
