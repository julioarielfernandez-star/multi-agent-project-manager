"""
Sistema de Agentes Especializados
Cada agente tiene personalidad única y gestiona un proyecto específico
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from database import DatabaseManager
from datetime import datetime
import os
import json

# Configurar OpenAI API (ya está preconfigurada en el ambiente)
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0.7)

class BaseAgent:
    """Clase base para todos los agentes"""
    
    def __init__(self, agent_id, project, personality, db_manager):
        self.agent_id = agent_id
        self.project = project
        self.personality = personality
        self.db = db_manager
        
        # Inicializar o recuperar memoria
        self.memory = self.db.get_or_create_agent_memory(
            agent_id=agent_id,
            project=project,
            personality_traits=personality
        )
    
    def get_system_prompt(self):
        """Genera el prompt del sistema basado en la personalidad"""
        return f"""Eres {self.agent_id}, un agente especializado en {self.project}.

PERSONALIDAD:
{json.dumps(self.personality, indent=2, ensure_ascii=False)}

CONTEXTO ACTUAL:
{self.memory.get('context', 'Sin contexto previo')}

DECISIONES RECIENTES:
{json.dumps(self.memory.get('decisions_made', [])[-3:], indent=2, ensure_ascii=False)}

Tu objetivo es gestionar tareas de manera efectiva manteniendo tu personalidad única.
Siempre proporciona respuestas estructuradas, accionables y alineadas con tu rol."""
    
    def process_task(self, task):
        """Procesa una tarea y genera una respuesta"""
        system_prompt = self.get_system_prompt()
        
        user_message = f"""TAREA: {task['title']}

DESCRIPCIÓN: {task['description']}

PRIORIDAD: {task['priority']}

Por favor:
1. Analiza la tarea desde tu perspectiva como {self.agent_id}
2. Proporciona un plan de acción específico
3. Identifica posibles subtareas
4. Sugiere próximos pasos concretos
5. Actualiza el estado si es apropiado

