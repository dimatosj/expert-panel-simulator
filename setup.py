"""Setup script for Expert Panel Simulator."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="expert-panel-simulator",
    version="1.0.0",
    author="Expert Panel Simulator Contributors",
    description="Multi-Agent Expert Review System for any topic or document",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "expert-panel=expert_panel_simulator:main",
        ],
    },
    keywords="ai, expert-panel, multi-agent, review, simulation, autogen, openai, anthropic",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/expert-panel-simulator/issues",
        "Source": "https://github.com/yourusername/expert-panel-simulator",
    },
)