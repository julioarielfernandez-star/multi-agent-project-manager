from agents.base_agent import BaseAgent

class MonitoringAgent(BaseAgent):
    """
    Monitoring Agent - Specializes in project monitoring and control
    Responsible for:
    - Progress tracking
    - Performance analysis
    - Variance analysis
    - Change management
    - Risk monitoring
    - Quality control
    """

    def __init__(self):
        super().__init__(
            name="Monitoring Agent",
            role="Project Monitoring & Control Specialist"
        )

    def get_system_prompt(self):
        return """You are a Project Monitoring & Control Specialist following PMI standards.

Your responsibilities include:
1. Monitoring project performance against the plan
2. Analyzing variances and trends
3. Evaluating change requests
4. Tracking risks and issues
5. Measuring quality metrics
6. Assessing schedule and cost performance
7. Recommending corrective actions
8. Validating scope completion

You apply PMI monitoring and controlling processes:
- Monitor and control project work
- Perform integrated change control
- Validate scope
- Control scope
- Control schedule
- Control costs
- Control quality
- Control resources
- Monitor communications
- Monitor risks
- Control procurements
- Monitor stakeholder engagement

Use data-driven analysis and provide actionable insights.
Calculate key performance indicators (KPIs) such as:
- Schedule Performance Index (SPI)
- Cost Performance Index (CPI)
- Schedule Variance (SV)
- Cost Variance (CV)

Recommend corrective actions when performance deviates from the plan."""

    def analyze_progress(self, planned_vs_actual):
        """Analyze project progress and identify variances"""
        prompt = f"""Analyze the following project progress data:

{planned_vs_actual}

Provide:
1. Variance analysis (schedule and scope)
2. Performance indicators (SPI, if applicable)
3. Trend analysis
4. Areas of concern
5. Recommended corrective actions"""

        return self.send_message(prompt)

    def evaluate_change_request(self, change_request):
        """Evaluate a change request and provide recommendations"""
        prompt = f"""Evaluate the following change request:

{change_request}

Assess:
1. Impact on project scope
2. Impact on schedule
3. Impact on resources
4. Impact on risks
5. Benefits vs. costs
6. Recommendation (approve/reject/modify)
7. Implementation considerations"""

        return self.send_message(prompt)

    def assess_risks(self, risk_data):
        """Assess current project risks"""
        prompt = f"""Assess the following risk information:

{risk_data}

Provide:
1. Risk prioritization matrix
2. High-priority risks requiring immediate attention
3. Risk trend analysis
4. Recommended mitigation strategies
5. Contingency planning needs"""

        return self.send_message(prompt)

    def generate_performance_report(self, project_data):
        """Generate a comprehensive performance report"""
        prompt = f"""Generate a project performance report based on:

{project_data}

Include:
1. Executive summary
2. Schedule performance
3. Scope completion status
4. Quality metrics
5. Risk status
6. Issues and blockers
7. Forecasts and projections
8. Recommendations"""

        return self.send_message(prompt)

    def identify_bottlenecks(self, workflow_data):
        """Identify bottlenecks in project workflow"""
        prompt = f"""Analyze the following workflow data to identify bottlenecks:

{workflow_data}

Provide:
1. Identified bottlenecks
2. Impact assessment
3. Root causes
4. Optimization recommendations
5. Priority actions"""

        return self.send_message(prompt)
