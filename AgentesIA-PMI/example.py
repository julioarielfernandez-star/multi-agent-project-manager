#!/usr/bin/env python3
"""
Example usage of the AgentesIA-PMI system
This script demonstrates how to use each agent programmatically
"""

from config.settings import settings
from agents.planning_agent import PlanningAgent
from agents.execution_agent import ExecutionAgent
from agents.monitoring_agent import MonitoringAgent

def example_planning():
    """Example: Using the Planning Agent"""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: PLANNING AGENT")
    print("=" * 80)

    agent = PlanningAgent()

    project_description = """
    Develop a customer relationship management (CRM) system with the following features:
    - Contact management
    - Sales pipeline tracking
    - Email integration
    - Reporting and analytics
    - Mobile app support

    Constraints:
    - 6-month timeline
    - Team of 4 developers, 1 designer, 1 QA engineer
    - Budget: $200,000
    - Must integrate with existing email system
    """

    print("\nProject Description:")
    print(project_description)
    print("\nGenerating project plan...\n")

    plan = agent.create_project_plan(project_description)

    if plan:
        print("\nProject Plan:")
        print("-" * 80)
        print(plan)
        print("-" * 80)

def example_wbs():
    """Example: Creating a Work Breakdown Structure"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: WORK BREAKDOWN STRUCTURE")
    print("=" * 80)

    agent = PlanningAgent()

    project_description = """
    Implement user authentication and authorization system for a web application
    """

    print("\nGenerating WBS...\n")

    wbs = agent.create_wbs(project_description)

    if wbs:
        print("\nWork Breakdown Structure:")
        print("-" * 80)
        print(wbs)
        print("-" * 80)

def example_execution():
    """Example: Using the Execution Agent"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: EXECUTION AGENT - TASK BREAKDOWN")
    print("=" * 80)

    agent = ExecutionAgent()

    work_package = """
    Work Package: Implement Email Integration Module

    Requirements:
    - Connect to Gmail and Outlook APIs
    - Sync emails automatically
    - Allow sending emails from within the app
    - Handle attachments
    - Implement email templates
    """

    print("\nWork Package:")
    print(work_package)
    print("\nBreaking down into tasks...\n")

    tasks = agent.create_task_breakdown(work_package)

    if tasks:
        print("\nTask Breakdown:")
        print("-" * 80)
        print(tasks)
        print("-" * 80)

def example_issue_resolution():
    """Example: Resolving a project issue"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: EXECUTION AGENT - ISSUE RESOLUTION")
    print("=" * 80)

    agent = ExecutionAgent()

    issue = """
    Issue: API Integration Delay

    The third-party payment gateway API that we planned to integrate is delayed.
    The vendor says it won't be available for another 3 weeks.
    This is blocking our checkout implementation and could delay the entire release.

    Context:
    - Planned release: 4 weeks from now
    - Checkout is a critical feature
    - Team is currently working on other features
    """

    print("\nIssue:")
    print(issue)
    print("\nGenerating resolution guidance...\n")

    resolution = agent.resolve_issue(issue)

    if resolution:
        print("\nResolution Guidance:")
        print("-" * 80)
        print(resolution)
        print("-" * 80)

def example_monitoring():
    """Example: Using the Monitoring Agent"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: MONITORING AGENT - PROGRESS ANALYSIS")
    print("=" * 80)

    agent = MonitoringAgent()

    progress_data = """
    Project: CRM System Development
    Sprint: 3 of 12

    Planned Progress: 25% (end of sprint 3)
    Actual Progress: 18%

    Tasks:
    - Planned: 30 tasks
    - Completed: 22 tasks
    - In Progress: 5 tasks
    - Blocked: 3 tasks

    Timeline:
    - Original End Date: June 30
    - Current Projection: July 15 (2 weeks delay)

    Issues:
    - Database schema changes required more time than estimated
    - One developer was sick for 1 week
    - Third-party API integration took longer than expected
    """

    print("\nProgress Data:")
    print(progress_data)
    print("\nAnalyzing progress...\n")

    analysis = agent.analyze_progress(progress_data)

    if analysis:
        print("\nProgress Analysis:")
        print("-" * 80)
        print(analysis)
        print("-" * 80)

def example_change_request():
    """Example: Evaluating a change request"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: MONITORING AGENT - CHANGE REQUEST EVALUATION")
    print("=" * 80)

    agent = MonitoringAgent()

    change_request = """
    Change Request #CR-2024-015

    Requested By: Sales Director
    Date: Current Sprint

    Description:
    Add social media authentication (Google, Facebook, LinkedIn) to the login system.

    Justification:
    - Market research shows 65% of users prefer social login
    - Competitors offer this feature
    - Could increase conversion rate by 20%

    Current Status:
    - Basic email/password authentication is 80% complete
    - No social auth was in original scope
    - Release is planned in 4 weeks

    Estimated Impact:
    - Development effort: 2-3 weeks
    - Testing effort: 1 week
    - No additional infrastructure costs
    """

    print("\nChange Request:")
    print(change_request)
    print("\nEvaluating change request...\n")

    evaluation = agent.evaluate_change_request(change_request)

    if evaluation:
        print("\nChange Request Evaluation:")
        print("-" * 80)
        print(evaluation)
        print("-" * 80)

def main():
    """Run all examples"""
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║         AI AGENTS FOR PMI - EXAMPLES                  ║
    ║    Demonstrating Agent Capabilities                   ║
    ╚═══════════════════════════════════════════════════════╝
    """)

    try:
        settings.validate()
    except ValueError as e:
        print(f"\n⚠️  Configuration Error: {e}")
        print("\nTo run these examples, you need to:")
        print("1. Create a .env file based on .env.example")
        print("2. Add your Anthropic API key")
        print("3. (Optional) Add Notion credentials\n")
        return

    print("\nThis script will demonstrate all agent capabilities.")
    print("Each example may take 10-30 seconds to complete.\n")

    # Run examples
    example_planning()
    input("\nPress Enter to continue to next example...")

    example_wbs()
    input("\nPress Enter to continue to next example...")

    example_execution()
    input("\nPress Enter to continue to next example...")

    example_issue_resolution()
    input("\nPress Enter to continue to next example...")

    example_monitoring()
    input("\nPress Enter to continue to next example...")

    example_change_request()

    print("\n" + "=" * 80)
    print("EXAMPLES COMPLETE")
    print("=" * 80)
    print("\nYou can now:")
    print("1. Run 'python main.py' for interactive mode")
    print("2. Import agents in your own scripts")
    print("3. Customize agents for your specific needs\n")

if __name__ == "__main__":
    main()