Responde en formato JSON con esta estructura:
{{
    "analisis": "tu análisis de la tarea",
    "plan_accion": ["paso 1", "paso 2", "paso 3"],
    "subtareas": ["subtarea 1", "subtarea 2"],
    "proximos_pasos": ["paso inmediato 1", "paso inmediato 2"],
    "estado_sugerido": "pending|in_progress|completed",
    "notas": "observaciones adicionales"
}}"""
        
        try:
            response = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ])
            
            # Parsear respuesta
            result = json.loads(response.content)
            
            # Registrar en memoria
            self.db.update_agent_memory(
                agent_id=self.agent_id,
                conversation_history={
                    'timestamp': datetime.utcnow().isoformat(),
                    'task_id': task['id'],
                    'response': result
                }
            )
            
            # Log del evento
            self.db.log_event(
                event_type='task_processed',
                agent_id=self.agent_id,
                task_id=task['id'],
                description=f"Tarea procesada: {task['title']}",
                metadata=result
            )
            
            return result
            
        except Exception as e:
            return {
                "error": str(e),
                "analisis": "Error al procesar la tarea",
                "plan_accion": [],
                "subtareas": [],
                "proximos_pasos": ["Revisar la tarea manualmente"],
                "estado_sugerido": "blocked",
                "notas": f"Error: {str(e)}"
            }
    
    def chat(self, message):
        """Conversa con el agente"""
        system_prompt = self.get_system_prompt()
        
        try:
            response = llm.invoke([
                SystemMessage(content=system_prompt),
                HumanMessage(content=message)
            ])
            
            # Registrar conversación
            self.db.update_agent_memory(
                agent_id=self.agent_id,
                conversation_history={
                    'timestamp': datetime.utcnow().isoformat(),
                    'user_message': message,
                    'agent_response': response.content
                }
            )
            
            return response.content
            
        except Exception as e:
            return f"Error en la conversación: {str(e)}"
    
    def update_context(self, new_context):
        """Actualiza el contexto del agente"""
        self.db.update_agent_memory(
            agent_id=self.agent_id,
            context=new_context
        )
        self.memory = self.db.get_agent_memory(self.agent_id)


class OptimizadorConsorcio(BaseAgent):
    """Agente especializado en optimización de administración de consorcios"""
    
    def __init__(self, db_manager):
        personality = {
            "nombre": "OptimizadorConsorcio",
            "rol": "Experto en optimización de procesos administrativos",
            "tono": "Profesional, analítico, directo",
            "enfoque": "Eficiencia, métricas, procesos estructurados",
            "especialidades": [
                "Análisis de procesos administrativos",
                "Identificación de ineficiencias",
                "Propuestas de mejora basadas en datos",
                "Seguimiento de KPIs",
                "Automatización de tareas repetitivas"
            ],
            "estilo_comunicacion": "Estructurado, basado en datos, orientado a resultados"
        }
        super().__init__(
            agent_id="OptimizadorConsorcio",
            project="ConsorcioOpt",
            personality=personality,
            db_manager=db_manager
        )


class SocialManagerConsorcio(BaseAgent):
    """Agente especializado en gestión de redes sociales para administración"""
    
    def __init__(self, db_manager):
        personality = {
            "nombre": "SocialManagerConsorcio",
            "rol": "Community Manager especializado en servicios de administración",
            "tono": "Amigable, profesional, cercano",
            "enfoque": "Engagement, branding, comunicación efectiva",
            "especialidades": [
                "Planificación de contenido",
                "Creación de posts atractivos",
                "Calendario editorial",
                "Análisis de métricas sociales",
                "Gestión de comunidad",
                "Respuesta a comentarios"
            ],
            "estilo_comunicacion": "Creativo, visual, orientado a la audiencia"
        }
        super().__init__(
            agent_id="SocialManagerConsorcio",
            project="SocialConsorcio",
            personality=personality,
            db_manager=db_manager
        )


class MentorEmprendedor(BaseAgent):
    """Agente especializado en mentoría para emprendedores"""
    
    def __init__(self, db_manager):
        personality = {
            "nombre": "MentorEmprendedor",
            "rol": "Mentor experimentado que guía a emprendedores",
            "tono": "Inspirador, motivador, educativo",
            "enfoque": "Enseñanza práctica, mentoría, crecimiento personal",
            "especialidades": [
                "Contenido educativo para emprendedores",
                "Tips y consejos prácticos",
                "Casos de éxito inspiradores",
                "Recursos y herramientas",
                "Estrategias de crecimiento",
                "Superación de obstáculos"
            ],
            "estilo_comunicacion": "Empático, práctico, orientado a la acción"
        }
        super().__init__(
            agent_id="MentorEmprendedor",
            project="SocialEmprendedores",
            personality=personality,
            db_manager=db_manager
        )


class ProjectCoordinator:
    """Coordinador que gestiona todos los agentes"""
    
    def __init__(self, db_manager):
        self.db = db_manager
        self.agents = {
            'ConsorcioOpt': OptimizadorConsorcio(db_manager),
            'SocialConsorcio': SocialManagerConsorcio(db_manager),
            'SocialEmprendedores': MentorEmprendedor(db_manager)
        }
    
    def assign_task(self, task):
        """Asigna una tarea al agente apropiado"""
        project = task['project']
        if project in self.agents:
            agent = self.agents[project]
            
            # Actualizar tarea con agente asignado
            self.db.update_task(
                task['id'],
                assigned_agent=agent.agent_id,
                status='in_progress'
            )
            
            # Procesar tarea
            result = agent.process_task(task)
            
            # Actualizar tarea con resultados
            self.db.update_task(
                task['id'],
                notes=json.dumps(result, ensure_ascii=False),
                subtasks=result.get('subtareas', []),
                status=result.get('estado_sugerido', 'in_progress')
            )
            
            return {
                'task_id': task['id'],
                'agent': agent.agent_id,
                'result': result
            }
        else:
            return {
                'error': f'No hay agente disponible para el proyecto {project}'
            }
    
    def get_agent(self, project):
        """Obtiene un agente específico"""
        return self.agents.get(project)
    
    def get_all_agents_status(self):
        """Obtiene el estado de todos los agentes"""
        status = {}
        for project, agent in self.agents.items():
            memory = self.db.get_agent_memory(agent.agent_id)
            status[project] = {
                'agent_id': agent.agent_id,
                'project': project,
                'personality': agent.personality,
                'last_active': memory.get('last_active') if memory else None,
                'total_tasks_completed': memory.get('total_tasks_completed', 0) if memory else 0
            }
        return status
    
    def generate_report(self):
        """Genera un reporte consolidado del sistema"""
        all_tasks = self.db.get_all_tasks()
        agents_status = self.get_all_agents_status()
        
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_tasks': len(all_tasks),
            'tasks_by_status': {},
            'tasks_by_project': {},
            'agents': agents_status
        }
        
        # Contar tareas por estado
        for task in all_tasks:
            status = task['status']
            project = task['project']
            
            report['tasks_by_status'][status] = report['tasks_by_status'].get(status, 0) + 1
            report['tasks_by_project'][project] = report['tasks_by_project'].get(project, 0) + 1
        
        return report
