# 👥 Team Coordination Guide

## How to Divide Work Among 4 Team Members

---

## 📋 Work Distribution

### Student 1: Answer Analyzer Specialist

**Responsibilities:**
- ✅ Develop `agents/answer_analyzer.py`
- ✅ Develop `tools/file_reader.py`
- ✅ Write tests for file reader tool
- ✅ Document the Answer Analyzer in technical report

**Key Files to Edit:**
```
agents/answer_analyzer.py       # PRIMARY
tools/file_reader.py            # PRIMARY
tests/test_tools.py             # TestFileReader class
TECHNICAL_REPORT.md             # Student 1 section
```

**Development Tasks:**
1. Design system prompt for answer analysis
2. Implement JSON parsing from LLM responses
3. Create file reading tools with error handling
4. Write tests for file I/O operations
5. Test with sample assignments

**Testing Focus:**
- File reading works correctly
- Error handling for missing files
- JSON parsing robustness
- Analysis score ranges (0.0-1.0)

---

### Student 2: Marking Agent Specialist

**Responsibilities:**
- ✅ Develop `agents/marking_agent.py`
- ✅ Develop `tools/rubric_evaluator.py`
- ✅ Write tests for rubric evaluator
- ✅ Document the Marking Agent in technical report

**Key Files to Edit:**
```
agents/marking_agent.py         # PRIMARY
tools/rubric_evaluator.py       # PRIMARY
tests/test_agents.py            # TestMarkingAgent class
tests/test_tools.py             # TestRubricEvaluator class
TECHNICAL_REPORT.md             # Student 2 section
```

**Development Tasks:**
1. Design system prompt for marking
2. Implement rubric evaluation algorithm
3. Blend tool and LLM evaluations
4. Create grade boundary calculator
5. Write comprehensive tests

**Testing Focus:**
- Marks within valid ranges
- Total marks = sum of criteria
- Percentage calculation accuracy
- Justifications for all criteria

---

### Student 3: Feedback Generator Specialist

**Responsibilities:**
- ✅ Develop `agents/feedback_generator.py`
- ✅ Develop `tools/feedback_template.py`
- ✅ Write tests for feedback tools
- ✅ Document the Feedback Generator in technical report

**Key Files to Edit:**
```
agents/feedback_generator.py    # PRIMARY
tools/feedback_template.py      # PRIMARY
tests/test_agents.py            # TestFeedbackGenerator class
tests/test_tools.py             # TestFeedbackTemplate class
TECHNICAL_REPORT.md             # Student 3 section
```

**Development Tasks:**
1. Design system prompt for feedback generation
2. Implement feedback template formatting
3. Create detailed comment generator
4. Ensure constructive tone
5. Write tests for feedback structure

**Testing Focus:**
- Feedback contains strengths
- Feedback contains improvements
- Recommendations are actionable
- Tone is constructive (not negative)

---

### Student 4: Validator Specialist

**Responsibilities:**
- ✅ Develop `agents/validator.py`
- ✅ Develop `tools/validation_checker.py`
- ✅ Write tests for validation tools
- ✅ Document the Validator in technical report

**Key Files to Edit:**
```
agents/validator.py             # PRIMARY
tools/validation_checker.py     # PRIMARY
tests/test_agents.py            # TestValidatorAgent class
tests/test_tools.py             # TestValidationChecker class
TECHNICAL_REPORT.md             # Student 4 section
```

**Development Tasks:**
1. Design system prompt for validation
2. Implement consistency checking algorithms
3. Create anomaly detection logic
4. Implement baseline comparison
5. Write tests for validation rules

**Testing Focus:**
- Detects invalid marks (> max, < 0)
- Checks sum consistency
- Identifies anomalies
- Provides recommendations

---

## 🔗 Integration Points

### Shared Files (Coordinate Changes)

**`state/graph_state.py`**
- All students need to understand this
- Define data structures together
- Don't modify without team agreement

**`orchestrator.py`**
- Student 1 or 4 should lead this
- Defines workflow sequence
- Integrates all agents

**`observability/logger.py`**
- One student implements (suggest Student 4)
- Others use the logger interface
- Don't modify logger API without discussion

**`main.py`**
- One student implements (suggest Student 1)
- Entry point for the system
- Displays results

**`tests/test_agents.py`**
- Each student writes their own test class
- Follow existing patterns
- Ensure all tests pass before integration

---

## 📅 Suggested Timeline

### Week 1: Setup & Design
- [ ] All: Read assignment requirements
- [ ] All: Understand the architecture
- [ ] All: Set up development environment
- [ ] Team: Agree on state structure
- [ ] Team: Define agent interfaces

### Week 2: Individual Development
- [ ] Student 1: Answer Analyzer + File Reader
- [ ] Student 2: Marking Agent + Rubric Evaluator
- [ ] Student 3: Feedback Generator + Feedback Template
- [ ] Student 4: Validator + Validation Checker

### Week 3: Integration & Testing
- [ ] All: Complete individual components
- [ ] All: Write tests for your components
- [ ] Team: Integrate into workflow
- [ ] Team: Run full system test
- [ ] Team: Fix integration issues

### Week 4: Documentation & Polish
- [ ] All: Write your section of technical report
- [ ] Team: Complete architecture diagrams
- [ ] Team: Create demo video
- [ ] Team: Prepare GitHub repository
- [ ] Team: Practice viva presentation

---

## 🤝 Collaboration Guidelines

### Git Workflow

**Option 1: Shared Repository (Recommended)**
```bash
# Everyone clones the same repo
git clone <repo-url>

# Create feature branches
git checkout -b student1-answer-analyzer
git checkout -b student2-marking-agent
git checkout -b student3-feedback
git checkout -b student4-validator

# Push branches
git push origin student1-answer-analyzer

# Create Pull Requests for review
# Merge to main after testing
```

