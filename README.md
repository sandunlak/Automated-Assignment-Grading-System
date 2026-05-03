# Automated Assignment Grading System - Multi-Agent AI

A locally-hosted Multi-Agent System (MAS) that automates the assignment grading process using Small Language Models (SLMs) via Ollama and LangGraph orchestration.

## 🎯 Problem Domain

Automates the evaluation of student assignments by:
- Analyzing submitted answers
- Comparing against marking schemes/rubrics
- Generating detailed feedback
- Validating grading consistency

## 🏗️ System Architecture

### Multi-Agent Components
1. **Answer Analyzer Agent** - Parses and understands student responses
2. **Marking Agent** - Evaluates answers against rubrics and assigns scores
3. **Feedback Generator Agent** - Creates constructive feedback
4. **Validator Agent** - Ensures grading consistency and fairness

### Custom Tools
- File Reader Tool - Reads assignment submissions and rubrics
- Rubric Evaluator Tool - Matches answers against criteria
- Feedback Template Tool - Generates structured feedback
- Validation Checker Tool - Validates scoring consistency

## 🛠️ Tech Stack

- **LLM Engine**: Ollama (llama3:8b, phi3, qwen)
- **Orchestrator**: LangGraph
- **Framework**: LangChain
- **Language**: Python 3.10+

## 📋 Prerequisites

1. Install [Ollama](https://ollama.ai/)
2. Pull required models:
   ```bash
   ollama pull llama3:8b
   ```

## 🚀 Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the grading system:
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
Automated Assignment Grading System/
├── agents/                 # Agent implementations
│   ├── answer_analyzer.py
│   ├── marking_agent.py
│   ├── feedback_generator.py
│   └── validator.py
├── tools/                  # Custom Python tools
│   ├── file_reader.py
│   ├── rubric_evaluator.py
│   ├── feedback_template.py
│   └── validation_checker.py
├── state/                  # State management
│   └── graph_state.py
├── observability/          # Logging & tracing
│   └── logger.py
├── tests/                  # Evaluation scripts
│   ├── test_agents.py
│   └── evaluation.py
├── data/                   # Sample data
│   ├── sample_assignment.txt
│   └── sample_rubric.json
├── main.py                 # Entry point
└── requirements.txt
```

## 👥 Team Contributions

Each team member is responsible for:
- 1 Agent design and implementation
- 1 Custom tool development
- Testing and evaluation for their agent

## 📊 Evaluation

Run tests:
```bash
pytest tests/
```

## 🎥 Demo Video

[Link to demo video - 4-5 minutes max]

## 📄 Technical Report

[Link to technical report - 4-8 pages]
