# 🚀 Getting Started Guide

## Complete Setup & Running Instructions

---

## ⚡ Quick Start (5 Minutes)

### Prerequisites Check
```bash
# Check Python version (need 3.10+)
python --version

# Check if Ollama is installed
ollama --version
```

### Step-by-Step Setup

#### 1️⃣ Install Ollama
- **Windows**: Download from https://ollama.ai/download/windows
- **Mac**: `brew install ollama`
- **Linux**: `curl -fsSL https://ollama.ai/install.sh | sh`

After installation, Ollama should run automatically in the background.

#### 2️⃣ Download the AI Model
```bash
ollama pull llama3:8b
```
This downloads an 8-billion parameter model (~4.7 GB). Takes 5-10 minutes depending on internet speed.

Verify installation:
```bash
ollama list
# Should show: llama3:8b
```

#### 3️⃣ Set Up Python Environment

**Option A: Using Virtual Environment (Recommended)**
```bash
# Navigate to project folder
cd "d:\Y4S1\Automated Assignment Grading System"

# Create virtual environment
python -m venv venv

# Activate it
# Windows PowerShell:
.\venv\Scripts\Activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Option B: Global Installation (Quick but not recommended)**
```bash
pip install -r requirements.txt
```

#### 4️⃣ Verify Installation
```bash
# Run tests
pytest tests/ -v

# Should see: 35+ tests passing
```

#### 5️⃣ Run the System
```bash
python main.py
```

**Windows Shortcut**: Just double-click `run.bat`!

---

## 📋 Detailed Setup Guide

### For Windows Users

#### Method 1: Using Batch Files (Easiest)

1. **Setup**:
   - Double-click `setup.bat`
   - Follow the prompts
   - Installs all dependencies automatically

2. **Run**:
   - Double-click `run.bat`
   - System starts grading automatically

#### Method 2: Manual Setup (PowerShell)

```powershell
# 1. Navigate to project
cd "d:\Y4S1\Automated Assignment Grading System"

# 2. Create virtual environment
python -m venv venv

# 3. Activate
.\venv\Scripts\Activate.ps1

# Note: If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run
python main.py
```

### For Mac/Linux Users

```bash
# 1. Navigate to project
cd "/path/to/Automated Assignment Grading System"

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run
python main.py
```

---

## 🔧 Troubleshooting

### Issue: "Ollama connection refused"

**Solution:**
```bash
# Check if Ollama is running
# Windows: Check system tray for Ollama icon
# Mac/Linux: 
ps aux | grep ollama

# If not running, start it:
ollama serve

# Test connection:
curl http://localhost:11434
# Should return: "Ollama is running"
```

### Issue: "Model not found"

**Solution:**
```bash
# List installed models
ollama list

# If llama3:8b is not listed:
ollama pull llama3:8b

# Verify again
ollama list
```

### Issue: "Import Error" or "Module not found"

**Solution:**
```bash
# Make sure you're in the project directory
pwd  # Should show project path

# Make sure virtual environment is activated
# You should see (venv) in your terminal

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: "Tests failing"

**Solution:**
```bash
# Run tests with verbose output
pytest tests/ -v

# Check which tests fail
# Most failures are due to:
# 1. Missing dependencies (run pip install)
# 2. Wrong Python version (need 3.10+)
# 3. File path issues (run from project root)
```

### Issue: "Permission denied" on Windows

**Solution:**
```powershell
# Run PowerShell as Administrator
# Then:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📂 Understanding the Project Structure

```
Automated Assignment Grading System/
│
├── 📖 Documentation
│   ├── README.md              ← Start here
│   ├── SETUP.md               ← Detailed setup guide
│   ├── GETTING_STARTED.md     ← This file
│   ├── PROJECT_SUMMARY.md     ← Quick overview
│   ├── TECHNICAL_REPORT.md    ← Full report template
│   ├── ARCHITECTURE_DIAGRAMS.md ← Visual diagrams
│   └── VIVA_PREPARATION.md    ← Exam prep guide
│
├── 🤖 Source Code
│   ├── agents/                ← 4 AI agents
│   ├── tools/                 ← 4 custom tools
│   ├── state/                 ← State management
│   ├── observability/         ← Logging system
│   ├── orchestrator.py        ← Workflow engine
│   └── main.py                ← Entry point
│
├── 🧪 Testing
│   └── tests/                 ← 35+ automated tests
│
├── 📊 Data
│   └── data/                  ← Sample assignments & rubrics
│
├── 🚀 Scripts
│   ├── setup.bat              ← Windows setup script
│   └── run.bat                ← Windows run script
│
└── ⚙️ Configuration
    ├── requirements.txt       ← Python dependencies
    └── .gitignore            ← Git ignore rules
```

---

## 🎯 First Run Walkthrough

### What to Expect

When you run `python main.py`, you'll see:

```
============================================================
🚀 STARTING AUTOMATED ASSIGNMENT GRADING
============================================================
Student ID: STU2024001
Assignment ID: ML_ASSIGNMENT_01
Status: initialized
============================================================

============================================================
🔍 STEP 1: Answer Analysis
============================================================
📝 Logger initialized. Session ID: 20260425_184503
✓ Agent 'Answer Analyzer' executed in 12.34s [SUCCESS]

============================================================
📝 STEP 2: Marking
============================================================
  🔧 Tool 'evaluate_answer_against_rubric' called [SUCCESS]
✓ Agent 'Marking Agent' executed in 15.67s [SUCCESS]

============================================================
💬 STEP 3: Feedback Generation
============================================================
  🔧 Tool 'generate_feedback_template' called [SUCCESS]
✓ Agent 'Feedback Generator' executed in 14.23s [SUCCESS]

