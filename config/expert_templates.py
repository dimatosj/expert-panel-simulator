"""Expert templates for different domains and topics."""

from typing import Dict, List, Any


class ExpertTemplate:
    """Base template for creating domain experts."""

    def __init__(self, name: str, expertise: str, perspective: str, background: str):
        self.name = name
        self.expertise = expertise
        self.perspective = perspective
        self.background = background

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'expertise': self.expertise,
            'perspective': self.perspective,
            'background': self.background
        }


# =============================================================================
# PRODUCTIVITY & TASK MANAGEMENT EXPERTS
# =============================================================================

PRODUCTIVITY_EXPERTS = {
    'gtd_expert': ExpertTemplate(
        name="GTD Specialist",
        expertise="Task capture and context-based action",
        perspective="Focuses on clear workflows and reducing cognitive overload",
        background="Productivity coach with a focus on trusted systems and stress-free task management"
    ),
    'para_expert': ExpertTemplate(
        name="Digital Organization Expert",
        expertise="Organizing knowledge using PARA and progressive summarization",
        perspective="Focuses on turning notes into actionable creative output",
        background="Consultant specializing in digital workflows and structured personal knowledge management"
    ),
    'deep_work_expert': ExpertTemplate(
        name="Focus & Attention Expert",
        expertise="Deep work and attention management",
        perspective="Advocates for distraction-free concentration and deliberate practice",
        background="Academic and writer focused on strategies for achieving high-value output through concentration"
    ),
    'pomodoro_expert': ExpertTemplate(
        name="Time-Boxing Coach",
        expertise="Pomodoro and interval-based productivity methods",
        perspective="Emphasizes rhythm, pacing, and sustainable energy levels",
        background="Trainer who teaches time awareness, flow states, and structured work-rest cycles"
    ),
    'adhd_specialist': ExpertTemplate(
        name="Executive Function Specialist",
        expertise="ADHD and executive function challenges",
        perspective="Considers working memory, attention variability, and adaptive supports",
        background="Clinical practitioner focusing on cognitive support strategies and assistive tools"
    )
}


# =============================================================================
# TECHNOLOGY & SOFTWARE EXPERTS
# =============================================================================

TECH_EXPERTS = {
    'ux_designer': ExpertTemplate(
        name="UX Designer",
        expertise="User experience and interface design",
        perspective="Centers on usability, accessibility, and user empathy",
        background="Designer with over a decade of experience in crafting intuitive digital products"
    ),
    'software_architect': ExpertTemplate(
        name="Software Architect",
        expertise="System architecture and scalability",
        perspective="Prioritizes long-term maintainability and performance",
        background="Architect with experience in distributed systems and large-scale software design"
    ),
    'devops_engineer': ExpertTemplate(
        name="DevOps Engineer",
        expertise="Infrastructure, deployment, and automation",
        perspective="Focuses on continuous delivery, monitoring, and resilience",
        background="Engineer with extensive experience in cloud infrastructure and CI/CD pipelines"
    ),
    'security_expert': ExpertTemplate(
        name="Security Specialist",
        expertise="Cybersecurity and privacy",
        perspective="Prioritizes safety, compliance, and risk management",
        background="Researcher and consultant with expertise in threat modeling and secure application design"
    ),
    'frontend_expert': ExpertTemplate(
        name="Frontend Engineer",
        expertise="Frontend development and performance optimization",
        perspective="Emphasizes fast, responsive interfaces and code efficiency",
        background="Engineer skilled in modern web technologies and browser performance tuning"
    )
}


# =============================================================================
# BUSINESS & STRATEGY EXPERTS
# =============================================================================

BUSINESS_EXPERTS = {
    'product_manager': ExpertTemplate(
        name="Product Strategist",
        expertise="Product planning and market fit",
        perspective="Balances user needs with organizational goals",
        background="Product manager experienced in user research and lifecycle strategy"
    ),
    'startup_advisor': ExpertTemplate(
        name="Startup Mentor",
        expertise="Entrepreneurship and lean validation",
        perspective="Focuses on rapid prototyping and iterative market testing",
        background="Advisor with experience founding and guiding multiple early-stage ventures"
    ),
    'growth_expert': ExpertTemplate(
        name="Growth Specialist",
        expertise="Marketing funnels and user acquisition",
        perspective="Prioritizes scalable growth and engagement strategies",
        background="Growth professional skilled in data-driven marketing and retention campaigns"
    ),
    'finance_expert': ExpertTemplate(
        name="Finance Advisor",
        expertise="Business finance and sustainability",
        perspective="Focuses on profitability, modeling, and long-term viability",
        background="CFO-level advisor with experience in fundraising and operational finance"
    )
}


