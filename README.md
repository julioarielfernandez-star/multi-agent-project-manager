# Multi-Agent Project Manager 🤖

Sistema multi-agente inteligente para gestionar proyectos con agentes especializados que tienen memoria, personalidad única y capacidad de ser controlados desde otras IAs.

## 🎯 Proyectos Gestionados

### 1. ConsorcioOpt - Optimización de Administración de Consorcios
**Agente:** OptimizadorConsorcio  
**Personalidad:** Analítico, eficiente, orientado a procesos  
**Especialidad:** Optimización de procesos administrativos, identificación de ineficiencias, propuestas de mejora basadas en datos

### 2. SocialConsorcio - Canal de Redes Sociales para Administración
**Agente:** SocialManagerConsorcio  
**Personalidad:** Creativo, comunicativo, orientado a engagement  
**Especialidad:** Gestión de redes sociales, creación de contenido, calendario editorial, análisis de métricas

### 3. SocialEmprendedores - Canal de Redes Sociales para Emprendedores
**Agente:** MentorEmprendedor  
**Personalidad:** Inspirador, educativo, empático  
**Especialidad:** Mentoría para emprendedores, contenido educativo, tips prácticos, casos de éxito

## 🚀 Características Principales

- ✅ **3 Agentes Especializados** con personalidades únicas
- ✅ **Memoria Persistente** (SQLite) - Los agentes recuerdan contexto y decisiones
- ✅ **API REST Completa** - Control desde cualquier aplicación o IA
- ✅ **Interfaz Web** - Visualización y gestión de tareas
- ✅ **Multi-Agente** - Los agentes se coordinan automáticamente
- ✅ **Procesamiento Inteligente** - Usa GPT-4 para análisis y respuestas
- ✅ **Sistema de Logs** - Registro completo de todas las operaciones
- ✅ **Chat con Agentes** - Conversa directamente con cada agente

## 📋 Requisitos

- Python 3.11+
- OpenAI API Key (preconfigurada en el ambiente)
- Dependencias: ver `requirements.txt`

## 🛠️ Instalación

```bash
# Clonar el repositorio
git clone <tu-repo>
cd multi-agent-project-manager

# Crear entorno virtual
python3.11 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Probar el sistema
python test_system.py
```

## 🎮 Uso

### Opción 1: API REST (Recomendado para control desde otras IAs)

```bash
# Iniciar el servidor API
python api.py
```

La API estará disponible en `http://localhost:8000`

### Opción 2: Interfaz Web

```bash
# Iniciar el servidor
python api.py

# Abrir en el navegador
# http://localhost:8000/index.html
```

### Opción 3: Uso Programático

```python
from database import DatabaseManager
from agents import ProjectCoordinator

# Inicializar sistema
db = DatabaseManager()
coordinator = ProjectCoordinator(db)

# Crear una tarea
task = db.create_task(
    project="ConsorcioOpt",
    title="Analizar proceso de cobranza",
    description="Revisar el proceso actual e identificar mejoras",
    priority="high"
)

# Asignar al agente apropiado
result = coordinator.assign_task(task)
print(result)

# Conversar con un agente
agent = coordinator.get_agent('SocialEmprendedores')
response = agent.chat("¿Qué consejos tienes para emprendedores?")
print(response)
```

## 📡 API Endpoints

### Tareas
- `POST /api/tasks` - Crear nueva tarea
- `GET /api/tasks` - Listar todas las tareas
- `GET /api/tasks/{task_id}` - Obtener tarea específica
- `PUT /api/tasks/{task_id}` - Actualizar tarea
- `DELETE /api/tasks/{task_id}` - Eliminar tarea

### Agentes
- `GET /api/agents` - Listar todos los agentes
- `GET /api/agents/{project}` - Info de agente específico
- `POST /api/agents/{project}/chat` - Conversar con agente
- `GET /api/agents/{project}/memory` - Ver memoria del agente

### Proyectos
- `GET /api/projects` - Listar proyectos
- `GET /api/projects/{project_id}/tasks` - Tareas de un proyecto
- `GET /api/projects/{project_id}/status` - Estado del proyecto

### Coordinación
- `POST /api/coordinate/assign` - Asignar tarea manualmente
- `GET /api/coordinate/report` - Reporte general del sistema

### Logs
- `GET /api/logs` - Obtener logs del sistema

## 🔌 Usar desde Otra IA (ChatGPT, Claude, etc.)

