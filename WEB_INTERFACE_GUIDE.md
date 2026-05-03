# 🌐 Web Interface User Guide

## Complete Guide to the Automated Assignment Grading System Web App

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Web App

**Windows:**
```bash
# Double-click this file:
run_web.bat

# Or run manually:
streamlit run web_app.py
```

**Mac/Linux:**
```bash
streamlit run web_app.py
```

### 3. Access the Interface
The app will automatically open in your browser at:
```
http://localhost:8501
```

---

## 📱 Interface Overview

The web app has **5 main tabs**:

1. 📥 **Input Configuration** - Upload answers and configure rubrics
2. 🤖 **Agent Pipeline** - Watch agents work in real-time
3. 📊 **Grading Results** - View detailed marks and feedback
4. 📝 **Agent Activity Logs** - Complete observability
5. 📄 **Final Report** - Comprehensive grading report

---

## 📥 Tab 1: Input Configuration

### What You Can Do:
- ✅ Paste student answers manually
- ✅ Upload answer files (.txt, .md)
- ✅ Load sample answer with one click
- ✅ Configure marking rubric in JSON
- ✅ Upload rubric files (.json)
- ✅ Load sample rubric with one click
- ✅ Preview rubric in table format
- ✅ Set student and assignment IDs

### Step-by-Step:

#### Option A: Use Sample Data (Quick Demo)
1. Click **"📄 Load Sample Answer"**
2. Click **"📊 Load Sample Rubric"**
3. Review the loaded data
4. Click **"🚀 Start Grading Process"**

#### Option B: Upload Your Own Data
1. **Student Answer:**
   - Paste text in the text area, OR
   - Upload a .txt/.md file
   
2. **Assignment Question:**
   - Edit the question text (pre-filled with sample)

3. **Marking Rubric:**
   - Edit JSON directly, OR
   - Upload a .json file
   
4. **Student Info:**
   - Enter Student ID
   - Enter Assignment ID

5. Click **"🚀 Start Grading Process"**

### Rubric JSON Format:
```json
[
  {
    "criterion_id": "C1_Knowledge",
    "description": "Understanding of concepts",
    "max_marks": 10,
    "keywords": ["machine learning", "AI", "algorithms"]
  },
  {
    "criterion_id": "C2_Application",
    "description": "Practical application",
    "max_marks": 10,
    "keywords": ["examples", "implementation", "use case"]
  }
]
```

---

## 🤖 Tab 2: Agent Pipeline

### What You'll See:
- 🔄 Real-time pipeline execution
- 📊 Progress bar showing completion
- 📝 Status updates for each agent
- 🎯 Step-by-step execution flow

### The 4 Agents Execute In Order:

1. **🔍 Answer Analyzer**
   - Analyzes student answer
   - Identifies key concepts
   - Assesses completeness, relevance, clarity

2. **📝 Marking Agent**
   - Evaluates against rubric
   - Assigns marks per criterion
   - Provides justifications

3. **💬 Feedback Generator**
   - Creates constructive feedback
   - Identifies strengths
   - Provides recommendations

4. **✅ Validator**
   - Checks grading consistency
   - Detects anomalies
   - Validates fairness

### How to Use:
1. Click **"▶️ Execute Pipeline"**
2. Watch the progress bar
3. Expand each agent step to see details
4. Wait for completion message
5. Switch to "Grading Results" tab

---

## 📊 Tab 3: Grading Results

### What's Displayed:

#### 🎯 Overall Performance
- **Total Marks**: e.g., 35/50
- **Percentage**: e.g., 70%
- **Grade**: e.g., B+
- **Validation Status**: Passed/Failed

#### 📋 Detailed Criterion Breakdown
Interactive table showing:
- Criterion ID
- Description
- Marks Obtained
- Max Marks
- Percentage
- Justification

#### 📈 Marks Distribution
Visual bar chart showing:
- Marks obtained vs max marks per criterion

#### 💬 Detailed Feedback
- **Overall Assessment**: Summary paragraph
- **Areas of Strength**: Bullet list
- **Areas for Improvement**: Bullet list
- **Actionable Recommendations**: Step-by-step guide

#### ✅ Validation Report
- Consistency score
- Anomalies detected
- Validator recommendations

---

## 📝 Tab 4: Agent Activity Logs

### Complete Observability

#### 📊 Session Information
- Session ID
- Start/End time
- Number of agents executed
- Number of tools called
- Error count

#### 🤖 Agent Executions
For each agent:
- Status (success/failed)
- Processing time
- Input summary
- Output summary

#### 🔧 Tool Calls
For each tool:
- Tool name
- Called by which agent
- Status
- Execution time
- Parameters used
- Result summary

#### ❌ Errors (if any)
- Error type
- Error message
- Context information

#### 📈 Session Summary
- Final grade
- Validation status
- Overall status
- Error count

### How to Navigate Logs:
1. Expand sections using expander arrows
2. Click through each agent execution
3. Review tool calls for details
4. Check for any errors
5. View summary statistics

---

## 📄 Tab 5: Final Report

### Comprehensive Report Contains:

#### 📋 Header Information
- Student ID
- Assignment ID
- Submission date

#### ❓ Assignment Question
Full question text

#### 📝 Student Answer
Complete student submission (expandable)

#### 🎯 Final Grade
- Total marks
- Percentage
- Letter grade with description

