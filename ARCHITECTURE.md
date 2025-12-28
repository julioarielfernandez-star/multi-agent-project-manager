# Arquitectura del Sistema Multi-Agente de Gestión de Proyectos

## Visión General

Sistema multi-agente para gestionar 3 proyectos específicos con memoria persistente, personalidades únicas y capacidad de control externo.

## Proyectos Gestionados

### 1. ConsorcioOpt - Optimización de Administración de Consorcios
**Objetivo**: Optimizar procesos administrativos de consorcios
**Agente**: OptimizadorConsorcio
**Personalidad**: Analítico, eficiente, orientado a procesos
**Tareas típicas**: 
- Análisis de procesos actuales
- Identificación de ineficiencias
- Propuestas de mejora
- Seguimiento de implementaciones
- Reportes de optimización

### 2. SocialConsorcio - Canal de Redes Sociales para Administración
**Objetivo**: Gestionar presencia en redes sociales de servicios de administración
**Agente**: SocialManagerConsorcio
**Personalidad**: Creativo, comunicativo, orientado a engagement
**Tareas típicas**:
- Planificación de contenido
- Creación de posts
- Calendario editorial
- Análisis de métricas
- Respuesta a comentarios

### 3. SocialEmprendedores - Canal de Redes Sociales para Emprendedores
**Objetivo**: Asesorar emprendedores a través de redes sociales
**Agente**: MentorEmprendedor
**Personalidad**: Inspirador, educativo, empático
**Tareas típicas**:
- Contenido educativo
- Tips y consejos
- Casos de éxito
- Recursos para emprendedores
- Engagement con comunidad

## Arquitectura de Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    API REST (FastAPI)                       │
│  - Control externo desde otras IAs                          │
│  - Endpoints para crear/actualizar/consultar tareas         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Coordinador (Project Manager)                  │
│  - Distribuye tareas entre agentes                          │
│  - Monitorea progreso                                       │
│  - Genera reportes consolidados                             │
└─────────────────────────────────────────────────────────────┘
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
        ┌────────────┐ ┌────────────┐ ┌────────────┐
        │ Optimizador│ │   Social   │ │   Mentor   │
        │ Consorcio  │ │  Manager   │ │Emprendedor │
        │            │ │ Consorcio  │ │            │
        └────────────┘ └────────────┘ └────────────┘
                 │            │            │
                 └────────────┼────────────┘
                              ▼
                    ┌──────────────────┐
                    │ Sistema de Memoria│
                    │   (SQLite DB)    │
                    │  - Tareas        │
                    │  - Historial     │
                    │  - Contexto      │
                    └──────────────────┘
```

## Stack Tecnológico

- **Framework de Agentes**: LangChain con OpenAI
- **Backend API**: FastAPI
- **Base de Datos**: SQLite (memoria persistente)
- **LLM**: OpenAI GPT (via API preconfigurada)
- **Frontend**: React + TypeScript + TailwindCSS
- **Integración**: GitHub API para versionado

## Estructura de Datos

### Tarea (Task)
```json
{
  "id": "uuid",
  "project": "ConsorcioOpt|SocialConsorcio|SocialEmprendedores",
  "title": "string",
  "description": "string",
  "status": "pending|in_progress|completed|blocked",
  "priority": "low|medium|high|urgent",
  "assigned_agent": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "completed_at": "datetime|null",
  "notes": "string",
  "subtasks": []
}
```

### Memoria del Agente
```json
{
  "agent_id": "string",
  "project": "string",
  "context": "string",
  "personality_traits": {},
  "conversation_history": [],
  "decisions_made": [],
  "last_active": "datetime"
}
```

## Flujo de Trabajo

1. **Entrada de Tarea** (via API o interfaz web)
2. **Coordinador** analiza y asigna al agente apropiado
3. **Agente Especializado** procesa la tarea con su personalidad
4. **Sistema de Memoria** registra contexto y decisiones
5. **Actualización** de estado y generación de respuesta
6. **Reporte** disponible via API o interfaz

## Endpoints de API

### Tareas
- `POST /api/tasks` - Crear nueva tarea
- `GET /api/tasks` - Listar todas las tareas
- `GET /api/tasks/{task_id}` - Obtener tarea específica
- `PUT /api/tasks/{task_id}` - Actualizar tarea
- `DELETE /api/tasks/{task_id}` - Eliminar tarea

### Agentes
- `GET /api/agents` - Listar agentes y su estado
- `GET /api/agents/{agent_id}` - Info de agente específico
- `POST /api/agents/{agent_id}/chat` - Conversar con agente
- `GET /api/agents/{agent_id}/memory` - Ver memoria del agente

### Proyectos
- `GET /api/projects` - Listar proyectos
- `GET /api/projects/{project_id}/tasks` - Tareas de un proyecto
- `GET /api/projects/{project_id}/status` - Estado del proyecto

### Coordinación
- `POST /api/coordinate/assign` - Asignar tarea manualmente
- `GET /api/coordinate/report` - Reporte general del sistema

## Personalidades de los Agentes

### OptimizadorConsorcio
- **Tono**: Profesional, analítico, directo
- **Enfoque**: Eficiencia, métricas, procesos
- **Estilo**: Estructurado, basado en datos
- **Prompt base**: "Eres un experto en optimización de procesos administrativos..."

### SocialManagerConsorcio
- **Tono**: Amigable, profesional, cercano
- **Enfoque**: Engagement, branding, comunicación
- **Estilo**: Creativo, visual, orientado a audiencia
- **Prompt base**: "Eres un community manager especializado en servicios..."

### MentorEmprendedor
- **Tono**: Inspirador, motivador, educativo
- **Enfoque**: Enseñanza, mentoría, crecimiento
- **Estilo**: Empático, práctico, orientado a acción
- **Prompt base**: "Eres un mentor experimentado que ayuda a emprendedores..."

## Seguridad y Control

- **Autenticación**: API keys para acceso externo
- **Rate limiting**: Prevenir abuso
- **Logs**: Registro completo de operaciones
- **Validación**: Sanitización de inputs
- **Backup**: Exportación periódica de memoria

## Escalabilidad

El sistema está diseñado para:
- Agregar nuevos proyectos fácilmente
- Crear nuevos agentes especializados
- Integrar con servicios externos
- Escalar horizontalmente si es necesario
