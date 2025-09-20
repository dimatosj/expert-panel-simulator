"""Configuration modules for Expert Panel Simulator."""

from .expert_templates import (
    get_expert_set,
    create_custom_expert,
    get_available_domains,
    get_all_experts,
    SAMPLE_CONFIGURATIONS,
    ExpertTemplate
)

__all__ = [
    'get_expert_set',
    'create_custom_expert',
    'get_available_domains',
    'get_all_experts',
    'SAMPLE_CONFIGURATIONS',
    'ExpertTemplate'
]