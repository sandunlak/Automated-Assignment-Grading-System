# Project Summary: Automated Assignment Grading System

## 📋 Quick Overview

**Project Name**: Automated Assignment Grading System  
**Course**: SE4010 – CTSE Assignment 2 – Machine Learning  
**Team Size**: 4 Students  
**Tech Stack**: LangGraph + Ollama + LangChain + Python  

---

## 🎯 What It Does

A multi-agent AI system that automatically grades student assignments by:
1. **Analyzing** student answers for key concepts and completeness
2. **Marking** against rubrics with detailed justifications
3. **Generating** constructive, actionable feedback
4. **Validating** grading consistency and fairness

**Key Feature**: Runs 100% locally with zero cloud costs using Ollama SLMs!

---

## 🏗️ Architecture at a Glance

### 4 Specialized Agents (Sequential Pipeline)

```
Student Submission
       ↓
┌──────────────────────────────┐
│  1. ANSWER ANALYZER AGENT    │
│  - Identifies key concepts   │
│  - Scores completeness       │
│  - Assesses relevance        │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│  2. MARKING AGENT            │
│  - Applies rubric criteria   │
│  - Assigns marks             │
│  - Provides justifications   │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│  3. FEEDBACK GENERATOR AGENT │
│  - Identifies strengths      │
│  - Notes areas to improve    │
│  - Creates recommendations   │
└──────────────┬───────────────┘
               ↓
┌──────────────────────────────┐
│  4. VALIDATOR AGENT          │
│  - Checks consistency        │
│  - Detects anomalies         │
│  - Validates fairness        │
└──────────────┬───────────────┘
               ↓
    Final Grade + Feedback
```

---

## 🛠️ Custom Tools (4 Tools)

| Tool | Purpose | Used By |
|------|---------|---------|
| **File Reader** | Read/write assignment files | Answer Analyzer |
| **Rubric Evaluator** | Keyword-based scoring | Marking Agent |
| **Feedback Template** | Format feedback reports | Feedback Generator |
| **Validation Checker** | Consistency checks | Validator |

---

## 📁 Project Structure

```
Automated Assignment Grading System/
│
├── 🤖 agents/                     # Multi-Agent Implementation
│   ├── answer_analyzer.py         # Agent 1: Analyzes answers
│   ├── marking_agent.py           # Agent 2: Evaluates & marks
│   ├── feedback_generator.py      # Agent 3: Creates feedback
│   └── validator.py               # Agent 4: Validates grading
│
├── 🔧 tools/                      # Custom Python Tools
│   ├── file_reader.py             # File I/O operations
│   ├── rubric_evaluator.py        # Rubric matching logic
│   ├── feedback_template.py       # Feedback formatting
│   └── validation_checker.py      # Validation algorithms
│
├── 📊 state/                      # State Management
│   └── graph_state.py             # Global state definitions
│
├── 📝 observability/              # Logging & Tracing
│   └── logger.py                  # AgentLogger implementation
│
├── 🧪 tests/                      # Test Suite
│   ├── test_tools.py              # Tool unit tests (15+)
│   └── test_agents.py             # Agent property tests (20+)
│
├── 📂 data/                       # Sample Data
│   ├── sample_rubric.json         # Example rubric (5 criteria)
│   └── sample_assignment.txt      # Example student answer
│
├── orchestrator.py                # LangGraph workflow
├── main.py                        # Entry point
├── requirements.txt               # Dependencies
├── README.md                      # Documentation
├── SETUP.md                       # Installation guide
└── TECHNICAL_REPORT.md            # Full report template
```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Ollama
```bash
# Download from https://ollama.ai/
ollama pull llama3:8b
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the System
```bash
python main.py
```

**Windows Users**: Just double-click `run.bat`!

---

## 💡 Key Features

### ✅ Multi-Agent Orchestration
- 4 distinct agents with specialized roles
- LangGraph-based workflow management
- Clear delegation and interaction strategy

### ✅ Tool Usage
- Custom Python tools with type hinting
- Real-world file I/O operations
- Rubric evaluation algorithms
- Validation logic

### ✅ State Management
- TypedDict-based global state
- Pydantic models for data validation
- Sequential state population
- Context preservation across agents

### ✅ Observability
- Comprehensive logging system
- Agent execution tracking
- Tool call monitoring
- JSON-formatted session logs

### ✅ Testing & Evaluation
- 35+ automated tests
- Property-based testing
- Tool unit tests
- Agent evaluation scripts

---

## 📊 Assessment Criteria Coverage

| Criteria | Weight | Implementation |
|----------|--------|----------------|
| **Problem Definition & Architecture** | 10% | ✅ Clear problem domain, professional diagrams |
| **Multi-Agent Architecture** | 15% | ✅ 4 agents, LangGraph orchestration |
| **Tool Development** | 10% | ✅ 4 custom tools, fully integrated |
| **State Management & Observability** | 10% | ✅ Global state, comprehensive logging |
| **System Demonstration** | 5% | ✅ Video script provided |
| **Testing & Evaluation** | 10% | ✅ 35+ tests, property-based |
| **Individual Agent Design** | 20% | ✅ Each student builds 1 agent |
| **Individual Custom Tool** | 20% | ✅ Each student builds 1 tool |

---

## 👥 Team Contribution Guide

### Student 1: Answer Analyzer
**Deliverables**:
- ✅ `agents/answer_analyzer.py`
- ✅ `tools/file_reader.py`
- ✅ Tests in `tests/test_tools.py`

**Proof of Contribution**:
- System prompt design
- JSON parsing logic
- File I/O error handling

---

### Student 2: Marking Agent
**Deliverables**:
- ✅ `agents/marking_agent.py`
- ✅ `tools/rubric_evaluator.py`
- ✅ Tests in `tests/test_agents.py`

**Proof of Contribution**:
- Rubric evaluation algorithm
- Tool + LLM blending logic
- Grade boundary calculations

---

### Student 3: Feedback Generator
**Deliverables**:
- ✅ `agents/feedback_generator.py`
- ✅ `tools/feedback_template.py`
- ✅ Tests in `tests/test_agents.py`

**Proof of Contribution**:
- Feedback generation prompt
- Template formatting
- Constructive tone enforcement

---

### Student 4: Validator
**Deliverables**:
- ✅ `agents/validator.py`
- ✅ `tools/validation_checker.py`
- ✅ Tests in `tests/test_agents.py`

**Proof of Contribution**:
- Validation algorithms
- Anomaly detection logic
- Baseline comparison

---

## 🎥 Demo Video Guide (4-5 Minutes)

### Script Timeline:

**0:00-0:30** - Introduction
- Show project title and problem statement
- Explain why automated grading matters

**0:30-1:30** - Architecture & Setup
- Show Ollama running locally
- Display the 4-agent architecture diagram
- Explain LangGraph orchestration

**1:30-3:30** - Live Demo
- Run `python main.py`
- Show console output as each agent executes
- Display logs being generated
- Show final grading results

**3:30-4:30** - Results & Testing
- Show formatted feedback report
- Display validation results
- Run test suite: `pytest tests/ -v`

**4:30-5:00** - Conclusion
- Summarize key achievements
- Mention zero cloud costs
- Show GitHub repository

---

## 📝 Technical Report Sections

The `TECHNICAL_REPORT.md` file includes:
1. ✅ Problem Domain
2. ✅ System Architecture
3. ✅ Agent Design (prompts, constraints, reasoning)
4. ✅ Custom Tools (APIs, examples)
5. ✅ State Management
6. ✅ Evaluation Methodology
7. ✅ Individual Contributions
8. ✅ GitHub Repository Link

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pip install pytest-cov
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_tools.py -v
pytest tests/test_agents.py -v
```

