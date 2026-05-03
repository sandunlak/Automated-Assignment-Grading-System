# Architecture Diagrams

## 1. High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                           │
│              (Terminal / CLI Interface)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  ORCHESTRATION LAYER                        │
│                  (LangGraph Workflow)                       │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           GradingWorkflow Class                      │  │
│  │  - Manages agent execution sequence                  │  │
│  │  - Handles state transitions                         │  │
│  │  - Coordinates data flow                             │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    AGENT LAYER                              │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Answer     │→ │   Marking    │→ │  Feedback    │     │
│  │  Analyzer    │  │    Agent     │  │  Generator   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                             │               │
│                                             ▼               │
│                                      ┌──────────────┐      │
│                                      │  Validator   │      │
│                                      │    Agent     │      │
│                                      └──────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     TOOL LAYER                              │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    File      │  │   Rubric     │  │  Feedback    │     │
│  │   Reader     │  │  Evaluator   │  │  Template    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────┐                                          │
│  │  Validation  │                                          │
│  │   Checker    │                                          │
│  └──────────────┘                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  INFRASTRUCTURE LAYER                       │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Ollama     │  │   LangChain  │  │   Pydantic   │     │
│  │  (LLM Engine)│  │  (Framework) │  │ (Validation) │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │     Rich     │  │    Pytest    │                        │
│  │  (Display)   │  │  (Testing)   │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Detailed Agent Workflow

```
                    INITIAL STATE
                         │
    ┌────────────────────┴────────────────────┐
    │  - assignment_question                  │
    │  - student_answer_raw                   │
    │  - rubric (criteria list)               │
    │  - student_id, assignment_id            │
    └────────────────────┬────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │  ANSWER ANALYZER    │
              │                     │
              │  Uses: File Reader  │
              │                     │
              │  Outputs:           │
              │  - key_concepts     │
              │  - completeness     │
              │  - relevance        │
              │  - clarity          │
              └────────┬────────────┘
                       │
                       ▼
              ┌─────────────────────┐
              │   MARKING AGENT     │
              │                     │
              │  Uses: Rubric       │
              │        Evaluator    │
              │                     │
              │  Outputs:           │
              │  - criterion_marks  │
              │  - total_marks      │
              │  - justifications   │
              └────────┬────────────┘
                       │
                       ▼
              ┌─────────────────────┐
              │ FEEDBACK GENERATOR  │
              │                     │
              │  Uses: Feedback     │
              │        Template     │
              │                     │
              │  Outputs:           │
              │  - strengths        │
              │  - weaknesses       │
              │  - recommendations  │
              └────────┬────────────┘
                       │
                       ▼
              ┌─────────────────────┐
              │   VALIDATOR AGENT   │
              │                     │
              │  Uses: Validation   │
              │        Checker      │
              │                     │
              │  Outputs:           │
              │  - consistency      │
              │  - anomalies        │
              │  - final_grade      │
              └────────┬────────────┘
                       │
                       ▼
                    FINAL STATE
    ┌────────────────────┴────────────────────┐
    │  - final_grade                          │
    │  - feedback_result                      │
    │  - validation_result                    │
    │  - ready_for_review (boolean)           │
    └─────────────────────────────────────────┘
```

---

## 3. State Management Flow

```
┌─────────────────────────────────────────────────────────┐
│                    GradingState                         │
│                                                         │
│  INPUT DATA (Initialized at start)                     │
│  ├─ assignment_question: str                           │
│  ├─ student_answer_raw: str                            │
│  ├─ rubric: List[RubricCriterion]                      │
│  ├─ student_id: str                                    │
│  └─ assignment_id: str                                 │
│                                                         │
│  AGENT OUTPUTS (Populated sequentially)                │
│  ├─ analysis_result: Optional[AnalysisResult]  ← Agent 1│
│  ├─ marking_result: Optional[MarkingResult]    ← Agent 2│
│  ├─ feedback_result: Optional[FeedbackResult]  ← Agent 3│
│  └─ validation_result: Optional[ValidationResult] ←Ag4 │
│                                                         │
│  METADATA (Updated throughout)                         │
│  ├─ processing_status: str                             │
│  ├─ error_messages: List[str]                          │
│  └─ ready_for_review: bool                             │
│                                                         │
│  FINAL OUTPUT (Set at end)                             │
│  ├─ final_grade: Optional[float]                       │
│  └─ final_feedback: Optional[str]                      │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Tool Usage Map

```
AGENT                 TOOL                    PURPOSE
│                     │                        │
│  Answer Analyzer ───┤                        │
│                     ├─→ File Reader          │ Read assignment files
│                     │                        │
│                     │                        │
│  Marking Agent ─────┤                        │
│                     ├─→ Rubric Evaluator     │ Score against criteria
│                     ├─→ Grade Boundary       │ Calculate letter grade
│                     │                        │
│                     │                        │
│  Feedback Generator─┤                        │
│                     ├─→ Feedback Template    │ Format feedback report
│                     ├─→ Detailed Comment     │ Criterion comments
│                     │                        │
│                     │                        │
│  Validator ─────────┤                        │
│                     ├─→ Validation Checker   │ Check consistency
│                     └─→ Baseline Comparison  │ Detect outliers
```

---

## 5. Data Flow Diagram

```
[Student Submission File] ──────────────────────────┐
                                                    │
