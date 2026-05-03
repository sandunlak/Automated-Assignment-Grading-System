# 📚 Documentation Index

## Quick Navigation Guide

Welcome to the Automated Assignment Grading System! This index helps you find exactly what you need.

---

## 🚀 Getting Started (Start Here!)

### I'm New to This Project
📖 **Read**: [GETTING_STARTED.md](GETTING_STARTED.md)
- Complete setup instructions
- First run walkthrough
- Troubleshooting guide

### I Want to Run the System Now
⚡ **Quick Start**:
1. Install Ollama: https://ollama.ai/
2. Run: `ollama pull llama3:8b`
3. Run: `pip install -r requirements.txt`
4. Run: `python main.py`

**Windows**: Just double-click `run.bat`!

---

## 📖 Understanding the Project

### I Want a High-Level Overview
📋 **Read**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- What the system does
- Architecture at a glance
- Key features
- Assessment criteria coverage

### I Need to Understand the Architecture
🏗️ **Read**: [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md)
- 7 detailed architecture diagrams
- Data flow visualizations
- Component interaction maps
- Perfect for reports and presentations

### I Want Technical Details
📊 **Read**: [TECHNICAL_REPORT.md](TECHNICAL_REPORT.md)
- Complete technical report template
- Agent design details
- Tool implementations
- Evaluation methodology
- Individual contribution sections

---

## 👥 Team Collaboration

### We're a Team of 4
👥 **Read**: [TEAM_GUIDE.md](TEAM_GUIDE.md)
- Work distribution for 4 students
- Timeline and milestones
- Integration guidelines
- Git workflow
- Common pitfalls

### I Need to Know My Specific Tasks
🎯 **In TEAM_GUIDE.md**:
- Student 1: Answer Analyzer tasks
- Student 2: Marking Agent tasks
- Student 3: Feedback Generator tasks
- Student 4: Validator tasks

---

## 🎓 Viva/Exam Preparation

### I Have a Viva Coming Up
🎓 **Read**: [VIVA_PREPARATION.md](VIVA_PREPARATION.md)
- Key concepts to master
- Likely questions with answers
- Demonstration tips
- Individual contribution proof
- Presentation structure

### I Need to Practice
📝 **In VIVA_PREPARATION.md**:
- 8 comprehensive sections
- Common viva questions
- Red flags to avoid
- Final checklist

---

## 🛠️ Development

### I Want to Understand the Code

**Start with the workflow:**
1. 📂 [main.py](main.py) - Entry point
2. 📂 [orchestrator.py](orchestrator.py) - Workflow engine
3. 📂 [state/graph_state.py](state/graph_state.py) - Data structures

**Then explore agents:**
4. 🤖 [agents/answer_analyzer.py](agents/answer_analyzer.py)
5. 🤖 [agents/marking_agent.py](agents/marking_agent.py)
6. 🤖 [agents/feedback_generator.py](agents/feedback_generator.py)
7. 🤖 [agents/validator.py](agents/validator.py)

**Understand the tools:**
8. 🔧 [tools/file_reader.py](tools/file_reader.py)
9. 🔧 [tools/rubric_evaluator.py](tools/rubric_evaluator.py)
10. 🔧 [tools/feedback_template.py](tools/feedback_template.py)
11. 🔧 [tools/validation_checker.py](tools/validation_checker.py)

### I Want to Modify the System

**Change the assignment:**
- Edit: [data/sample_assignment.txt](data/sample_assignment.txt)

**Change the rubric:**
- Edit: [data/sample_rubric.json](data/sample_rubric.json)

**Use a different model:**
- Edit: Each agent's `__init__` method
- Change: `model="llama3:8b"` to another model

### I Want to Add Features

**Add a new agent:**
1. Create file in `agents/`
2. Add node in [orchestrator.py](orchestrator.py)
3. Update state in [state/graph_state.py](state/graph_state.py)

**Add a new tool:**
1. Create file in `tools/`
2. Import in the agent that uses it
3. Write tests in `tests/`

---

## 🧪 Testing

### I Want to Run Tests
```bash
# All tests
pytest tests/ -v

# Tools only
pytest tests/test_tools.py -v

# Agents only
pytest tests/test_agents.py -v
```

