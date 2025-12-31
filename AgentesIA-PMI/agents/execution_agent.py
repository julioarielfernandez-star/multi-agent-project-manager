from agents.base_agent import BaseAgent

class ExecutionAgent(BaseAgent):
    """
    Execution Agent - Specializes in project execution and coordination
    Responsible for:
    - Task assignment and delegation
    - Team coordination
    - Resource allocation
    - Quality assurance
    - Stakeholder communication
    """

    def __init__(self):
        super().__init__(
            name="Execution Agent",
            role="Project Execution Coordinator"
        )

    def get_system_prompt(self):
        return """You are a Project Execution Coordinator specialized in PMI execution processes.

Your responsibilities include:
1. Breaking down work packages into actionable tasks
2. Creating clear task assignments with acceptance criteria
3. Coordinating team activities and dependencies
4. Ensuring quality standards are met
5. Managing stakeholder communications
6. Resolving conflicts and issues
7. Facilitating team collaboration
8. Tracking deliverable completion

You follow PMI best practices for project execution, including:
- Direct and manage project work
- Manage project knowledge
- Manage quality
- Acquire and develop team
- Manage communications
- Implement risk responses
- Conduct procurements
- Engage stakeholders

Provide clear, actionable guidance that helps teams execute work effectively.
Focus on practical implementation while maintaining alignment with project objectives.
Consider resource constraints, dependencies, and quality requirements."""

    def create_task_breakdown(self, work_package):
        """Break down a work package into specific tasks"""
        prompt = f"""Break down the following work package into specific, actionable tasks:

{work_package}

For each task, provide:
1. Task title
2. Description
3. Estimated effort
4. Required skills/resources
5. Dependencies
6. Acceptance criteria"""

        return self.send_message(prompt)

    def generate_team_assignments(self, tasks, team_info):
        """Generate task assignments based on team capabilities"""
        prompt = f"""Given the following tasks and team information, suggest optimal task assignments:

Tasks:
{tasks}

Team Information:
{team_info}

Provide:
1. Recommended assignments
2. Rationale for each assignment
3. Potential workload concerns
4. Skill development opportunities"""

        return self.send_message(prompt)

    def resolve_issue(self, issue_description):
        """Provide guidance on resolving project issues"""
        prompt = f"""Analyze the following project issue and provide resolution guidance:

Issue:
{issue_description}

Provide:
1. Root cause analysis
2. Recommended actions
3. Risk mitigation steps
4. Communication plan
5. Preventive measures"""

        return self.send_message(prompt)

    def create_status_update(self, current_status):
        """Generate a project status update"""
        prompt = f"""Create a comprehensive project status update based on:

{current_status}

Include:
1. Accomplishments since last update
2. Current activities
3. Upcoming milestones
4. Issues and risks
5. Action items
6. Overall health assessment"""

        return self.send_message(prompt)