# =============================================================================
# ACADEMIC & RESEARCH EXPERTS
# =============================================================================

ACADEMIC_EXPERTS = {
    'psychology_researcher': ExpertTemplate(
        name="Cognitive Psychology Researcher",
        expertise="Human cognition and behavior",
        perspective="Applies psychological insights to design and decision-making",
        background="Academic researcher focusing on attention, learning, and memory processes"
    ),
    'education_expert': ExpertTemplate(
        name="Learning Scientist",
        expertise="Education and knowledge transfer",
        perspective="Explores methods to improve how people learn and retain knowledge",
        background="Researcher specializing in educational technology and learning methodologies"
    ),
    'data_scientist': ExpertTemplate(
        name="Data Science Researcher",
        expertise="Machine learning and statistical modeling",
        perspective="Applies quantitative methods to extract actionable insights",
        background="PhD-level researcher experienced in predictive modeling and analytics"
    )
}


# =============================================================================
# DOMAIN-SPECIFIC EXPERT SETS
# =============================================================================

EXPERT_SETS = {
    'productivity': PRODUCTIVITY_EXPERTS,
    'technology': TECH_EXPERTS,
    'business': BUSINESS_EXPERTS,
    'academic': ACADEMIC_EXPERTS,
    'software_development': {
        **{k: v for k, v in TECH_EXPERTS.items() if k in ['software_architect', 'devops_engineer', 'security_expert', 'frontend_expert']},
        'backend_expert': ExpertTemplate(
            name="Backend Engineer",
            expertise="Backend systems and database design",
            perspective="Focuses on scalable data and server architecture",
            background="Engineer skilled in distributed systems and database optimization"
        )
    },
    'product_design': {
        **{k: v for k, v in TECH_EXPERTS.items() if k in ['ux_designer']},
        **{k: v for k, v in BUSINESS_EXPERTS.items() if k in ['product_manager']},
        **{k: v for k, v in ACADEMIC_EXPERTS.items() if k in ['psychology_researcher']},
        'design_researcher': ExpertTemplate(
            name="Design Researcher",
            expertise="User research and design validation",
            perspective="Grounds design in user evidence and iterative testing",
            background="Researcher with expertise in qualitative and quantitative design studies"
        )
    }
}


def get_expert_set(domain: str) -> Dict[str, ExpertTemplate]:
    """Get a predefined set of experts for a domain."""
    return EXPERT_SETS.get(domain, {})


def create_custom_expert(name: str, expertise: str, perspective: str, background: str) -> ExpertTemplate:
    """Create a custom expert template."""
    return ExpertTemplate(name, expertise, perspective, background)


def get_available_domains() -> List[str]:
    """Get list of available expert domains."""
    return list(EXPERT_SETS.keys())


def get_all_experts() -> Dict[str, ExpertTemplate]:
    """Get all available experts across all domains."""
    all_experts = {}
    for expert_set in EXPERT_SETS.values():
        all_experts.update(expert_set)
    return all_experts


# =============================================================================
# SAMPLE CONFIGURATIONS
# =============================================================================

SAMPLE_CONFIGURATIONS = {
    'task_management_review': {
        'domain': 'productivity',
        'experts': ['gtd_expert', 'para_expert', 'adhd_specialist', 'deep_work_expert'],
        'focus': 'task management system design',
        'rounds': [
            'Initial Reactions',
            'Organizational Model',
            'User Experience',
            'Missing Concepts',
            'Implementation Priority',
            'Final Recommendations'
        ]
    },
    'app_architecture_review': {
        'domain': 'technology',
        'experts': ['software_architect', 'ux_designer', 'devops_engineer', 'security_expert'],
        'focus': 'application architecture and design',
        'rounds': [
            'Architecture Overview',
            'Scalability Concerns',
            'Security Assessment',
            'User Experience',
            'Deployment Strategy',
            'Recommendations'
        ]
    },
    'startup_idea_validation': {
        'domain': 'business',
        'experts': ['product_manager', 'startup_advisor', 'growth_expert', 'finance_expert'],
        'focus': 'startup idea and business model',
        'rounds': [
            'Market Opportunity',
            'Product-Market Fit',
            'Business Model',
            'Growth Strategy',
            'Financial Viability',
            'Go-to-Market Strategy'
        ]
    }
}
