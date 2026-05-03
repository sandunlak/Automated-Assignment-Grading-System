"""
Feedback Template Tool

Generates structured feedback for student assignments.
"""

from typing import List, Dict
from langchain_core.tools import tool


@tool
def generate_feedback_template(
    student_name: str,
    assignment_title: str,
    marks_awarded: float,
    max_marks: float,
    strengths: List[str],
    weaknesses: List[str],
    recommendations: List[str]
) -> str:
    """
    Generate a structured feedback document for a student assignment.
    
    Args:
        student_name: Name or ID of the student
        assignment_title: Title of the assignment
        marks_awarded: Marks awarded to the student
        max_marks: Maximum possible marks
        strengths: List of strengths identified
        weaknesses: List of areas needing improvement
        recommendations: List of actionable recommendations
        
    Returns:
        Formatted feedback string
    """
    try:
        percentage = (marks_awarded / max_marks * 100) if max_marks > 0 else 0
        
        feedback = f"""
{'='*60}
ASSIGNMENT FEEDBACK REPORT
{'='*60}

Student: {student_name}
Assignment: {assignment_title}
Marks Awarded: {marks_awarded}/{max_marks} ({percentage:.1f}%)

{'='*60}
OVERALL ASSESSMENT
{'='*60}

"""
        
        # Add strengths
        if strengths:
            feedback += "AREAS OF STRENGTH:\n"
            feedback += "-" * 40 + "\n"
            for i, strength in enumerate(strengths, 1):
                feedback += f"  {i}. ✓ {strength}\n"
            feedback += "\n"
        
        # Add weaknesses
        if weaknesses:
            feedback += "AREAS FOR IMPROVEMENT:\n"
            feedback += "-" * 40 + "\n"
            for i, weakness in enumerate(weaknesses, 1):
                feedback += f"  {i}. ⚠ {weakness}\n"
            feedback += "\n"
        
        # Add recommendations
        if recommendations:
            feedback += "ACTIONABLE RECOMMENDATIONS:\n"
            feedback += "-" * 40 + "\n"
            for i, rec in enumerate(recommendations, 1):
                feedback += f"  {i}. → {rec}\n"
            feedback += "\n"
        
        feedback += f"{'='*60}\n"
        feedback += "End of Feedback Report\n"
        feedback += f"{'='*60}\n"
        
        return feedback
    
    except Exception as e:
        return f"Error generating feedback template: {str(e)}"


@tool
def create_detailed_comment(
    criterion_name: str,
    marks_awarded: float,
    max_marks: float,
    justification: str
) -> str:
    """
    Create a detailed comment for a specific grading criterion.
    
    Args:
        criterion_name: Name of the criterion being assessed
        marks_awarded: Marks awarded for this criterion
        max_marks: Maximum marks for this criterion
        justification: Explanation for the marks awarded
        
    Returns:
        Formatted criterion comment
    """
    try:
        percentage = (marks_awarded / max_marks * 100) if max_marks > 0 else 0
        
        comment = f"""
Criterion: {criterion_name}
Marks: {marks_awarded}/{max_marks} ({percentage:.0f}%)
Assessment: {justification}
"""
        return comment.strip()
    
    except Exception as e:
        return f"Error creating detailed comment: {str(e)}"