============================================================
✅ STEP 4: Validation
============================================================
  🔧 Tool 'validate_grading_consistency' called [SUCCESS]
✓ Agent 'Validator' executed in 11.89s [SUCCESS]

============================================================
🎓 GRADING RESULTS
============================================================
[Shows final grade, feedback, and validation results]
```

### After Execution

1. **Check the console output** for final grade and feedback
2. **Check `logs/` directory** for detailed JSON logs
3. **Review the output** to understand what happened

---

## 🧪 Testing the System

### Run All Tests
```bash
pytest tests/ -v
```

Expected output:
```
tests/test_tools.py::TestFileReader::test_read_assignment_file_success PASSED
tests/test_tools.py::TestRubricEvaluator::test_evaluate_answer_with_keywords PASSED
...
=================== 35 passed in 2.34s ====================
```

### Run Specific Test File
```bash
# Test tools only
pytest tests/test_tools.py -v

# Test agents only
pytest tests/test_agents.py -v
```

### Run with Coverage Report
```bash
# Install coverage plugin
pip install pytest-cov

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Open coverage report
# Windows: start htmlcov/index.html
# Mac: open htmlcov/index.html
# Linux: xdg-open htmlcov/index.html
```

---

## 🎨 Customizing the System

### Change the Assignment

1. **Edit the question and answer**:
   ```
   Open: data/sample_assignment.txt
   ```

2. **Format**:
   ```
   Question: [Your question here]

   Student Answer:
   [Student's answer here]
   ```

### Modify the Rubric

1. **Edit rubric criteria**:
   ```
   Open: data/sample_rubric.json
   ```

2. **Structure**:
   ```json
   {
     "rubric": [
       {
         "criterion_id": "C1_Name",
         "description": "What this criterion measures",
         "max_marks": 10,
         "keywords": ["keyword1", "keyword2", "keyword3"]
       }
     ]
   }
   ```

### Use a Different AI Model

1. **Download another model**:
   ```bash
   ollama pull phi3      # Microsoft's model
   ollama pull qwen      # Alibaba's model
   ollama pull mistral   # Mistral's model
   ```

2. **Update agents**:
   ```python
   # In each agent's __init__ method:
   self.llm = ChatOllama(
       model="phi3",  # Change from "llama3:8b"
       temperature=0.3,
       base_url="http://localhost:11434"
   )
   ```

---

## 📊 Monitoring & Debugging

### View Execution Logs

After running the system:
```bash
# List log files
ls logs/
# or on Windows:
dir logs

# View latest log
cat logs/grading_session_*.json
# or on Windows:
type logs\grading_session_*.json
```

### Log Structure

Each log file contains:
```json
{
  "session_id": "20260425_184503",
  "start_time": "2026-04-25T18:45:03",
  "agents_executed": [
    {
      "agent_name": "Answer Analyzer",
      "status": "success",
      "processing_time_seconds": 12.34,
      "input_summary": "...",
      "output_summary": "..."
    }
  ],
  "tools_called": [...],
  "errors": []
}
```

### Common Debugging Steps

1. **Check if Ollama is running**:
   ```bash
   curl http://localhost:11434
   ```

2. **Test a single agent**:
   ```python
   # In Python shell:
   from agents.answer_analyzer import AnswerAnalyzerAgent
   from observability.logger import AgentLogger
   
   logger = AgentLogger()
   agent = AnswerAnalyzerAgent(logger)
   # Test with sample data
   ```

3. **Enable verbose logging**:
   ```python
   # Add to main.py before workflow execution:
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

---

## 🎓 Next Steps

### For Development

1. **Understand the code**:
   - Read each agent file
   - Trace the workflow in `orchestrator.py`
   - Understand state management in `state/graph_state.py`

2. **Experiment**:
   - Modify system prompts
   - Add new tools
   - Change temperature settings
   - Test with different assignments

3. **Extend the system**:
   - Add support for multiple questions
   - Create a web interface
   - Add database storage
   - Implement batch processing

### For Submission

1. **Create GitHub repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Automated Assignment Grading System"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Record demo video** (4-5 minutes):
   - Use OBS Studio (free): https://obsproject.com/
   - Follow the script in `PROJECT_SUMMARY.md`

3. **Complete technical report**:
   - Fill in team member names in `TECHNICAL_REPORT.md`
   - Add your GitHub repository link
   - Export to PDF

4. **Prepare for viva**:
   - Study `VIVA_PREPARATION.md`
   - Practice explaining the architecture
   - Test the system one final time

---

## 📞 Getting Help

### Resources

1. **Documentation**: All `.md` files in the project
2. **Code comments**: Each file has detailed docstrings
3. **Logs**: Check `logs/` for execution details
4. **Tests**: Run tests to verify functionality

### Common Questions

**Q: How long does grading take?**
A: About 1-2 minutes per assignment (depends on your machine).

**Q: Can I run this without internet?**
A: Yes! After downloading the model once, everything runs offline.

**Q: How much RAM do I need?**
A: Minimum 8GB, recommended 16GB for smooth operation.

**Q: Can I use this for real grading?**
A: It's a prototype. For production, you'd want more testing and a teacher review step.

---

## ✅ Setup Checklist

- [ ] Ollama installed and running
- [ ] llama3:8b model downloaded
- [ ] Python 3.10+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Tests passing (`pytest tests/ -v`)
- [ ] System runs successfully (`python main.py`)
- [ ] Logs generated in `logs/` directory
- [ ] Understood the architecture
- [ ] Ready to customize and extend

---

## 🎉 You're All Set!

Your Automated Assignment Grading System is ready to use. 

**Next**: Run `python main.py` and watch the magic happen! ✨

For any issues, check the troubleshooting section or review the logs.
