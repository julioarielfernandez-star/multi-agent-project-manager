# AgentesIA-PMI

Multi-Agent AI System for Project Management based on PMI (Project Management Institute) standards.

## Overview

This system implements three specialized AI agents that work together to manage projects following PMI best practices and PMBOK (Project Management Body of Knowledge) principles:

1. **Planning Agent** - Handles project planning, scope definition, WBS creation, and resource planning
2. **Execution Agent** - Manages project execution, task breakdown, team coordination, and issue resolution
3. **Monitoring Agent** - Tracks progress, analyzes performance, evaluates changes, and identifies risks

## Features

- PMI-compliant project planning and management
- Automated Work Breakdown Structure (WBS) generation
- Intelligent task breakdown and assignment recommendations
- Project performance analysis and reporting
- Risk assessment and monitoring
- Integration with Notion for task management
- Interactive command-line interface

## Architecture

```
AgentesIA-PMI/
├── agents/
│   ├── base_agent.py          # Base agent class
│   ├── planning_agent.py      # Planning specialist
│   ├── execution_agent.py     # Execution coordinator
│   └── monitoring_agent.py    # Monitoring & control specialist
├── config/
│   └── settings.py            # Configuration management
├── utils/
│   └── notion_client.py       # Notion API integration
├── data/                      # Data storage
├── logs/                      # Log files
├── main.py                    # Main application
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## Prerequisites

- Python 3.8 or higher
- Anthropic API key (for Claude AI)
- Notion API key (optional, for task management)
- Notion database ID (optional)

## Installation

### 1. Clone or Navigate to the Project

```bash
cd AgentesIA-PMI
```

### 2. Create Virtual Environment

**On Linux/Mac:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Anthropic API Configuration
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Notion API Configuration (optional)
NOTION_API_KEY=your_notion_api_key_here
NOTION_DATABASE_ID=your_notion_database_id_here

# Agent Configuration
DEFAULT_MODEL=claude-3-5-sonnet-20241022
MAX_TOKENS=4096
TEMPERATURE=0.7
```

### 5. Get Your API Keys

**Anthropic API Key:**
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key

**Notion API Key (Optional):**
1. Go to https://www.notion.so/my-integrations
2. Create a new integration
3. Copy the Internal Integration Token
4. Create a database in Notion
5. Share the database with your integration
6. Copy the database ID from the URL

## Usage

### Interactive Mode

Run the main application:

```bash
python main.py
```

Available commands:
- `plan` - Start planning phase for a project
- `execute` - Break down work packages into tasks
- `monitor` - Analyze project performance
- `status` - Check Notion task status (if configured)
- `help` - Show available commands
- `exit` - Exit the system

### Programmatic Usage

```python
from agents.planning_agent import PlanningAgent
from agents.execution_agent import ExecutionAgent
from agents.monitoring_agent import MonitoringAgent

# Initialize agents
planning_agent = PlanningAgent()
execution_agent = ExecutionAgent()
monitoring_agent = MonitoringAgent()

# Use planning agent
project_plan = planning_agent.create_project_plan(
    "Develop a mobile application for task management"
)

# Use execution agent
tasks = execution_agent.create_task_breakdown(
    "Design and implement user authentication system"
)

# Use monitoring agent
report = monitoring_agent.analyze_progress(
    "Planned: 10 tasks, Actual: 7 completed, 2 in progress, 1 blocked"
)
```

## Agent Capabilities

### Planning Agent

- Create comprehensive project plans
- Generate Work Breakdown Structures (WBS)
- Analyze and refine requirements
- Estimate resources and timelines
- Identify risks and constraints
- Define project scope and objectives

### Execution Agent

- Break down work packages into actionable tasks
- Generate team assignment recommendations
- Resolve project issues
- Create status updates
- Coordinate team activities
- Manage quality assurance

### Monitoring Agent

- Analyze project progress and variances
- Evaluate change requests
- Assess and prioritize risks
- Generate performance reports
- Calculate KPIs (SPI, CPI, etc.)
- Identify workflow bottlenecks

## PMI Knowledge Areas Covered

This system addresses the following PMI knowledge areas:

1. **Project Integration Management** - Coordinating all aspects of the project
2. **Project Scope Management** - Defining and controlling project scope
3. **Project Schedule Management** - Planning and controlling project timeline
4. **Project Cost Management** - Planning and controlling project budget
5. **Project Quality Management** - Ensuring deliverables meet requirements
6. **Project Resource Management** - Managing team and resources
7. **Project Communications Management** - Stakeholder communications
8. **Project Risk Management** - Identifying and managing risks
9. **Project Procurement Management** - Managing external resources
10. **Project Stakeholder Management** - Managing stakeholder engagement

## Examples

### Example 1: Planning a Software Project

```python
planning_agent = PlanningAgent()

plan = planning_agent.create_project_plan("""
Develop a web-based customer portal that allows users to:
- View their account information
- Submit support tickets
- Track order status
- Download invoices

Timeline: 3 months
Team: 2 developers, 1 designer, 1 QA engineer
""")

print(plan)
```

### Example 2: Breaking Down Tasks

```python
execution_agent = ExecutionAgent()

tasks = execution_agent.create_task_breakdown("""
Implement user authentication system with:
- Email/password login
- OAuth integration (Google, Facebook)
- Password reset functionality
- Two-factor authentication
""")

print(tasks)
```

### Example 3: Monitoring Progress

```python
monitoring_agent = MonitoringAgent()

report = monitoring_agent.analyze_progress("""
Project: Customer Portal Development
Planned completion: 80%
Actual completion: 65%
Completed tasks: 13/20
In progress: 4
Blocked: 1 (waiting for API access)
Behind schedule by: 2 weeks
""")

print(report)
```

## Notion Integration

If you configure Notion integration, the system can:

- Create tasks automatically in your Notion database
- Update task statuses
- Retrieve current project status
- Add comments and notes

Make sure your Notion database has these properties:
- Name (title)
- Status (status)
- Priority (select)
- Description (rich text)
- Assigned To (rich text)

## Troubleshooting

### Missing API Keys Error

If you see "Missing required environment variables", ensure:
1. You created a `.env` file (not just `.env.example`)
2. You added valid API keys to the `.env` file
3. The `.env` file is in the same directory as `main.py`

### Notion Connection Issues

If Notion integration fails:
1. Verify your integration has access to the database
2. Check that the database ID is correct
3. Ensure the database has the required properties

### Agent Response Issues

If agents don't respond properly:
1. Check your Anthropic API key is valid
2. Verify you have API credits available
3. Check your internet connection
4. Review the error messages in the console

## Best Practices

1. **Start with Planning** - Always run the planning phase before execution
2. **Be Specific** - Provide detailed project descriptions for better results
3. **Iterate** - Use conversation history to refine outputs
4. **Monitor Regularly** - Run monitoring phase frequently to catch issues early
5. **Document Decisions** - Use Notion or logs to track agent recommendations

## Contributing

Contributions are welcome! Areas for enhancement:

- Additional specialized agents (closing, risk management)
- Enhanced Notion integration
- Integration with other PM tools (Jira, Asana)
- Web interface
- Report export (PDF, Excel)
- Automated scheduling

## License

This project is provided as-is for educational and professional use.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the example code
3. Consult PMI/PMBOK documentation for methodology questions

## Acknowledgments

- Built with Anthropic's Claude AI
- Based on PMI/PMBOK standards
- Notion API for task management

---

**Version:** 1.0.0
**Last Updated:** 2025