#### 📊 Criterion-wise Breakdown
For each criterion:
- Description
- Marks awarded
- Justification

#### 💬 Feedback Summary
- Overall feedback
- Strengths list
- Areas for improvement
- Recommendations

#### ✅ Validation Report
- Validation status
- Consistency score
- Anomalies (if any)

#### 📥 Export Options
- Download report as text file
- Save for records
- Share with students

---

## 💡 Pro Tips

### For Quick Testing:
1. Use "Load Sample Answer" and "Load Sample Rubric"
2. Click "Start Grading Process"
3. Execute pipeline
4. Review results in under 2 minutes

### For Real Assignments:
1. Prepare rubric JSON in advance
2. Upload student answers
3. Run pipeline for each student
4. Export final reports
5. Check logs for quality assurance

### For Best Performance:
- Keep answers under 2000 words
- Define 3-7 rubric criteria
- Include relevant keywords in rubric
- Use descriptive criterion IDs
- Review logs for any anomalies

---

## 🎨 UI Features

### Visual Elements:
- 🎨 **Color-coded sections** for easy navigation
- 📊 **Interactive charts** for marks visualization
- 📋 **Data tables** with sorting
- 📈 **Progress bars** for pipeline execution
- 🎯 **Metric cards** for key statistics
- 💡 **Tooltips** for help text
- 🔄 **Expandable sections** for details

### Responsive Design:
- Works on desktop and tablet
- Wide layout for better visibility
- Organized tabs for clean interface
- Professional color scheme

---

## 🔧 Troubleshooting

### App Won't Start
```bash
# Reinstall Streamlit
pip install --upgrade streamlit pandas

# Check if port 8501 is free
netstat -ano | findstr :8501
```

### "Module Not Found" Error
```bash
# Install missing packages
pip install -r requirements.txt
```

### Pipeline Execution Fails
1. Check Ollama is running: `ollama list`
2. Verify model is downloaded: `ollama pull llama3:8b`
3. Check logs in Tab 4
4. Try with sample data first

### Results Look Incorrect
1. Review rubric JSON format
2. Check keyword lists in rubric
3. Verify answer text is complete
4. Check validation report in Tab 3
5. Review agent logs in Tab 4

---

## 📊 Example Workflow

### Complete Demo (5 minutes):

1. **Open App** (0:00)
   - Run `streamlit run web_app.py`
   - Browser opens automatically

2. **Load Sample Data** (0:30)
   - Click "Load Sample Answer"
   - Click "Load Sample Rubric"
   - Preview the data

3. **Start Grading** (1:00)
   - Click "Start Grading Process"
   - Switch to "Agent Pipeline" tab

4. **Watch Pipeline** (2:30)
   - Click "Execute Pipeline"
   - Watch each agent execute
   - See progress bar complete

5. **Review Results** (3:30)
   - Switch to "Grading Results"
   - View marks breakdown
   - Read feedback

6. **Check Logs** (4:00)
   - Switch to "Agent Activity Logs"
   - Review agent executions
   - Check tool calls

7. **Export Report** (4:30)
   - Switch to "Final Report"
   - Review complete report
   - Download as text file

---

## 🎯 Use Cases

### For Teachers:
- ✅ Grade assignments quickly
- ✅ Ensure consistent marking
- ✅ Generate detailed feedback
- ✅ Export reports for records
- ✅ Review grading quality via logs

### For Students:
- ✅ Get instant feedback
- ✅ Understand marks breakdown
- ✅ See areas for improvement
- ✅ Receive actionable recommendations

### For Administrators:
- ✅ Audit grading process
- ✅ Review agent decisions
- ✅ Ensure fairness via validation
- ✅ Access complete logs

---

## 📱 Mobile Access

To access from mobile devices on same network:

```bash
# Find your IP address
ipconfig  # Windows
ifconfig  # Mac/Linux

# Run with host option
streamlit run web_app.py --server.address 0.0.0.0

# Access from mobile:
http://YOUR_IP_ADDRESS:8501
```

---

## 🚀 Advanced Configuration

### Change Port:
```bash
streamlit run web_app.py --server.port 8502
```

### Run in Headless Mode:
```bash
streamlit run web_app.py --server.headless true
```

### Custom Theme:
Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

---

## 📞 Support

### Common Issues:

**Q: App is slow?**
A: SLM processing takes 1-2 minutes per agent. This is normal.

**Q: Can I grade multiple students?**
A: Yes! Run pipeline for each student. Results are saved separately.

**Q: Where are logs saved?**
A: In `logs/` directory as JSON files with timestamps.

**Q: Can I customize the UI?**
A: Edit CSS in `web_app.py` or create custom theme.

---

## 🎓 Next Steps

1. ✅ Try the sample data first
2. ✅ Upload your own assignments
3. ✅ Customize rubrics for your needs
4. ✅ Review logs for quality assurance
5. ✅ Export reports for students
6. ✅ Provide feedback for improvements

---

## 📚 Additional Resources

- **Setup Guide**: See `GETTING_STARTED.md`
- **Architecture**: See `ARCHITECTURE_DIAGRAMS.md`
- **Technical Report**: See `TECHNICAL_REPORT.md`
- **Viva Prep**: See `VIVA_PREPARATION.md`

---

**Enjoy grading with AI! 🎉**

*Built with Streamlit + LangGraph + Ollama*
