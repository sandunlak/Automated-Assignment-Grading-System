# Setup Guide for Automated Assignment Grading System

## Prerequisites

1. **Python 3.10 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version`

2. **Ollama (Local LLM Engine)**
   - Download from: https://ollama.ai/
   - Install and run Ollama on your machine

## Installation Steps

### Step 1: Install Ollama and Download Model

1. Install Ollama from https://ollama.ai/
2. Open a terminal and pull the required model:
   ```bash
   ollama pull llama3:8b
   ```
3. Verify Ollama is running:
   ```bash
   ollama list
   ```

### Step 2: Set Up Python Environment

1. Navigate to project directory:
   ```bash
   cd "d:\Y4S1\Automated Assignment Grading System"
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows (PowerShell):**
     ```bash
     .\venv\Scripts\Activate
     ```
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Step 3: Verify Installation

Run the test suite to ensure everything is working:
```bash
pytest tests/ -v
```

### Step 4: Run the System

Execute the main application:
```bash
python main.py
```

## Troubleshooting

### Ollama Connection Issues
- Ensure Ollama is running in the background
- Check that the model is downloaded: `ollama list`
- Verify Ollama is accessible at: http://localhost:11434

### Import Errors
- Make sure you're in the project directory
- Activate the virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

### LangGraph Errors
- Ensure Python version is 3.10 or higher
- Check all dependencies are installed

## Directory Structure

```
Automated Assignment Grading System/
├── agents/                 # Multi-agent implementations
│   ├── answer_analyzer.py     # Analyzes student answers
│   ├── marking_agent.py       # Evaluates against rubrics
│   ├── feedback_generator.py  # Creates feedback
│   └── validator.py           # Validates grading
├── tools/                  # Custom Python tools
│   ├── file_reader.py         # File I/O operations
│   ├── rubric_evaluator.py    # Rubric matching
│   ├── feedback_template.py   # Feedback formatting
│   └── validation_checker.py  # Validation logic
├── state/                  # State management
│   └── graph_state.py         # GradingState definition
├── observability/          # Logging & tracing
│   └── logger.py              # AgentLogger implementation
├── tests/                  # Test suite
│   ├── test_tools.py            # Tool tests
│   └── test_agents.py           # Agent evaluation tests
├── data/                   # Sample data
│   ├── sample_rubric.json       # Example rubric
│   └── sample_assignment.txt    # Example submission
├── logs/                   # Execution logs (auto-generated)
├── main.py                 # Entry point
├── orchestrator.py         # LangGraph workflow
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_tools.py -v
pytest tests/test_agents.py -v
```

### Run with Coverage
```bash
pip install pytest-cov
pytest tests/ --cov=. --cov-report=html
```

## Customization

### Using Different Models

Edit the model name in each agent's `__init__` method:
```python
self.llm = ChatOllama(
    model="llama3:8b",  # Change to: phi3, qwen, etc.
    temperature=0.3,
    base_url="http://localhost:11434"
)
```

### Modifying the Rubric

Edit `data/sample_rubric.json` to match your assignment requirements.

### Adding More Agents

1. Create a new agent in the `agents/` directory
2. Define its node in `orchestrator.py`
3. Add edges to define the workflow

## Team Contribution Tracking

Each team member should document their work:

### Student 1: Answer Analyzer Agent
- File: `agents/answer_analyzer.py`
- Tool: `tools/file_reader.py`
- Tests: `tests/test_tools.py` (FileReader tests)

### Student 2: Marking Agent
- File: `agents/marking_agent.py`
- Tool: `tools/rubric_evaluator.py`
- Tests: `tests/test_agents.py` (MarkingAgent tests)

### Student 3: Feedback Generator
- File: `agents/feedback_generator.py`
- Tool: `tools/feedback_template.py`
- Tests: `tests/test_agents.py` (FeedbackGenerator tests)

### Student 4: Validator Agent
- File: `agents/validator.py`
- Tool: `tools/validation_checker.py`
- Tests: `tests/test_agents.py` (ValidatorAgent tests)

## Demo Video Script (4-5 minutes)

1. **Introduction (30 seconds)**
   - Show project overview
   - Explain the problem domain

2. **Setup & Architecture (1 minute)**
   - Show Ollama running locally
   - Display system architecture
   - Explain the 4-agent workflow

3. **Live Demonstration (2 minutes)**
   - Run `python main.py`
   - Show each agent executing
   - Display logs and observability

4. **Results & Output (1 minute)**
   - Show final grading results
   - Display feedback generated
   - Show validation results

5. **Testing & Code Quality (30 seconds)**
   - Run test suite
   - Show code structure

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs in `logs/` directory
3. Verify all dependencies are installed
4. Ensure Ollama is running with the correct model