---

## 🔧 Customization Options

### Change the LLM Model
Edit any agent's `__init__` method:
```python
self.llm = ChatOllama(
    model="phi3",  # or "qwen", "mistral", etc.
    temperature=0.3,
    base_url="http://localhost:11434"
)
```

### Modify the Rubric
Edit `data/sample_rubric.json` with your criteria.

### Add Your Own Assignment
Create a new file in `data/` following the format:
```
Question: [Your question]

Student Answer:
[Student's response]
```

---

## 🎓 Viva Preparation

### Key Concepts to Understand:
1. **Multi-Agent Systems**: Why multiple agents vs. single agent?
2. **LangGraph**: How does state graph orchestration work?
3. **Ollama/SLMs**: Why local models? What are the trade-offs?
4. **Tool Usage**: Why can't agents just use LLM knowledge?
5. **State Management**: How is context passed between agents?
6. **Observability**: Why is logging important in AI systems?

### Likely Questions:
- How do you ensure grading consistency?
- What happens if an agent fails?
- How do you prevent hallucination?
- Why did you choose sequential architecture?
- How would you scale this to 1000s of submissions?
- What are the limitations of using SLMs?

---

## 📈 Future Enhancements

- [ ] Support for multiple questions per assignment
- [ ] Integration with Moodle/Canvas LMS
- [ ] Historical performance tracking
- [ ] Adaptive rubric adjustment
- [ ] Plagiarism detection agent
- [ ] Multi-language support

---

## 📞 Support

- **Setup Issues**: See `SETUP.md`
- **Technical Details**: See `TECHNICAL_REPORT.md`
- **Code Documentation**: Check docstrings in each file
- **Logs**: Check `logs/` directory after running

---

## ✅ Deliverables Checklist

- [x] Source Code Repository
- [x] MAS Implementation (LangGraph)
- [x] 4 Agents Implemented
- [x] 4 Custom Python Tools
- [x] Testing/Evaluation Scripts
- [x] Demo Video Script
- [x] Technical Report Template
- [x] Individual Contribution Proof
- [x] README Documentation
- [x] Setup Instructions

---

**Built with ❤️ using LangGraph, Ollama, and Python**