### Ejemplo con Python (desde cualquier IA que ejecute código):

```python
import requests

API_URL = "http://tu-servidor:8000"

# Crear una tarea
response = requests.post(f"{API_URL}/api/tasks", json={
    "project": "SocialEmprendedores",
    "title": "Crear post sobre financiamiento",
    "description": "Contenido sobre opciones de financiamiento para startups",
    "priority": "high"
})

task_result = response.json()
print(f"Tarea creada: {task_result['task']['id']}")
print(f"Respuesta del agente: {task_result['agent_response']}")

# Conversar con un agente
chat_response = requests.post(
    f"{API_URL}/api/agents/SocialEmprendedores/chat",
    json={"message": "Dame 5 ideas de posts para esta semana"}
)

print(chat_response.json()['agent_response'])
```

### Ejemplo con cURL:

```bash
# Crear tarea
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "project": "ConsorcioOpt",
    "title": "Optimizar proceso de pagos",
    "description": "Analizar y mejorar el sistema de pagos",
    "priority": "urgent"
  }'

# Chat con agente
curl -X POST http://localhost:8000/api/agents/MentorEmprendedor/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cómo validar una idea de negocio?"}'
```

## 📊 Estructura del Proyecto

```
multi-agent-project-manager/
├── database.py           # Sistema de base de datos (SQLite)
├── agents.py            # Agentes especializados con personalidades
├── api.py               # API REST con FastAPI
├── test_system.py       # Script de prueba
├── index.html           # Interfaz web
├── ARCHITECTURE.md      # Documentación de arquitectura
├── README.md            # Este archivo
├── requirements.txt     # Dependencias Python
└── multi_agent_system.db # Base de datos (se crea automáticamente)
```

## 🧠 Cómo Funcionan los Agentes

Cada agente:
1. **Recibe una tarea** del coordinador
2. **Analiza** la tarea según su personalidad y especialidad
3. **Genera un plan de acción** con pasos específicos
4. **Identifica subtareas** si es necesario
5. **Registra en memoria** todo el contexto y decisiones
6. **Actualiza el estado** de la tarea
7. **Puede conversar** sobre el proyecto en cualquier momento

La memoria persistente permite que los agentes:
- Recuerden conversaciones anteriores
- Mantengan contexto entre sesiones
- Aprendan de decisiones pasadas
- Proporcionen respuestas consistentes

## 🔐 Seguridad

- La API acepta conexiones desde cualquier origen (CORS habilitado)
- Para producción, configura autenticación y HTTPS
- Los datos se almacenan localmente en SQLite
- No se exponen claves API en el código

## 🚀 Despliegue

### Local
```bash
python api.py
```

### Docker (próximamente)
```bash
docker build -t multi-agent-pm .
docker run -p 8000:8000 multi-agent-pm
```

### Cloud (Railway, Render, etc.)
1. Sube el repositorio a GitHub
2. Conecta con tu servicio de hosting
3. Configura las variables de entorno
4. Despliega

## 📝 Ejemplos de Uso Real

### Caso 1: Automatizar Gestión de Redes Sociales
```python
# Crear 5 tareas de contenido para la semana
for day in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]:
    db.create_task(
        project="SocialEmprendedores",
        title=f"Post {day}",
        description=f"Crear contenido inspirador para {day}",
        priority="medium"
    )
```

### Caso 2: Optimización de Procesos
```python
# El agente analiza y propone mejoras
task = db.create_task(
    project="ConsorcioOpt",
    title="Reducir tiempo de cobranza",
    description="Actual: 45 días. Objetivo: 30 días",
    priority="urgent"
)
result = coordinator.assign_task(task)
# El agente genera un plan detallado de optimización
```

### Caso 3: Mentoría Continua
```python
# Conversar con el mentor sobre desafíos
mentor = coordinator.get_agent('SocialEmprendedores')
response = mentor.chat("Mi startup no está creciendo, ¿qué hago?")
# El agente proporciona consejos personalizados
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

MIT License - Usa libremente para proyectos personales o comerciales

## 👨‍💻 Autor

Creado con ❤️ por Manus AI

## 📞 Soporte

Para preguntas o problemas:
- Abre un issue en GitHub
- Revisa la documentación en `ARCHITECTURE.md`
- Ejecuta `python test_system.py` para diagnóstico

---

**¡Disfruta gestionando tus proyectos con agentes inteligentes!** 🚀
