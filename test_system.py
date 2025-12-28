"""
Script de Prueba del Sistema Multi-Agente
Prueba todas las funcionalidades principales
"""

from database import DatabaseManager
from agents import ProjectCoordinator
import json

def test_system():
    """Prueba completa del sistema"""
    
    print("=" * 60)
    print("PRUEBA DEL SISTEMA MULTI-AGENTE")
    print("=" * 60)
    
    # Inicializar sistema
    print("\n1. Inicializando sistema...")
    db = DatabaseManager()
    coordinator = ProjectCoordinator(db)
    print("✓ Sistema inicializado correctamente")
    
    # Crear tareas de prueba
    print("\n2. Creando tareas de prueba...")
    
    tasks_data = [
        {
            "project": "ConsorcioOpt",
            "title": "Analizar proceso de cobranza actual",
            "description": "Revisar el proceso actual de cobranza de expensas e identificar puntos de mejora",
            "priority": "high"
        },
        {
            "project": "SocialConsorcio",
            "title": "Crear calendario de contenido para diciembre",
            "description": "Planificar posts para redes sociales durante el mes de diciembre, incluyendo tips de fin de año",
            "priority": "medium"
        },
        {
            "project": "SocialEmprendedores",
            "title": "Post sobre gestión del tiempo para emprendedores",
            "description": "Crear contenido inspirador sobre cómo los emprendedores pueden gestionar mejor su tiempo",
            "priority": "medium"
        }
    ]
    
    created_tasks = []
    for task_data in tasks_data:
        task = db.create_task(**task_data)
        created_tasks.append(task)
        print(f"✓ Tarea creada: {task['title']}")
    
    # Asignar tareas a agentes
    print("\n3. Asignando tareas a agentes...")
    results = []
    for task in created_tasks:
        result = coordinator.assign_task(task)
        results.append(result)
        print(f"✓ Tarea '{task['title']}' asignada a {result['agent']}")
    
    # Mostrar respuestas de los agentes
    print("\n4. Respuestas de los agentes:")
    print("-" * 60)
    for i, result in enumerate(results):
        print(f"\nTarea {i+1}: {created_tasks[i]['title']}")
        print(f"Agente: {result['agent']}")
        
        if 'result' in result and isinstance(result['result'], dict):
            agent_result = result['result']
            print(f"\nAnálisis:")
            print(agent_result.get('analisis', 'N/A'))
            
            print(f"\nPlan de Acción:")
            for j, step in enumerate(agent_result.get('plan_accion', []), 1):
                print(f"  {j}. {step}")
            
            print(f"\nSubtareas:")
            for j, subtask in enumerate(agent_result.get('subtareas', []), 1):
                print(f"  • {subtask}")
            
            print(f"\nEstado Sugerido: {agent_result.get('estado_sugerido', 'N/A')}")
        
        print("-" * 60)
    
    # Probar chat con un agente
    print("\n5. Probando chat con agente MentorEmprendedor...")
    mentor = coordinator.get_agent('SocialEmprendedores')
    chat_response = mentor.chat("¿Cuáles son los 3 errores más comunes que cometen los emprendedores al comenzar?")
    print(f"\nRespuesta del Mentor:")
    print(chat_response)
    
    # Obtener estado de agentes
    print("\n6. Estado de todos los agentes:")
    agents_status = coordinator.get_all_agents_status()
    for project, status in agents_status.items():
        print(f"\n{project}:")
        print(f"  - Agente: {status['agent_id']}")
        print(f"  - Tareas completadas: {status['total_tasks_completed']}")
        print(f"  - Última actividad: {status['last_active']}")
    
    # Generar reporte del sistema
    print("\n7. Reporte del sistema:")
    report = coordinator.generate_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    
    # Obtener todas las tareas
    print("\n8. Lista de todas las tareas:")
    all_tasks = db.get_all_tasks()
    for task in all_tasks:
        print(f"  • [{task['status']}] {task['title']} - {task['project']}")
    
    print("\n" + "=" * 60)
    print("PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 60)
    print("\nEl sistema está funcionando correctamente.")
    print("Puedes iniciar la API con: python api.py")
    print("Y abrir la interfaz web en: http://localhost:8000/index.html")
    print("\nO usar la API directamente desde otras aplicaciones/IAs.")

if __name__ == "__main__":
    test_system()
