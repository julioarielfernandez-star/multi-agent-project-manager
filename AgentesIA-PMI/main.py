#!/usr/bin/env python3
"""
AgentesIA-PMI - Multi-Agent Project Management System
Based on PMI (Project Management Institute) standards
"""

import sys
from config.settings import settings
from agents.planning_agent import PlanningAgent
from agents.execution_agent import ExecutionAgent
from agents.monitoring_agent import MonitoringAgent
from utils.notion_client import NotionManager

class ProjectManagementSystem:
    """Main orchestrator for the multi-agent PMI system"""

    def __init__(self):
        print("Initializing AI Agents for PMI...")

        try:
            settings.validate()
        except ValueError as e:
            print(f"Configuration Error: {e}")
            print("\nPlease ensure you have:")
            print("1. Created a .env file based on .env.example")
            print("2. Added your API keys and configuration")
            sys.exit(1)

        self.planning_agent = PlanningAgent()
        self.execution_agent = ExecutionAgent()
        self.monitoring_agent = MonitoringAgent()
        self.notion = NotionManager()

        print("All agents initialized successfully!")

    def run_planning_phase(self, project_description):
        """Execute the planning phase"""
        print("\n=== PLANNING PHASE ===")
        print(f"Planning Agent: Analyzing project...")

        plan = self.planning_agent.create_project_plan(project_description)

        if plan:
            print("\nProject Plan Generated:")
            print("-" * 80)
            print(plan)
            print("-" * 80)

        return plan

    def run_execution_phase(self, work_package):
        """Execute the execution phase"""
        print("\n=== EXECUTION PHASE ===")
        print(f"Execution Agent: Breaking down work package...")

        tasks = self.execution_agent.create_task_breakdown(work_package)

        if tasks:
            print("\nTask Breakdown:")
            print("-" * 80)
            print(tasks)
            print("-" * 80)

        return tasks

    def run_monitoring_phase(self, project_data):
        """Execute the monitoring phase"""
        print("\n=== MONITORING PHASE ===")
        print(f"Monitoring Agent: Analyzing project performance...")

        report = self.monitoring_agent.generate_performance_report(project_data)

        if report:
            print("\nPerformance Report:")
            print("-" * 80)
            print(report)
            print("-" * 80)

        return report

    def interactive_mode(self):
        """Run the system in interactive mode"""
        print("\n" + "=" * 80)
        print("AI AGENTS FOR PMI - INTERACTIVE MODE")
        print("=" * 80)
        print("\nAvailable Commands:")
        print("  1. plan    - Start planning phase")
        print("  2. execute - Start execution phase")
        print("  3. monitor - Start monitoring phase")
        print("  4. status  - Check project status")
        print("  5. help    - Show this help")
        print("  6. exit    - Exit the system")
        print("=" * 80)

        while True:
            try:
                command = input("\nEnter command: ").strip().lower()

                if command in ['exit', 'quit', '6']:
                    print("\nShutting down AI Agents for PMI. Goodbye!")
                    break

                elif command in ['plan', '1']:
                    description = input("\nEnter project description: ")
                    self.run_planning_phase(description)

                elif command in ['execute', '2']:
                    work_package = input("\nEnter work package description: ")
                    self.run_execution_phase(work_package)

                elif command in ['monitor', '3']:
                    data = input("\nEnter project data (or press Enter for sample): ")
                    if not data:
                        data = "Sample project with 10 tasks, 7 completed, 3 in progress"
                    self.run_monitoring_phase(data)

                elif command in ['status', '4']:
                    print("\nFetching project status from Notion...")
                    tasks = self.notion.get_tasks()
                    print(f"\nFound {len(tasks)} tasks in Notion database")

                elif command in ['help', '5']:
                    print("\nAvailable Commands:")
                    print("  1. plan    - Start planning phase")
                    print("  2. execute - Start execution phase")
                    print("  3. monitor - Start monitoring phase")
                    print("  4. status  - Check project status")
                    print("  5. help    - Show this help")
                    print("  6. exit    - Exit the system")

                else:
                    print(f"\nUnknown command: '{command}'. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\n\nInterrupted. Shutting down...")
                break
            except Exception as e:
                print(f"\nError: {e}")

def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║         AI AGENTS FOR PMI                             ║
    ║    Multi-Agent Project Management System              ║
    ║         Based on PMI Standards                        ║
    ╚═══════════════════════════════════════════════════════╝
    """)

    system = ProjectManagementSystem()
    system.interactive_mode()

if __name__ == "__main__":
    main()
