from agents.base_agent import BaseAgent

class PlanningAgent(BaseAgent):
    """
    Planning Agent - Specializes in project planning following PMI standards
    Responsible for:
    - Developing project scope
    - Creating work breakdown structures (WBS)
    - Defining project objectives
    - Resource planning
    - Schedule development
    """

    def __init__(self):
        super().__init__(
            name="Planning Agent",
            role="Project Planning Specialist"
        )

    def get_system_prompt(self):
        return """You are a Project Planning Specialist trained in PMI (Project Management Institute) standards and best practices.

Your responsibilities include:
1. Analyzing project requirements and defining clear objectives
2. Creating comprehensive Work Breakdown Structures (WBS)
3. Identifying project deliverables and milestones
4. Estimating resource requirements and timelines
5. Identifying potential risks and constraints
6. Developing project scope statements
7. Creating project schedules using critical path method

You should follow PMI guidelines and PMBOK (Project Management Body of Knowledge) principles.
Always provide structured, detailed, and actionable planning outputs.
Consider stakeholder requirements, constraints, and success criteria in all planning activities.

When analyzing a project, break it down into:
- Initiation elements
- Planning components
- Key deliverables
- Resource requirements
- Timeline estimates
- Risk factors

Provide your responses in a clear, organized format that can be easily implemented."""

    def create_project_plan(self, project_description):
        """Generate a comprehensive project plan"""
        prompt = f"""Create a detailed project plan for the following project:

{project_description}

Please provide:
1. Project Scope Statement
2. Work Breakdown Structure (WBS)
3. Key Deliverables
4. Resource Requirements
5. Estimated Timeline
6. Risk Assessment
7. Success Criteria"""

        return self.send_message(prompt)

    def create_wbs(self, project_description):
        """Create a Work Breakdown Structure"""
        prompt = f"""Create a detailed Work Breakdown Structure (WBS) for:

{project_description}

Break down the project into phases, deliverables, and work packages.
Use hierarchical numbering (1.0, 1.1, 1.1.1, etc.)"""

        return self.send_message(prompt)

    def analyze_requirements(self, requirements):
        """Analyze and refine project requirements"""
        prompt = f"""Analyze the following project requirements and provide:
1. Clarified and refined requirements
2. Potential gaps or missing elements
3. Dependencies between requirements
4. Priority recommendations

Requirements:
{requirements}"""

        return self.send_message(prompt)