[Rubric JSON File] ─────────────────────────────┐   │
                                                │   │
                                                ▼   ▼
                                        ┌───────────────┐
                                        │  File Reader  │
                                        │     Tool      │
                                        └───────┬───────┘
                                                │
                                                ▼
                                        ┌───────────────┐
                                        │  Initial State│
                                        │  Creation     │
                                        └───────┬───────┘
                                                │
                                                ▼
┌───────────────────────────────────────────────────────────┐
│                    LangGraph Workflow                     │
│                                                           │
│  Node 1: Answer Analyzer ─────→ State Update              │
│       ↓                                                    │
│  Node 2: Marking Agent ───────→ State Update              │
│       ↓                                                    │
│  Node 3: Feedback Generator ──→ State Update              │
│       ↓                                                    │
│  Node 4: Validator ──────────→ State Update               │
│                                                           │
└──────────────────────────────┬────────────────────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │ Final Output │
                        └──────┬───────┘
                               │
               ┌───────────────┼───────────────┐
               │               │               │
               ▼               ▼               ▼
         ┌──────────┐  ┌──────────┐  ┌──────────┐
         │  Grade   │  │ Feedback │  │  Logs    │
         │  Report  │  │  Report  │  │  (JSON)  │
         └──────────┘  └──────────┘  └──────────┘
```

---

## 6. Component Interaction Diagram

```
┌────────────────────────────────────────────────────────────┐
│                       main.py                              │
│  - Loads assignment data                                   │
│  - Initializes workflow                                    │
│  - Displays results                                        │
└────────────────────────┬───────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────┐
│                   orchestrator.py                          │
│  - Creates GradingWorkflow                                 │
│  - Builds LangGraph state graph                            │
│  - Executes workflow                                       │
└──┬──────────┬───────────┬───────────┬─────────────────────┘
   │          │           │           │
   ▼          ▼           ▼           ▼
┌──────┐  ┌──────┐  ┌──────────┐  ┌──────────┐
│Agent1│  │Agent2│  │ Agent3   │  │ Agent4   │
│      │  │      │  │          │  │          │
│Uses  │  │Uses  │  │ Uses     │  │ Uses     │
│Tool1 │  │Tool2 │  │ Tool3    │  │ Tool4    │
└──┬───┘  └──┬───┘  └────┬─────┘  └────┬─────┘
   │         │           │             │
   └─────────┴───────────┴─────────────┘
                     │
                     ▼
          ┌────────────────────┐
          │  Shared State      │
          │  (GradingState)    │
          └────────┬───────────┘
                   │
                   ▼
          ┌────────────────────┐
          │  AgentLogger       │
          │  (Observability)   │
          └────────────────────┘
```

---

## 7. Testing Architecture

```
┌──────────────────────────────────────────────────────┐
│                 Test Suite                           │
│                                                      │
│  ┌─────────────────────┐  ┌──────────────────────┐  │
│  │   test_tools.py     │  │  test_agents.py      │  │
│  │                     │  │                      │  │
│  │  Unit Tests:        │  │  Property Tests:     │  │
│  │  ├─ File Reader     │  │  ├─ Answer Analyzer  │  │
│  │  ├─ Rubric Eval     │  │  ├─ Marking Agent    │  │  │
│  │  ├─ Feedback Temp   │  │  ├─ Feedback Gen     │  │
│  │  └─ Validation      │  │  └─ Validator        │  │
│  └─────────────────────┘  └──────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │         Integration Tests                    │   │
│  │  ├─ State Management                         │   │
│  │  ├─ Workflow Execution                       │   │
│  │  └─ Security & Robustness                    │   │
│  └──────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

---

## Tips for Using These Diagrams

1. **Technical Report**: Use diagrams 1, 2, and 5
2. **Demo Video**: Show diagrams 1 and 2 during architecture explanation
3. **Viva Preparation**: Understand all diagrams thoroughly
4. **Presentation**: Convert to images using any ASCII-to-image converter

You can also recreate these in professional tools like:
- Draw.io (free)
- Lucidchart
- Microsoft Visio
- Figma
