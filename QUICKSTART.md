# Guía Rápida de Uso 🚀

## Instalación Rápida

```bash
# Clonar el repositorio
git clone https://github.com/julioarielfernandez-star/multi-agent-project-manager.git
cd multi-agent-project-manager

# Crear entorno virtual e instalar dependencias
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Probar el sistema
python test_system.py
```

## Uso Inmediato

### 1. Iniciar la API

```bash
python api.py
```

La API estará en `http://localhost:8000`

### 2. Abrir la Interfaz Web

Navega a: `http://localhost:8000/index.html`

### 3. Crear tu Primera Tarea

**Desde la interfaz web:**
- Selecciona un proyecto
- Escribe el título y descripción
- Elige la prioridad
- Haz clic en "Crear Tarea"
- ¡El agente la procesará automáticamente!

**Desde código Python:**

```python
from database import DatabaseManager
from agents import ProjectCoordinator

db = DatabaseManager()
coordinator = ProjectCoordinator(db)

# Crear tarea
task = db.create_task(
    project="SocialEmprendedores",
    title="Crear post sobre productividad",
    description="Tips para emprendedores sobre gestión del tiempo",
    priority="high"
)

# Asignar al agente
result = coordinator.assign_task(task)
print(result['result'])
```

**Desde otra IA (usando la API):**

```python
import requests

# Crear tarea
response = requests.post("http://localhost:8000/api/tasks", json={
    "project": "ConsorcioOpt",
    "title": "Optimizar proceso de cobranza",
    "description": "Reducir tiempo de cobranza de 45 a 30 días",
    "priority": "urgent"
})

print(response.json())
```

## Los 3 Agentes

### 1. OptimizadorConsorcio (ConsorcioOpt)
**Especialidad:** Optimización de procesos administrativos  
**Úsalo para:** Análisis de eficiencia, identificación de cuellos de botella, propuestas de mejora

**Ejemplo:**
```python
task = db.create_task(
    project="ConsorcioOpt",
    title="Analizar proceso de atención al cliente",
    description="Identificar puntos de mejora en el servicio",
    priority="high"
)
```

### 2. SocialManagerConsorcio (SocialConsorcio)
**Especialidad:** Gestión de redes sociales para servicios  
**Úsalo para:** Calendario editorial, creación de contenido, análisis de métricas

**Ejemplo:**
```python
task = db.create_task(
    project="SocialConsorcio",
    title="Calendario de contenido enero",
    description="Planificar posts para todo el mes",
    priority="medium"
)
```

### 3. MentorEmprendedor (SocialEmprendedores)
**Especialidad:** Mentoría y asesoramiento para emprendedores  
**Úsalo para:** Contenido educativo, tips, casos de éxito

**Ejemplo:**
```python
task = db.create_task(
    project="SocialEmprendedores",
    title="Serie sobre financiamiento",
    description="5 posts sobre opciones de financiamiento para startups",
    priority="high"
)
```

## Conversar con un Agente

```python
# Obtener el agente
mentor = coordinator.get_agent('SocialEmprendedores')

# Conversar
response = mentor.chat("¿Cómo validar una idea de negocio?")
print(response)
```

**O desde la API:**

```bash
curl -X POST http://localhost:8000/api/agents/SocialEmprendedores/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Dame 5 ideas de posts para esta semana"}'
```

## Ver Estado del Sistema

```python
# Reporte general
report = coordinator.generate_report()
print(report)

# Estado de un agente específico
memory = db.get_agent_memory('OptimizadorConsorcio')
print(memory)

# Todas las tareas
tasks = db.get_all_tasks()
for task in tasks:
    print(f"{task['title']} - {task['status']}")
```

## Endpoints de API Más Usados

### Crear Tarea
```bash
POST /api/tasks
{
  "project": "ConsorcioOpt",
  "title": "Título",
  "description": "Descripción",
  "priority": "high"
}
```

### Listar Tareas
```bash
GET /api/tasks
GET /api/tasks?project=ConsorcioOpt
GET /api/tasks?status=completed
```

### Chat con Agente
```bash
POST /api/agents/SocialEmprendedores/chat
{
  "message": "Tu pregunta aquí"
}
```

### Reporte del Sistema
```bash
GET /api/coordinate/report
```

## Integración con Otras IAs

### Desde ChatGPT (Code Interpreter)

```python
import requests

API_URL = "http://tu-servidor:8000"

# Crear tarea
requests.post(f"{API_URL}/api/tasks", json={
    "project": "SocialEmprendedores",
    "title": "Post sobre liderazgo",
    "description": "Contenido inspirador sobre liderazgo en startups",
    "priority": "medium"
})

# Ver todas las tareas
tasks = requests.get(f"{API_URL}/api/tasks").json()
for task in tasks:
    print(f"- {task['title']} ({task['status']})")
```

### Desde Claude (MCP o Code)

```python
from database import DatabaseManager
from agents import ProjectCoordinator

# Inicializar
db = DatabaseManager()
coordinator = ProjectCoordinator(db)

# Usar directamente
task = db.create_task(
    project="ConsorcioOpt",
    title="Tu tarea",
    description="Descripción",
    priority="high"
)

result = coordinator.assign_task(task)
```

## Consejos Rápidos

1. **Sé específico en las descripciones** - Los agentes generan mejores planes con más contexto
2. **Usa prioridades correctamente** - `urgent` para tareas críticas, `low` para ideas futuras
3. **Revisa la memoria de los agentes** - Mantienen contexto entre sesiones
4. **Conversa con los agentes** - Pueden darte consejos específicos sobre el proyecto
5. **Usa la API para automatizar** - Perfecto para integraciones con otros sistemas

## Solución de Problemas

### Error al iniciar la API
```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate

# Reinstala dependencias si es necesario
pip install -r requirements.txt
```

### Base de datos corrupta
```bash
# Elimina y se recreará automáticamente
rm multi_agent_system.db
python test_system.py
```

### Puerto 8000 ocupado
```python
# En api.py, cambia el puerto al final:
uvicorn.run(app, host="0.0.0.0", port=8080)  # Usa 8080 en vez de 8000
```

## Próximos Pasos

1. Explora la documentación completa en `README.md`
2. Revisa la arquitectura en `ARCHITECTURE.md`
3. Personaliza los agentes en `agents.py`
4. Agrega nuevos proyectos según tus necesidades
5. Integra con tus herramientas favoritas

---

**¿Preguntas?** Abre un issue en GitHub o revisa la documentación completa.

¡Disfruta gestionando proyectos con agentes inteligentes! 🎉
