# Technical Report: Automated Assignment Grading System

## 1. Problem Domain

### 1.1 Overview
The Automated Assignment Grading System addresses the challenge of efficiently and consistently evaluating student assignments in educational institutions. Manual grading is time-consuming, prone to inconsistencies, and provides delayed feedback to students.

### 1.2 Problem Statement
Teachers spend significant time grading assignments, and maintaining consistency across multiple submissions is challenging. Students often receive delayed feedback, reducing its effectiveness for learning.

### 1.3 Solution Approach
We developed a Multi-Agent System (MAS) that automates the grading process using locally-hosted Small Language Models (SLMs) via Ollama. The system analyzes student answers, evaluates them against rubrics, generates constructive feedback, and validates grading consistency—all without cloud dependencies or API costs.

---

## 2. System Architecture

### 2.1 Multi-Agent Architecture

The system employs a **sequential pipeline architecture** with four specialized agents:

```
┌─────────────────┐
│  Answer         │
│  Analyzer       │
│  Agent          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Marking        │
│  Agent          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Feedback       │
│  Generator      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Validator      │
│  Agent          │
└─────────────────┘
```

### 2.2 Agent Roles and Responsibilities

#### Agent 1: Answer Analyzer
- **Role**: Parse and understand student responses
- **Responsibilities**:
  - Identify key concepts in the answer
  - Assess completeness, relevance, and clarity
  - Provide structured analysis for downstream agents
- **Output**: AnalysisResult with scores and concept identification

#### Agent 2: Marking Agent
- **Role**: Evaluate answers against rubrics
- **Responsibilities**:
  - Apply rubric criteria systematically
  - Assign marks with justifications
  - Calculate total scores and percentages
- **Output**: MarkingResult with criterion-wise marks

#### Agent 3: Feedback Generator
- **Role**: Create constructive feedback
- **Responsibilities**:
  - Identify strengths and weaknesses
  - Generate actionable recommendations
  - Format professional feedback reports
- **Output**: FeedbackResult with detailed comments

#### Agent 4: Validator
- **Role**: Ensure grading quality
- **Responsibilities**:
  - Detect anomalies and inconsistencies
  - Validate marks against constraints
  - Recommend adjustments if needed
- **Output**: ValidationResult with consistency metrics

### 2.3 Workflow Diagram

```
[Student Submission] → [File Reader Tool]
                            ↓
                    [Answer Analyzer Agent]
                            ↓
                    [Rubric Evaluator Tool]
                            ↓
                    [Marking Agent]
                            ↓
                    [Grade Boundary Tool]
                            ↓
                    [Feedback Generator Agent]
                            ↓
                    [Feedback Template Tool]
                            ↓
                    [Validator Agent]
                            ↓
                    [Validation Checker Tool]
                            ↓
                    [Final Grade & Feedback]
```

---

## 3. Agent Design

### 3.1 System Prompts and Constraints

#### Answer Analyzer Agent
**System Prompt Excerpt**:
```
You are an expert Answer Analyzer for an automated assignment grading system.

ANALYSIS CRITERIA:
1. Key Concepts: Identify main concepts, theories, or principles
2. Completeness: How thoroughly does the answer address the question? (0.0-1.0)
3. Relevance: How relevant is the content? (0.0-1.0)
4. Clarity: How clear and well-structured? (0.0-1.0)

CONSTRAINTS:
- Be objective and analytical
- Do NOT assign marks
- Provide specific examples from the answer
```

**Reasoning Logic**:
- Uses few-shot prompting principles
- Enforces JSON output for structured data
- Temperature set to 0.3 for balanced creativity/consistency

#### Marking Agent
**System Prompt Excerpt**:
```
You are an expert Marking Agent for an automated assignment grading system.

MARKING PRINCIPLES:
1. Fairness: Apply rubric consistently
2. Justification: Clear reasoning for each mark
3. Proportionality: Marks reflect quality
4. Constructive: Focus on demonstrated knowledge
```

**Reasoning Logic**:
- Blends tool evaluation (40%) with LLM evaluation (60%)
- Lower temperature (0.2) for consistent marking
- Validates against rubric constraints

#### Feedback Generator Agent
**System Prompt Excerpt**:
```
You are an expert Feedback Generator for an automated assignment grading system.

FEEDBACK PRINCIPLES:
1. Specific: Reference actual content
2. Constructive: Focus on improvement
3. Balanced: Acknowledge strengths and weaknesses
4. Actionable: Provide clear steps
```

**Reasoning Logic**:
- Slightly higher temperature (0.4) for natural language
- Enforces constructive tone
- Structures feedback for readability

