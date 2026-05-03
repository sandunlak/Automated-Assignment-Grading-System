"""
Web Frontend for Automated Assignment Grading System

Provides a user-friendly interface for:
- Uploading student answers
- Configuring marking rubrics
- Running the multi-agent grading pipeline
- Viewing detailed results and logs
"""

import streamlit as st
import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import List
import pandas as pd

from state.graph_state import GradingState, RubricCriterion, AnalysisResult, MarkingResult, FeedbackResult, ValidationResult
from orchestrator import GradingWorkflow


# Page configuration
st.set_page_config(
    page_title="Automated Assignment Grading System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .agent-step {
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-left: 4px solid #1f77b4;
        background-color: #f8f9fa;
    }
    .log-entry {
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        background-color: #f5f5f5;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 0.25rem;
    }
</style>
""", unsafe_allow_html=True)


def load_sample_assignment() -> str:
    """Load sample assignment from file."""
    try:
        with open("data/sample_assignment.txt", "r", encoding="utf-8") as f:
            content = f.read()
            # Extract just the student answer part
            parts = content.split("Student Answer:")
            if len(parts) > 1:
                return parts[1].strip()
            return content
    except Exception as e:
        st.error(f"Error loading sample assignment: {str(e)}")
        return ""


def load_sample_rubric() -> List[dict]:
    """Load sample rubric from file."""
    try:
        with open("data/sample_rubric.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("rubric", [])
    except Exception as e:
        st.error(f"Error loading sample rubric: {str(e)}")
        return []


def display_agent_progress(step: int, total_steps: int, agent_name: str, status: str = "running"):
    """Display agent execution progress."""
    icons = {
        "running": "🔄",
        "success": "✅",
        "failed": "❌"
    }
    
    icon = icons.get(status, "⏳")
    
    with st.sidebar:
        st.markdown(f"### {icon} Step {step}/{total_steps}")
        st.markdown(f"**{agent_name}**")
        
        if status == "running":
            st.info("Processing...")
        elif status == "success":
            st.success("Complete")
        elif status == "failed":
            st.error("Failed")
        
        st.markdown("---")


def main():
    """Main application."""
    
    # Header
    st.markdown('<p class="main-header">🎓 Automated Assignment Grading System</p>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Multi-Agent AI Powered Grading with Complete Observability</p>', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📥 Input Configuration",
        "🤖 Agent Pipeline",
        "📊 Grading Results",
        "📝 Agent Activity Logs",
        "📄 Final Report"
    ])
    
    # Initialize session state
    if 'grading_state' not in st.session_state:
        st.session_state.grading_state = None
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    if 'grading_complete' not in st.session_state:
        st.session_state.grading_complete = False
    
    # ============ TAB 1: Input Configuration ============
    with tab1:
        st.markdown('<p class="sub-header">📥 Input Configuration</p>', unsafe_allow_html=True)
        st.markdown("Upload student answers and configure the marking rubric")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📝 Student Answer")
            
            # Load sample button
            if st.button("📄 Load Sample Answer", type="secondary"):
                sample_answer = load_sample_assignment()
                if sample_answer:
                    st.session_state['sample_answer_loaded'] = sample_answer
                    st.success("Sample answer loaded!")
            
            # Text area for student answer
            student_answer = st.text_area(
                "Paste student answer here:",
                value=st.session_state.get('sample_answer_loaded', ''),
                height=300,
                placeholder="Student's answer will appear here...",
                help="Paste the student's answer or load the sample answer"
            )
            
            # File upload option
            st.markdown("**Or upload a file:**")
            uploaded_file = st.file_uploader(
                "Upload student answer file",
                type=['txt', 'md'],
                help="Upload a .txt or .md file containing the student's answer"
            )
            
            if uploaded_file is not None:
                student_answer = uploaded_file.read().decode('utf-8')
                st.success(f"✅ File '{uploaded_file.name}' loaded successfully")
            
            # Assignment question
            st.markdown("### ❓ Assignment Question")
            assignment_question = st.text_area(
                "Assignment question:",
                value="Explain the concept of machine learning and describe the differences between supervised and unsupervised learning. Provide examples of each and discuss their applications.",
                height=100
            )
            
            # Student metadata
            st.markdown("### 🏷️ Student Information")
            col_meta1, col_meta2 = st.columns(2)
            with col_meta1:
                student_id = st.text_input("Student ID", value="STU2024001")
            with col_meta2:
                assignment_id = st.text_input("Assignment ID", value="ML_ASSIGNMENT_01")
        
        with col2:
            st.markdown("### 📋 Marking Rubric")
            
            # Load sample button
            if st.button("📊 Load Sample Rubric", type="secondary"):
                sample_rubric = load_sample_rubric()
                if sample_rubric:
                    st.session_state['sample_rubric_loaded'] = sample_rubric
                    st.success("Sample rubric loaded!")
            
            # Rubric configuration
            rubric_json = st.text_area(
                "Rubric (JSON format):",
                value=json.dumps(st.session_state.get('sample_rubric_loaded', []), indent=2),
                height=400,
                help="Define rubric criteria in JSON format"
            )
            
            # Rubric file upload
            st.markdown("**Or upload a rubric file:**")
            rubric_file = st.file_uploader(
                "Upload rubric JSON file",
                type=['json'],
                help="Upload a .json file containing the rubric"
            )
            
            if rubric_file is not None:
                rubric_json = rubric_file.read().decode('utf-8')
                st.success(f"✅ Rubric file '{rubric_file.name}' loaded successfully")
            
            # Rubric preview
            try:
                rubric_data = json.loads(rubric_json)
                if rubric_data:
                    st.markdown("### 👁️ Rubric Preview")
                    
                    # Create a dataframe for better visualization
                    rubric_df = pd.DataFrame(rubric_data)
                    st.dataframe(rubric_df, use_container_width=True)
                    
                    st.info(f"📊 Total Criteria: {len(rubric_data)}")
                    total_marks = sum(item.get('max_marks', 0) for item in rubric_data)
                    st.info(f"🎯 Total Marks: {total_marks}")
            except json.JSONDecodeError:
                st.warning("⚠️ Invalid JSON format. Please check your rubric configuration.")
        
        # Run grading button
        st.markdown("---")
        if st.button("🚀 Start Grading Process", type="primary", use_container_width=True):
            if not student_answer or not rubric_json:
                st.error("❌ Please provide both student answer and rubric")
            else:
                try:
                    # Parse rubric
                    rubric_data = json.loads(rubric_json)
                    rubric_criteria = []
                    for item in rubric_data:
                        criterion = RubricCriterion(
                            criterion_id=item['criterion_id'],
                            description=item['description'],
                            max_marks=item['max_marks'],
                            keywords=item.get('keywords', [])
                        )
                        rubric_criteria.append(criterion)
                                
                    # Create initial state
                    initial_state = GradingState(
                        assignment_question=assignment_question,
                        student_answer_raw=student_answer,
                        rubric=rubric_criteria,
                        analysis_result=None,
                        marking_result=None,
                        feedback_result=None,
                        validation_result=None,
                        student_id=student_id,
                        assignment_id=assignment_id,
                        processing_status="initialized",
                        error_messages=[],
                        final_grade=None,
                        final_feedback=None,
                        ready_for_review=False
                    )
                                
                    st.session_state.initial_state = initial_state
                    st.session_state.logs = []
                                
                    # Execute the ACTUAL grading pipeline right here
                    with st.spinner("🤖 Executing multi-agent grading pipeline... This may take 4-8 minutes."):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                                    
                        try:
                            # Import and execute the real workflow
                            from orchestrator import GradingWorkflow
                                        
                            workflow = GradingWorkflow()
                                        
                            # Execute step by step with progress tracking
                            status_text.text("🔍 Step 1/4: Answer Analyzer is processing...")
                            progress_bar.progress(0.1)
                                        
                            status_text.text("📝 Step 2/4: Marking Agent is evaluating...")
                            progress_bar.progress(0.3)
                                        
                            status_text.text("💬 Step 3/4: Feedback Generator is creating feedback...")
                            progress_bar.progress(0.6)
                                        
                            status_text.text("✅ Step 4/4: Validator is checking consistency...")
                            progress_bar.progress(0.8)
                                        
                            # Execute the complete workflow (this runs all 4 agents with llama3:8b)
                            final_state = workflow.execute(initial_state)
                                        
                            progress_bar.progress(1.0)
                            status_text.text("✅ Grading complete!")
                                        
                            # Save results to session state
                            st.session_state.grading_state = final_state
                            st.session_state.grading_complete = True
                                        
                            st.success("🎉 Grading complete! Switch to 'Grading Results' tab to view detailed output.")
                                        
                        except Exception as exec_error:
                            st.error(f"❌ Pipeline execution failed: {str(exec_error)}")
                            st.info("💡 Make sure Ollama is running and llama3:8b model is downloaded.")
                            st.code("Run: ollama list (to check models)")
                            st.code("Run: ollama pull llama3:8b (if not found)")
                                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
    
    # ============ TAB 2: Agent Pipeline ============
    with tab2:
        st.markdown('<p class="sub-header">🤖 Agent Pipeline Execution</p>', unsafe_allow_html=True)
        st.markdown("Watch the multi-agent system process your submission in real-time")
        
        if 'initial_state' not in st.session_state:
            st.warning("⚠️ Please configure input in the 'Input Configuration' tab first.")
        else:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Agent execution visualization
            st.markdown("### 🔄 Pipeline Execution")
            
            agents = [
                ("Answer Analyzer", "🔍", "Analyzing student answer and identifying key concepts..."),
                ("Marking Agent", "📝", "Evaluating against rubric and assigning marks..."),
                ("Feedback Generator", "💬", "Generating constructive feedback..."),
                ("Validator", "✅", "Validating grading consistency...")
            ]
            
            # Create execution containers
            agent_containers = []
            for agent_name, icon, description in agents:
                container = st.container()
                agent_containers.append({
                    'name': agent_name,
                    'icon': icon,
                    'description': description,
                    'container': container,
                    'status': 'pending'
                })
            
            # Run grading button is now in Tab 1, Tab 2 just shows execution visualization
            if st.button("▶️ Re-Execute Pipeline", type="primary", use_container_width=True):
                if 'initial_state' not in st.session_state:
                    st.error("❌ Please configure input in Tab 1 first")
                else:
                    try:
                        # Execute the actual workflow
                        with st.spinner("🤖 Executing multi-agent grading pipeline..."):
                            from orchestrator import GradingWorkflow
                            workflow = GradingWorkflow()
                            final_state = workflow.execute(st.session_state.initial_state)
                            
                            st.session_state.grading_state = final_state
                            st.session_state.grading_complete = True
                            
                            st.success("🎉 Grading complete! Check the 'Grading Results' tab.")
                    except Exception as e:
                        st.error(f"❌ Pipeline execution failed: {str(e)}")
    
    # ============ TAB 3: Grading Results ============
    with tab3:
        st.markdown('<p class="sub-header">📊 Grading Results</p>', unsafe_allow_html=True)
        
        if not st.session_state.get('grading_complete') or not st.session_state.get('grading_state'):
            st.warning("⚠️ No grading results available. Please run the agent pipeline first.")
        else:
            state = st.session_state.grading_state
            
            # Overall metrics
            st.markdown("### 🎯 Overall Performance")
            
            col1, col2, col3, col4 = st.columns(4)
            
            if state.get('marking_result'):
                marking = state['marking_result']
                
                with col1:
                    st.metric("Total Marks", f"{marking.total_marks}/{marking.max_possible_marks}")
                
                with col2:
                    st.metric("Percentage", f"{marking.percentage:.1f}%")
                
                with col3:
                    # Grade calculation
                    percentage = marking.percentage
                    if percentage >= 90:
                        grade = "A+"
                    elif percentage >= 80:
                        grade = "A"
                    elif percentage >= 75:
                        grade = "A-"
                    elif percentage >= 70:
                        grade = "B+"
                    elif percentage >= 65:
                        grade = "B"
                    elif percentage >= 60:
                        grade = "B-"
                    elif percentage >= 55:
                        grade = "C+"
                    elif percentage >= 50:
                        grade = "C"
                    else:
                        grade = "F"
                    
                    st.metric("Grade", grade)
                
                with col4:
                    validation = state.get('validation_result')
                    if validation:
                        status = "✅ Passed" if validation.validation_passed else "⚠️ Failed"
                    else:
                        status = "❓ Unknown"
                    st.metric("Validation", status)
            
            # Criterion breakdown
            st.markdown("---")
            st.markdown("### 📋 Detailed Criterion Breakdown")
            
            if state.get('marking_result') and state['marking_result'].criterion_marks:
                marking = state['marking_result']
                
                # Create dataframe
                criteria_data = []
                for criterion_id, marks in marking.criterion_marks.items():
                    # Find criterion description
                    criterion_obj = next((c for c in state['rubric'] if c.criterion_id == criterion_id), None)
                    description = criterion_obj.description if criterion_obj else "N/A"
                    max_marks = criterion_obj.max_marks if criterion_obj else 0
                    justification = marking.marking_justification.get(criterion_id, "N/A")
                    
                    criteria_data.append({
                        'Criterion': criterion_id,
                        'Description': description,
                        'Marks Obtained': marks,
                        'Max Marks': max_marks,
                        'Percentage': f"{(marks/max_marks*100) if max_marks > 0 else 0:.1f}%",
                        'Justification': justification
                    })
                
                criteria_df = pd.DataFrame(criteria_data)
                st.dataframe(criteria_df, use_container_width=True)
                
                # Visualization
                st.markdown("### 📈 Marks Distribution")
                
                # Bar chart
                chart_data = pd.DataFrame({
                    'Criterion': [c['Criterion'] for c in criteria_data],
                    'Marks Obtained': [c['Marks Obtained'] for c in criteria_data],
                    'Max Marks': [c['Max Marks'] for c in criteria_data]
                })
                
                st.bar_chart(chart_data.set_index('Criterion'))
            
            # Feedback section
            st.markdown("---")
            st.markdown("### 💬 Detailed Feedback")
            
            if state.get('feedback_result'):
                feedback = state['feedback_result']
                
                # Overall feedback
                st.markdown("#### Overall Assessment")
                st.info(feedback.overall_feedback)
                
                # Strengths and weaknesses
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("#### ✅ Areas of Strength")
                    if feedback.areas_of_strength:
                        for strength in feedback.areas_of_strength:
                            st.success(f"• {strength}")
                    else:
                        st.warning("No strengths identified")
                
                with col2:
                    st.markdown("#### ⚠️ Areas for Improvement")
                    if feedback.areas_for_improvement:
                        for weakness in feedback.areas_for_improvement:
                            st.warning(f"• {weakness}")
                    else:
                        st.info("No areas for improvement identified")
                
                # Recommendations
                st.markdown("#### 💡 Actionable Recommendations")
                if feedback.actionable_recommendations:
                    for rec in feedback.actionable_recommendations:
                        st.markdown(f"→ {rec}")
                else:
                    st.info("No recommendations provided")
            
            # Validation results
            st.markdown("---")
            st.markdown("### ✅ Validation Report")
            
            if state.get('validation_result'):
                validation = state['validation_result']
                
                if validation.validation_passed:
                    st.success("✅ **Grading validation passed** - Results are consistent and reliable")
                else:
                    st.warning("⚠️ **Validation concerns detected** - Manual review recommended")
                
                st.metric("Consistency Score", f"{validation.consistency_score:.2f}")
                
                if validation.anomalies_detected:
                    st.markdown("#### Anomalies Detected:")
                    for anomaly in validation.anomalies_detected:
                        st.warning(f"• {anomaly}")
                
                if validation.recommendations:
                    st.markdown("#### Validator Recommendations:")
                    for rec in validation.recommendations:
                        st.info(f"• {rec}")
    
    # ============ TAB 4: Agent Activity Logs ============
    with tab4:
        st.markdown('<p class="sub-header">📝 Agent Activity Logs</p>', unsafe_allow_html=True)
        st.markdown("Complete observability — every input, tool call, and output is logged")
        
        # Load logs from file system
        logs_dir = Path("logs")
        if logs_dir.exists():
            log_files = list(logs_dir.glob("*.json"))
            
            if log_files:
                # Get the latest log file
                latest_log = max(log_files, key=lambda x: x.stat().st_mtime)
                
                st.info(f"📁 Latest log file: `{latest_log.name}`")
                
                try:
                    with open(latest_log, 'r', encoding='utf-8') as f:
                        log_data = json.load(f)
                    
                    # Session info
                    st.markdown("### 📊 Session Information")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Session ID:** `{log_data.get('session_id', 'N/A')}`")
                        st.markdown(f"**Start Time:** `{log_data.get('start_time', 'N/A')}`")
                        st.markdown(f"**End Time:** `{log_data.get('end_time', 'N/A')}`")
                    
                    with col2:
                        st.markdown(f"**Agents Executed:** {len(log_data.get('agents_executed', []))}")
                        st.markdown(f"**Tools Called:** {len(log_data.get('tools_called', []))}")
                        st.markdown(f"**Errors:** {len(log_data.get('errors', []))}")
                    
                    # Agent executions
                    st.markdown("---")
                    st.markdown("### 🤖 Agent Executions")
                    
                    if 'agents_executed' in log_data:
                        for idx, agent_log in enumerate(log_data['agents_executed'], 1):
                            with st.expander(f"{idx}. {agent_log.get('agent_name', 'Unknown')} - {agent_log.get('status', 'unknown')}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown(f"**Status:** {agent_log.get('status', 'N/A')}")
                                    st.markdown(f"**Processing Time:** {agent_log.get('processing_time_seconds', 0):.2f}s")
                                
                                with col2:
                                    st.markdown("**Input Summary:**")
                                    st.code(str(agent_log.get('input_summary', 'N/A'))[:200])
                                
                                st.markdown("**Output Summary:**")
                                st.code(str(agent_log.get('output_summary', 'N/A'))[:300])
                    
                    # Tool calls
                    st.markdown("---")
                    st.markdown("### 🔧 Tool Calls")
                    
                    if 'tools_called' in log_data:
                        for idx, tool_log in enumerate(log_data['tools_called'], 1):
                            with st.expander(f"{idx}. {tool_log.get('tool_name', 'Unknown')} (called by {tool_log.get('called_by_agent', 'unknown')})"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.markdown(f"**Status:** {tool_log.get('status', 'N/A')}")
                                    st.markdown(f"**Execution Time:** {tool_log.get('execution_time_seconds', 0):.2f}s")
                                
                                with col2:
                                    st.markdown("**Parameters:**")
                                    st.code(str(tool_log.get('parameters', 'N/A'))[:200])
                                
                                st.markdown("**Result:**")
                                st.code(str(tool_log.get('result_summary', 'N/A'))[:300])
                    
                    # Errors
                    if 'errors' in log_data and log_data['errors']:
                        st.markdown("---")
                        st.markdown("### ❌ Errors")
                        
                        for idx, error_log in enumerate(log_data['errors'], 1):
                            st.error(f"**{idx}. {error_log.get('error_type', 'Unknown')}**")
                            st.error(error_log.get('error_message', 'No message'))
                            
                            if error_log.get('context'):
                                st.code(str(error_log['context'])[:200])
                    
                    # Summary
                    st.markdown("---")
                    st.markdown("### 📈 Session Summary")
                    
                    if 'summary' in log_data:
                        summary = log_data['summary']
                        for key, value in summary.items():
                            st.markdown(f"**{key}:** {value}")
                
                except Exception as e:
                    st.error(f"Error reading log file: {str(e)}")
            else:
                st.info("📝 No log files found yet. Run the grading pipeline to generate logs.")
        else:
            st.info("📁 Logs directory does not exist yet. It will be created when you run the grading pipeline.")
        
        # Session logs (from current execution)
        if st.session_state.logs:
            st.markdown("---")
            st.markdown("### 🔄 Current Session Logs")
            
            for log in st.session_state.logs:
                st.markdown(f"`[{log['timestamp']}]` **{log['agent']}** - {log['status']}")
    
    # ============ TAB 5: Final Report ============
    with tab5:
        st.markdown('<p class="sub-header">📄 Final Grading Report</p>', unsafe_allow_html=True)
        st.markdown("Comprehensive grading report with all details")
        
        if not st.session_state.get('grading_complete') or not st.session_state.get('grading_state'):
            st.warning("⚠️ No report available. Please run the agent pipeline first.")
        else:
            state = st.session_state.grading_state
            
            # Report header
            st.markdown("---")
            st.markdown("## 🎓 Assignment Grading Report")
            st.markdown("---")
            
            # Student information
            st.markdown("### Student Information")
            st.markdown(f"**Student ID:** {state.get('student_id', 'N/A')}")
            st.markdown(f"**Assignment ID:** {state.get('assignment_id', 'N/A')}")
            st.markdown(f"**Submission Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            st.markdown("---")
            
            # Assignment question
            st.markdown("### Assignment Question")
            st.markdown(state.get('assignment_question', 'N/A'))
            
            st.markdown("---")
            
            # Student answer
            st.markdown("### Student Answer")
            with st.expander("View full answer"):
                st.markdown(state.get('student_answer_raw', 'N/A'))
            
            st.markdown("---")
            
            # Final grade
            st.markdown("### Final Grade")
            
            if state.get('marking_result'):
                marking = state['marking_result']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Total Marks:** `{marking.total_marks}/{marking.max_possible_marks}`")
                    st.markdown(f"**Percentage:** `{marking.percentage:.1f}%`")
                
                with col2:
                    # Calculate grade
                    percentage = marking.percentage
                    if percentage >= 90:
                        grade = "A+ (Outstanding)"
                    elif percentage >= 80:
                        grade = "A (Excellent)"
                    elif percentage >= 75:
                        grade = "A- (Very Good)"
                    elif percentage >= 70:
                        grade = "B+ (Good)"
                    elif percentage >= 65:
                        grade = "B (Above Average)"
                    elif percentage >= 60:
                        grade = "B- (Average)"
                    elif percentage >= 55:
                        grade = "C+ (Satisfactory)"
                    elif percentage >= 50:
                        grade = "C (Pass)"
                    else:
                        grade = "F (Fail)"
                    
                    st.markdown(f"**Grade:** `{grade}`")
            
            st.markdown("---")
            
            # Criterion breakdown
            st.markdown("### Criterion-wise Breakdown")
            
            if state.get('marking_result') and state['marking_result'].criterion_marks:
                marking = state['marking_result']
                
                for criterion_id, marks in marking.criterion_marks.items():
                    criterion_obj = next((c for c in state['rubric'] if c.criterion_id == criterion_id), None)
                    
                    if criterion_obj:
                        st.markdown(f"#### {criterion_id}: {criterion_obj.description}")
                        st.markdown(f"**Marks:** {marks}/{criterion_obj.max_marks}")
                        
                        justification = marking.marking_justification.get(criterion_id, 'N/A')
                        st.markdown(f"**Justification:** {justification}")
                        
                        st.markdown("")
            
            st.markdown("---")
            
            # Feedback
            st.markdown("### Feedback Summary")
            
            if state.get('feedback_result'):
                feedback = state['feedback_result']
                
                st.markdown("#### Overall Feedback")
                st.markdown(feedback.overall_feedback)
                
                st.markdown("#### Strengths")
                for strength in feedback.areas_of_strength:
                    st.markdown(f"✅ {strength}")
                
                st.markdown("#### Areas for Improvement")
                for weakness in feedback.areas_for_improvement:
                    st.markdown(f"⚠️ {weakness}")
                
                st.markdown("#### Recommendations")
                for rec in feedback.actionable_recommendations:
                    st.markdown(f"💡 {rec}")
            
            st.markdown("---")
            
            # Validation
            st.markdown("### Validation Report")
            
            if state.get('validation_result'):
                validation = state['validation_result']
                
                if validation.validation_passed:
                    st.success("✅ Grading validation passed")
                else:
                    st.warning("⚠️ Validation issues detected")
                
                st.markdown(f"**Consistency Score:** {validation.consistency_score:.2f}")
                
                if validation.anomalies_detected:
                    st.markdown("**Anomalies:**")
                    for anomaly in validation.anomalies_detected:
                        st.markdown(f"• {anomaly}")
            
            st.markdown("---")
            
            # Export report
            st.markdown("### 📥 Export Report")
            
            if st.button("📄 Download Report as Text"):
                # Generate report text
                report_text = f"""
AUTOMATED ASSIGNMENT GRADING REPORT
=====================================

Student ID: {state.get('student_id', 'N/A')}
Assignment ID: {state.get('assignment_id', 'N/A')}
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

QUESTION:
{state.get('assignment_question', 'N/A')}

FINAL GRADE: {state['marking_result'].total_marks}/{state['marking_result'].max_possible_marks} ({state['marking_result'].percentage:.1f}%)

CRITERION BREAKDOWN:
"""
                
                for criterion_id, marks in state['marking_result'].criterion_marks.items():
                    report_text += f"\n{criterion_id}: {marks} marks"
                
                report_text += f"\n\nFEEDBACK:\n{state['feedback_result'].overall_feedback if state.get('feedback_result') else 'N/A'}"
                
                # Download button
                st.download_button(
                    label="⬇️ Download Report",
                    data=report_text,
                    file_name=f"grading_report_{state.get('student_id', 'student')}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain"
                )


if __name__ == "__main__":
    main()
