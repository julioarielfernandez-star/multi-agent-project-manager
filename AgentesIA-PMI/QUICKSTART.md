# Quick Start Guide

Get started with AgentesIA-PMI in 5 minutes!

## Step 1: Install Dependencies

Make sure your virtual environment is activated, then:

```bash
pip install -r requirements.txt
```

## Step 2: Configure API Keys

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Anthropic API key:
```env
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Don't have an API key? Get one at: https://console.anthropic.com/

## Step 3: Run the System

### Option A: Interactive Mode

```bash
python main.py
```

Then use these commands:
- Type `plan` and describe your project
- Type `execute` to break down work packages
- Type `monitor` to analyze progress

### Option B: Run Examples

```bash
python example.py
```

This will demonstrate all agent capabilities with sample projects.

### Option C: Use Programmatically

```python
from agents.planning_agent import PlanningAgent

agent = PlanningAgent()
plan = agent.create_project_plan("Build a mobile app for task management")
print(plan)
```

## Next Steps

1. **Add Notion Integration** (Optional)
   - Get your Notion API key from https://www.notion.so/my-integrations
   - Create a database in Notion
   - Add credentials to `.env`

2. **Customize Agents**
   - Modify system prompts in agent files
   - Add new methods to agents
   - Create new specialized agents

3. **Integrate with Your Workflow**
   - Export agent outputs to your PM tool
   - Automate with scheduled runs
   - Build a web interface

## Common Issues

**"Missing required environment variables"**
- Make sure you created `.env` (not just `.env.example`)
- Check that ANTHROPIC_API_KEY is set

**"Import errors"**
- Activate your virtual environment
- Run `pip install -r requirements.txt`

## Documentation

- Full README: `README.md`
- Example code: `example.py`
- Agent reference: Check files in `agents/` directory

## Getting Help

- Review the examples in `example.py`
- Check agent docstrings for method details
- Consult PMI/PMBOK documentation for methodology

---

Ready to manage projects with AI? Run `python main.py` to get started!