#### Validator Agent
**System Prompt Excerpt**:
```
You are an expert Validator Agent for an automated assignment grading system.

VALIDATION CHECKS:
1. Range Validation: Marks within valid ranges
2. Sum Validation: Total equals sum of criteria
3. Proportionality: Marks match quality
4. Anomaly Detection: Identify outliers
```

**Reasoning Logic**:
- Very low temperature (0.1) for strict validation
- Combines rule-based and LLM-based validation
- Flags issues for manual review

### 3.2 Interaction Strategy

The agents interact through a **shared state pattern** using LangGraph:
- **State Passing**: Global `GradingState` object passed between agents
- **Sequential Execution**: Each agent enriches the state
- **No Direct Communication**: Agents interact only through state
- **Context Preservation**: All previous agent outputs remain accessible

---

## 4. Custom Tools

### 4.1 File Reader Tool
**Purpose**: Read assignment submissions and rubrics from local files

**Functions**:
- `read_assignment_file(file_path)`: Read student submission
- `read_rubric_file(file_path)`: Read marking rubric
- `write_feedback_file(file_path, content)`: Save feedback

**Example Usage**:
```python
content = read_assignment_file.invoke({
    "file_path": "data/sample_assignment.txt"
})
```

### 4.2 Rubric Evaluator Tool
**Purpose**: Evaluate answers against rubric criteria using keyword matching

**Functions**:
- `evaluate_answer_against_rubric(answer_text, rubric_criteria)`: Score answer
- `calculate_grade_boundary(percentage)`: Convert to letter grade

**Example Usage**:
```python
result = evaluate_answer_against_rubric.invoke({
    "answer_text": "Machine learning is...",
    "rubric_criteria": rubric_dict
})
# Returns: {'criterion_scores': {...}, 'total_score': 35.0, 'percentage': 70.0}
```

### 4.3 Feedback Template Tool
**Purpose**: Generate structured feedback documents

**Functions**:
- `generate_feedback_template(...)`: Create formatted feedback report
- `create_detailed_comment(...)`: Generate criterion-specific comments

**Example Usage**:
```python
feedback = generate_feedback_template.invoke({
    "student_name": "STU001",
    "marks_awarded": 35.0,
    "max_marks": 50.0,
    "strengths": ["Good understanding"],
    "weaknesses": ["Needs more depth"],
    "recommendations": ["Review chapter 5"]
})
```

### 4.4 Validation Checker Tool
**Purpose**: Validate grading consistency and detect anomalies

**Functions**:
- `validate_grading_consistency(...)`: Check marking validity
- `compare_with_baseline(...)`: Detect score outliers

**Example Usage**:
```python
validation = validate_grading_consistency.invoke({
    "marks_awarded": 35.0,
    "max_marks": 50.0,
    "analysis_scores": {"C1": 8.0, "C2": 7.0},
    "rubric_weights": {"C1": 10.0, "C2": 10.0}
})
```

---

## 5. State Management

### 5.1 Global State Structure

The `GradingState` TypedDict maintains all context:

```python
class GradingState(TypedDict):
    # Input data
    assignment_question: str
    student_answer_raw: str
    rubric: List[RubricCriterion]
    
    # Agent outputs (populated sequentially)
    analysis_result: Optional[AnalysisResult]
    marking_result: Optional[MarkingResult]
    feedback_result: Optional[FeedbackResult]
    validation_result: Optional[ValidationResult]
    
    # Metadata
    student_id: str
    assignment_id: str
    processing_status: str
    error_messages: List[str]
    
    # Final output
    final_grade: Optional[float]
    ready_for_review: bool
```

### 5.2 Context Passing Strategy

1. **Initialization**: State created with input data
2. **Answer Analyzer**: Populates `analysis_result`
3. **Marking Agent**: Reads analysis, populates `marking_result`
4. **Feedback Generator**: Reads analysis + marking, populates `feedback_result`
5. **Validator**: Reads all previous results, populates `validation_result`

**Key Features**:
- Immutability: Each agent returns new state dict
- Type Safety: Pydantic models for structured data
- Error Tracking: `error_messages` list accumulates issues
- Status Tracking: `processing_status` shows workflow progress

---

## 6. Evaluation Methodology

### 6.1 Testing Approach

We implemented comprehensive testing at multiple levels:

#### Unit Tests (Tools)
- **File Reader**: Test file I/O operations
- **Rubric Evaluator**: Test keyword matching and scoring
- **Feedback Template**: Test formatting and structure
- **Validation Checker**: Test consistency checks