### I Want to Write Tests
📂 **See**:
- [tests/test_tools.py](tests/test_tools.py) - Tool testing examples
- [tests/test_agents.py](tests/test_agents.py) - Agent testing examples

### I Want Coverage Reports
```bash
pip install pytest-cov
pytest tests/ --cov=. --cov-report=html
```

---

## 📝 Documentation Files

### Complete File List

| File | Purpose | When to Read |
|------|---------|--------------|
| [README.md](README.md) | Project overview | First time users |
| [GETTING_STARTED.md](GETTING_STARTED.md) | Setup guide | Setting up the system |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Quick overview | Understanding the project |
| [TECHNICAL_REPORT.md](TECHNICAL_REPORT.md) | Full report | Submission & study |
| [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md) | Visual diagrams | Reports & presentations |
| [VIVA_PREPARATION.md](VIVA_PREPARATION.md) | Exam prep | Before viva |
| [TEAM_GUIDE.md](TEAM_GUIDE.md) | Team coordination | Working in a team |
| [SETUP.md](SETUP.md) | Installation details | Troubleshooting setup |
| [INDEX.md](INDEX.md) | This file | Navigation |

---

## 🎥 Demo Video

### I Need to Create a Video
📹 **In PROJECT_SUMMARY.md**: See "Demo Video Guide" section
- 4-5 minute script
- Timeline breakdown
- What to show

### Video Structure
1. Introduction (30s)
2. Architecture (1m)
3. Live Demo (2m)
4. Results (1m)
5. Testing (30s)

---

## 📋 Submission Checklist

### Code Repository
- [ ] All agents implemented
- [ ] All tools implemented
- [ ] Tests passing (35+)
- [ ] README complete
- [ ] Code documented

### Documentation
- [ ] Technical report (4-8 pages)
- [ ] Architecture diagrams
- [ ] Individual contributions
- [ ] GitHub repository

### Demo
- [ ] Video recorded (4-5 min)
- [ ] Shows full workflow
- [ ] Clear narration

### Individual Proof
- [ ] Your agent code
- [ ] Your tool code
- [ ] Your tests
- [ ] Challenges documented

---

## 🔧 Quick Reference

### Commands

```bash
# Setup
ollama pull llama3:8b
pip install -r requirements.txt

# Run
python main.py

# Test
pytest tests/ -v

# Git
git init
git add .
git commit -m "Initial commit"
```

### File Locations

```
Agents:     agents/*.py
Tools:      tools/*.py
State:      state/graph_state.py
Tests:      tests/*.py
Logs:       logs/*.json
Data:       data/*
```

### Dependencies

**Core:**
- langgraph - Workflow orchestration
- langchain - LLM framework
- ollama - Local LLM engine
- pydantic - Data validation

**Testing:**
- pytest - Test framework
- rich - Console output

---

## 🆘 Help & Troubleshooting

### Common Issues

**Ollama not working:**
📖 See: [GETTING_STARTED.md](GETTING_STARTED.md) → Troubleshooting

**Tests failing:**
📖 See: [GETTING_STARTED.md](GETTING_STARTED.md) → Testing

**Integration problems:**
📖 See: [TEAM_GUIDE.md](TEAM_GUIDE.md) → Integration Checklist

### Where to Get Help

1. **Check logs**: `logs/` directory
2. **Run tests**: Identify what's broken
3. **Read docs**: Search relevant .md file
4. **Ask team**: Use TEAM_GUIDE.md guidelines

---

## 📊 Assessment Criteria Mapping

### Where to Find Evidence for Each Criteria

