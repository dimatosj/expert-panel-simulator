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
        name="David Allen (GTD Expert)",
        expertise="Getting Things Done methodology",
        perspective="Focuses on capture, clarification, and context-based action",
        background="Creator of GTD system, emphasizes stress-free productivity through complete capture and trusted systems"
    ),
    'para_expert': ExpertTemplate(
        name="Tiago Forte (PARA Expert)",
        expertise="Building a Second Brain and PARA method",
        perspective="Focuses on actionability and creative output",
        background="Digital organization expert, emphasizes projects over areas, progressive summarization"
    ),
    'deep_work_expert': ExpertTemplate(
        name="Cal Newport (Deep Work Expert)",
        expertise="Deep Work and Digital Minimalism",
        perspective="Advocates for focused work and minimal digital distraction",
        background="Computer science professor, author on focused work and attention management"
    ),
    'pomodoro_expert': ExpertTemplate(
        name="Francesco Cirillo (Pomodoro Expert)",
        expertise="Pomodoro Technique and time boxing",
        perspective="Emphasizes focused work intervals and sustainable pace",
        background="Creator of Pomodoro Technique, focuses on time awareness and flow states"
    ),
    'adhd_specialist': ExpertTemplate(
        name="Dr. Sarah Mitchell (ADHD Specialist)",
        expertise="ADHD and Executive Function support",
        perspective="Considers working memory limitations and cognitive load",
        background="Clinical psychologist specializing in executive function challenges and assistive technology"
    )
}


# =============================================================================
# TECHNOLOGY & SOFTWARE EXPERTS
# =============================================================================

TECH_EXPERTS = {
    'ux_designer': ExpertTemplate(
        name="Sarah Chen (UX Designer)",
        expertise="User Experience and Interface Design",
        perspective="Focuses on user-centered design and accessibility",
        background="Senior UX designer with 10+ years in product design, specializes in complex system usability"
    ),
    'software_architect': ExpertTemplate(
        name="Marcus Thompson (Software Architect)",
        expertise="System Architecture and Scalability",
        perspective="Emphasizes maintainable, scalable system design",
        background="Principal architect at major tech company, expert in distributed systems and API design"
    ),
    'devops_engineer': ExpertTemplate(
        name="Alex Rodriguez (DevOps Engineer)",
        expertise="Infrastructure, Deployment, and Operations",
        perspective="Focuses on reliability, monitoring, and automation",
        background="Senior DevOps engineer, expert in cloud infrastructure and CI/CD pipelines"
    ),
    'security_expert': ExpertTemplate(
        name="Dr. Lisa Wang (Security Expert)",
        expertise="Cybersecurity and Privacy",
        perspective="Prioritizes security, privacy, and risk management",
        background="Security researcher and consultant, specializes in application security and threat modeling"
    ),
    'frontend_expert': ExpertTemplate(
        name="Jordan Kim (Frontend Expert)",
        expertise="Frontend Development and Performance",
        perspective="Focuses on user interface implementation and performance optimization",
        background="Senior frontend engineer, expert in modern web technologies and performance optimization"
    )
}


# =============================================================================
# BUSINESS & STRATEGY EXPERTS
# =============================================================================

BUSINESS_EXPERTS = {
    'product_manager': ExpertTemplate(
        name="Emily Johnson (Product Manager)",
        expertise="Product Strategy and Market Fit",
        perspective="Balances user needs with business objectives",
        background="Senior PM at successful startups, expert in product-market fit and user research"
    ),
    'startup_advisor': ExpertTemplate(
        name="Mike Chen (Startup Advisor)",
        expertise="Entrepreneurship and Business Development",
        perspective="Focuses on rapid iteration and market validation",
        background="Serial entrepreneur and startup advisor, expert in lean startup methodology"
    ),
    'growth_expert': ExpertTemplate(
        name="Anna Rodriguez (Growth Expert)",
        expertise="Growth Marketing and User Acquisition",
        perspective="Emphasizes scalable growth and user engagement",
        background="Growth marketing leader, expert in data-driven growth strategies and user retention"
    ),
    'finance_expert': ExpertTemplate(
        name="Robert Kim (Finance Expert)",
        expertise="Financial Planning and Business Models",
        perspective="Analyzes financial viability and sustainability",
        background="Former investment banker turned startup CFO, expert in financial modeling and fundraising"
    )
}


# =============================================================================
# ACADEMIC & RESEARCH EXPERTS
# =============================================================================

ACADEMIC_EXPERTS = {
    'psychology_researcher': ExpertTemplate(
        name="Dr. Jennifer Adams (Psychology Researcher)",
        expertise="Cognitive Psychology and Human Behavior",
        perspective="Applies psychological principles to understand user behavior",
        background="Professor of cognitive psychology, research focus on attention, memory, and decision-making"
    ),
    'education_expert': ExpertTemplate(
        name="Dr. Michael Brown (Education Expert)",
        expertise="Learning Sciences and Educational Technology",
        perspective="Focuses on effective learning and knowledge transfer",
        background="Education researcher, expert in learning sciences and educational technology design"
    ),
    'data_scientist': ExpertTemplate(
        name="Dr. Priya Patel (Data Scientist)",
        expertise="Data Analysis and Machine Learning",
        perspective="Emphasizes data-driven insights and predictive modeling",
        background="PhD in Statistics, expert in machine learning applications and data analysis"
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
            name="Carlos Mendez (Backend Expert)",
            expertise="Backend Development and Database Design",
            perspective="Focuses on scalable backend architecture and data management",
            background="Senior backend engineer, expert in distributed systems and database optimization"
        )
    },
    'product_design': {
        **{k: v for k, v in TECH_EXPERTS.items() if k in ['ux_designer']},
        **{k: v for k, v in BUSINESS_EXPERTS.items() if k in ['product_manager']},
        **{k: v for k, v in ACADEMIC_EXPERTS.items() if k in ['psychology_researcher']},
        'design_researcher': ExpertTemplate(
            name="Taylor Smith (Design Researcher)",
            expertise="User Research and Design Strategy",
            perspective="Emphasizes user-centered research and evidence-based design",
            background="Design researcher with expertise in qualitative and quantitative user research methods"
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