#### Property-Based Tests (Agents)
- **Answer Analyzer**: Verify score ranges and concept identification
- **Marking Agent**: Test mark calculations and justifications
- **Feedback Generator**: Validate feedback structure and tone
- **Validator**: Test anomaly detection and recommendations

#### Integration Tests
- Test complete workflow execution
- Verify state transitions
- Check final output correctness

### 6.2 Test Scripts

**Location**: `tests/` directory
- `test_tools.py`: 15+ unit tests for tools
- `test_agents.py`: 20+ property-based tests for agents

**Running Tests**:
```bash
pytest tests/ -v
```

### 6.3 Performance Analysis

**Metrics Tracked**:
- Agent execution time
- Tool call duration
- State transition count
- Error rate

**Observability**:
- All operations logged to `logs/` directory
- JSON-formatted session logs
- Timestamped entries for each agent/tool execution

### 6.4 Reliability Features

1. **Error Handling**: Each agent catches and logs exceptions
2. **Fallback Values**: Default outputs if parsing fails
3. **Validation**: Validator catches grading errors
4. **Logging**: Complete audit trail for debugging

---

## 7. GitHub Repository

**Repository URL**: [Insert GitHub Link Here]

**Structure**:
```
├── agents/                 # Agent implementations
├── tools/                  # Custom Python tools
├── state/                  # State management
├── observability/          # Logging & tracing
├── tests/                  # Test suite
├── data/                   # Sample data
├── main.py                 # Entry point
├── orchestrator.py         # LangGraph workflow
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

---

## 8. Individual Contributions

### Student 1: [Name]

**Agent Developed**: Answer Analyzer Agent
- **File**: `agents/answer_analyzer.py`
- **Description**: Implements answer parsing and concept identification
- **Challenges Faced**:
  - Parsing JSON from LLM responses reliably
  - Balancing analysis depth with SLM limitations
  - Ensuring consistent output format

**Tool Implemented**: File Reader Tool
- **File**: `tools/file_reader.py`
- **Description**: Handles file I/O for assignments and rubrics
- **Features**: Error handling, encoding support, path validation

---

### Student 2: [Name]

**Agent Developed**: Marking Agent
- **File**: `agents/marking_agent.py`
- **Description**: Evaluates answers against rubrics and assigns marks
- **Challenges Faced**:
  - Blending tool and LLM evaluations effectively
  - Ensuring marking consistency across criteria
  - Providing meaningful justifications

**Tool Implemented**: Rubric Evaluator Tool
- **File**: `tools/rubric_evaluator.py`
- **Description**: Keyword-based rubric matching and scoring
- **Features**: Weighted scoring, content depth analysis

---

### Student 3: [Name]

**Agent Developed**: Feedback Generator Agent
- **File**: `agents/feedback_generator.py`
- **Description**: Creates constructive, actionable feedback
- **Challenges Faced**:
  - Maintaining constructive tone
  - Generating specific (not generic) feedback
  - Balancing strengths and weaknesses

**Tool Implemented**: Feedback Template Tool
- **File**: `tools/feedback_template.py`
- **Description**: Formats structured feedback reports
- **Features**: Professional formatting, criterion comments

---

### Student 4: [Name]

**Agent Developed**: Validator Agent
- **File**: `agents/validator.py`
- **Description**: Validates grading consistency and detects anomalies
- **Challenges Faced**:
  - Defining meaningful validation rules
  - Balancing strictness with flexibility
  - Providing actionable recommendations

**Tool Implemented**: Validation Checker Tool
- **File**: `tools/validation_checker.py`
- **Description**: Consistency checks and outlier detection
- **Features**: Multi-level validation, baseline comparison

---

## 9. Conclusion

The Automated Assignment Grading System successfully demonstrates a production-ready Multi-Agent System for educational assessment. Key achievements include:

- **Zero Cloud Costs**: Runs entirely locally with Ollama
- **Consistent Grading**: Validator ensures fairness
- **Actionable Feedback**: Students receive detailed guidance
- **Full Observability**: Complete logging and tracing
- **Robust Testing**: Comprehensive test suite ensures reliability

**Future Enhancements**:
- Support for multiple question types
- Integration with Learning Management Systems
- Historical performance tracking
- Adaptive rubric adjustment based on cohort performance

---

## 10. References

1. LangGraph Documentation: https://langchain-ai.github.io/langgraph/
2. Ollama: https://ollama.ai/
3. LangChain: https://python.langchain.com/
4. Pydantic: https://docs.pydantic.dev/