| Criteria | Weight | Where to Find |
|----------|--------|---------------|
| Problem Definition | 10% | [TECHNICAL_REPORT.md](TECHNICAL_REPORT.md) Section 1 |
| Multi-Agent Architecture | 15% | [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md), agents/ |
| Tool Development | 10% | tools/, [TECHNICAL_REPORT.md](TECHNICAL_REPORT.md) Section 4 |
| State Management | 10% | state/graph_state.py, [TECHNICAL_REPORT.md](TECHNICAL_REPORT.md) Section 5 |
| System Demonstration | 5% | Demo video |
| Testing & Evaluation | 10% | tests/, [TECHNICAL_REPORT.md](TECHNICAL_REPORT.md) Section 6 |
| Individual Agent Design | 20% | agents/, [TECHNICAL_REPORT.md](TECHNICAL_REPORT.md) Section 8 |
| Individual Custom Tool | 20% | tools/, [TECHNICAL_REPORT.md](TECHNICAL_REPORT.md) Section 8 |

---

## 🎯 Quick Paths by Role

### If You're Student 1 (Answer Analyzer)

**Must Read:**
1. [TEAM_GUIDE.md](TEAM_GUIDE.md) → Student 1 section
2. agents/answer_analyzer.py
3. tools/file_reader.py
4. [VIVA_PREPARATION.md](VIVA_PREPARATION.md)

**Must Do:**
- Implement Answer Analyzer agent
- Implement File Reader tool
- Write tests
- Document your work

### If You're Student 2 (Marking Agent)

**Must Read:**
1. [TEAM_GUIDE.md](TEAM_GUIDE.md) → Student 2 section
2. agents/marking_agent.py
3. tools/rubric_evaluator.py
4. [VIVA_PREPARATION.md](VIVA_PREPARATION.md)

**Must Do:**
- Implement Marking Agent
- Implement Rubric Evaluator tool
- Write tests
- Document your work

### If You're Student 3 (Feedback Generator)

**Must Read:**
1. [TEAM_GUIDE.md](TEAM_GUIDE.md) → Student 3 section
2. agents/feedback_generator.py
3. tools/feedback_template.py
4. [VIVA_PREPARATION.md](VIVA_PREPARATION.md)

**Must Do:**
- Implement Feedback Generator
- Implement Feedback Template tool
- Write tests
- Document your work

### If You're Student 4 (Validator)

**Must Read:**
1. [TEAM_GUIDE.md](TEAM_GUIDE.md) → Student 4 section
2. agents/validator.py
3. tools/validation_checker.py
4. [VIVA_PREPARATION.md](VIVA_PREPARATION.md)

**Must Do:**
- Implement Validator agent
- Implement Validation Checker tool
- Write tests
- Document your work

---

## 🚀 Next Steps

### For First-Time Users

1. ✅ Read [GETTING_STARTED.md](GETTING_STARTED.md)
2. ✅ Install dependencies
3. ✅ Run `python main.py`
4. ✅ Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
5. ✅ Explore the code

### For Team Members

1. ✅ Read [TEAM_GUIDE.md](TEAM_GUIDE.md)
2. ✅ Understand your responsibilities
3. ✅ Set up development environment
4. ✅ Start coding your components
5. ✅ Test frequently

### For Viva Preparation

1. ✅ Read [VIVA_PREPARATION.md](VIVA_PREPARATION.md)
2. ✅ Understand your code completely
3. ✅ Practice explaining architecture
4. ✅ Run demo successfully
5. ✅ Prepare for questions

---

## 📞 Quick Links

**External Resources:**
- Ollama: https://ollama.ai/
- LangGraph: https://langchain-ai.github.io/langgraph/
- LangChain: https://python.langchain.com/
- Python: https://www.python.org/

**Project Files:**
- Main entry: [main.py](main.py)
- Orchestrator: [orchestrator.py](orchestrator.py)
- Requirements: [requirements.txt](requirements.txt)
- Git ignore: [.gitignore](.gitignore)

---

## 💡 Tips for Success

1. **Start early**: Don't wait until the deadline
2. **Test often**: Run tests after every change
3. **Document as you go**: Don't leave it for last
4. **Communicate**: Keep team members updated
5. **Understand, don't copy**: You'll be questioned on it
6. **Practice the demo**: Multiple times before submission
7. **Back up everything**: Use Git regularly

---

## 🎉 You're Ready!

Use this index to navigate the documentation efficiently. 

**Remember**: All the information you need is in these documents. Read them thoroughly, understand the code, and practice your presentation.

**Good luck with your project! 🍀**

---

*Last updated: April 25, 2026*