**Option 2: Single Developer (If Git is complex)**
- One person manages the repository
- Others send code via email/cloud storage
- Manager integrates and commits

### Code Standards

**All code must have:**
1. Docstrings for every function/class
2. Type hints for parameters and return values
3. Error handling (try-except blocks)
4. Comments for complex logic

**Example:**
```python
def my_function(param1: str, param2: int) -> dict:
    """
    Brief description of what function does.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: If param1 is empty
    """
    try:
        # Implementation
        return result
    except Exception as e:
        # Error handling
        raise ValueError(f"Error: {str(e)}")
```

### Communication

**Regular Check-ins:**
- Weekly team meetings (minimum)
- Share progress and blockers
- Test integration frequently

**Shared Documents:**
- Google Docs for report writing
- Shared drive for resources
- Group chat for quick questions

---

## 🧩 Integration Checklist

### Before First Integration

- [ ] All agents run independently
- [ ] All tools work correctly
- [ ] All individual tests pass
- [ ] State structure agreed upon
- [ ] Orchestrator skeleton created

### Integration Steps

1. **Merge state management**:
   ```bash
   # Ensure everyone uses same graph_state.py
   git pull origin main
   ```

2. **Integrate agents one by one**:
   - Start with Answer Analyzer
   - Test it works
   - Add Marking Agent
   - Test again
   - Continue for all agents

3. **Run full workflow**:
   ```bash
   python main.py
   ```

4. **Verify output**:
   - Check all agents execute
   - Verify state passes correctly
   - Ensure logs are generated
   - Confirm results make sense

5. **Run all tests**:
   ```bash
   pytest tests/ -v
   ```

### After Integration

- [ ] All agents execute in sequence
- [ ] State passes correctly between agents
- [ ] All tests pass (35+)
- [ ] Logs generated correctly
- [ ] Results are reasonable
- [ ] Error handling works

---

## 📝 Technical Report Division

### Each Student Writes:

**Student 1:**
- Answer Agent Design section
- File Reader Tool description
- Individual contribution proof

**Student 2:**
- Marking Agent Design section
- Rubric Evaluator Tool description
- Individual contribution proof

**Student 3:**
- Feedback Agent Design section
- Feedback Template Tool description
- Individual contribution proof

**Student 4:**
- Validator Agent Design section
- Validation Checker Tool description
- Individual contribution proof

### Team Writes Together:

- Problem Domain (Section 1)
- System Architecture (Section 2)
- State Management (Section 5)
- Evaluation Methodology (Section 6)
- Conclusion (Section 9)

**Assign one person to compile and format the final report.**

---

## 🎥 Demo Video Division

**Suggested Script:**

**Student 1 (0:00-1:00):**
- Introduction
- Problem statement
- Architecture overview

**Student 2 (1:00-2:30):**
- Live demo start
- Show agents executing
- Explain marking process

**Student 3 (2:30-4:00):**
- Show results
- Display feedback
- Explain validation

**Student 4 (4:00-5:00):**
- Show tests
- Code quality
- Conclusion

**One person edits and finalizes the video.**

---

## 🎯 Viva Preparation

### Individual Preparation

Each student must know:
1. Their agent inside-out
2. Their tool implementation
3. Their test cases
4. How their component integrates

### Team Preparation

Practice together:
1. Full system demonstration
2. Architecture explanation
3. Handoffs between speakers
4. Q&A sessions

### Mock Viva

Schedule a practice session:
- One person acts as examiner
- Ask questions from `VIVA_PREPARATION.md`
- Practice explaining code
- Time the presentation

---

## ⚠️ Common Pitfalls & Solutions

### Pitfall 1: Integration Conflicts
**Problem**: Different state structures
**Solution**: Agree on `graph_state.py` BEFORE coding

### Pitfall 2: Tests Fail After Integration
**Problem**: Works individually, fails together
**Solution**: Test integration early and often

### Pitfall 3: Unequal Work Distribution
**Problem**: Some do more than others
**Solution**: Clear responsibilities, regular check-ins

### Pitfall 4: Last-Minute Rush
**Problem**: Everything due at once
**Solution**: Follow the timeline, set internal deadlines

### Pitfall 5: Poor Documentation
**Problem**: Code works but unclear
**Solution**: Write docs as you code, not after

---

## 📞 Emergency Contacts & Resources

### If Someone Falls Behind
1. Communicate early
2. Redistribute tasks if needed
3. Help each other
4. Focus on minimum viable product

### If Code Doesn't Work
1. Check logs in `logs/`
2. Run tests to isolate issue
3. Review error messages
4. Ask team for help

### If Time is Running Out
1. Prioritize core functionality
2. Ensure all 4 agents work
3. Get tests passing
4. Complete minimum documentation

---

## ✅ Final Submission Checklist

### Code Repository
- [ ] All agents implemented
- [ ] All tools implemented
- [ ] All tests passing
- [ ] README complete
- [ ] Code commented
- [ .gitignore configured

### Documentation
- [ ] Technical report (4-8 pages)
- [ ] Architecture diagrams
- [ ] Individual contributions documented
- [ ] GitHub link included

### Demo Video
- [ ] 4-5 minutes long
- [ ] Shows full workflow
- [ ] Clear narration
- [ ] Professional quality

### Individual Proof
- [ ] Each student's agent code
- [ ] Each student's tool code
- [ ] Each student's tests
- [ ] Challenges documented

---

## 🍀 Good Luck!

Remember:
- **Communicate** frequently
- **Test** early and often
- **Document** as you go
- **Support** each other

**You've got this as a team! 💪**
