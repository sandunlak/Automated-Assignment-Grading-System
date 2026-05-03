"""
Main Entry Point for Automated Assignment Grading System

This script demonstrates the complete multi-agent grading workflow.
"""

import json
from pathlib import Path
from typing import List
from state.graph_state import GradingState, RubricCriterion
from orchestrator import GradingWorkflow
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


def load_rubric(rubric_path: str) -> List[RubricCriterion]:
    """
    Load rubric from JSON file.
    
    Args:
        rubric_path: Path to rubric JSON file
        
    Returns:
        List of RubricCriterion objects
    """
    with open(rubric_path, 'r', encoding='utf-8') as f:
        rubric_data = json.load(f)
    
    criteria = []
    for item in rubric_data['rubric']:
        criterion = RubricCriterion(
            criterion_id=item['criterion_id'],
            description=item['description'],
            max_marks=item['max_marks'],
            keywords=item.get('keywords', [])
        )
        criteria.append(criterion)
    
    return criteria


def load_assignment(assignment_path: str) -> tuple:
    """
    Load assignment question and student answer from file.
    
    Args:
        assignment_path: Path to assignment file
        
    Returns:
        Tuple of (question, student_answer)
    """
    with open(assignment_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the file (assuming format: Question: ... \n\n Student Answer: ...)
    parts = content.split('Student Answer:')
    question = parts[0].replace('Question:', '').strip()
    student_answer = parts[1].strip() if len(parts) > 1 else ""
    
    return question, student_answer


def display_results(state: GradingState, console: Console):
    """
    Display grading results in a formatted way.
    
    Args:
        state: Final grading state
        console: Rich console instance
    """
    console.print("\n")
    console.print(Panel.fit("🎓 GRADING RESULTS", style="bold blue"))
    console.print("\n")
    
    # Display final grade
    if state.get('final_grade') is not None:
        marking = state['marking_result']
        validation = state['validation_result']
        
        # Grade table
        grade_table = Table(title="Final Grade Summary")
        grade_table.add_column("Metric", style="cyan")
        grade_table.add_column("Value", style="green")
        
        grade_table.add_row("Student ID", state['student_id'])
        grade_table.add_row("Assignment ID", state['assignment_id'])
        grade_table.add_row("Total Marks", f"{marking.total_marks}/{marking.max_possible_marks}")
        grade_table.add_row("Percentage", f"{marking.percentage}%")
        grade_table.add_row("Validation Status", "✅ PASSED" if validation.validation_passed else "⚠️ FAILED")
        grade_table.add_row("Consistency Score", f"{validation.consistency_score:.2f}")
        
        console.print(grade_table)
        console.print("\n")
        
        # Criterion breakdown
        if marking.criterion_marks:
            criterion_table = Table(title="Criterion Breakdown")
            criterion_table.add_column("Criterion", style="cyan")
            criterion_table.add_column("Marks", style="green")
            criterion_table.add_column("Justification", style="yellow")
            
            for criterion_id, marks in marking.criterion_marks.items():
                max_marks = next(
                    (c.max_marks for c in state['rubric'] if c.criterion_id == criterion_id),
                    0
                )
                justification = marking.marking_justification.get(criterion_id, 'N/A')[:80] + "..."
                criterion_table.add_row(
                    criterion_id,
                    f"{marks}/{max_marks}",
                    justification
                )
            
            console.print(criterion_table)
            console.print("\n")
        
        # Display feedback
        if state.get('feedback_result'):
            feedback = state['feedback_result']
            
            console.print(Panel.fit("📝 Feedback Summary", style="bold magenta"))
            console.print(f"\n{feedback.overall_feedback}\n")
            
            if feedback.areas_of_strength:
                console.print("\n✅ Areas of Strength:", style="green")
                for strength in feedback.areas_of_strength:
                    console.print(f"  • {strength}")
            
            if feedback.areas_for_improvement:
                console.print("\n⚠️  Areas for Improvement:", style="yellow")
                for weakness in feedback.areas_for_improvement:
                    console.print(f"  • {weakness}")
            
            if feedback.actionable_recommendations:
                console.print("\n💡 Recommendations:", style="cyan")
                for rec in feedback.actionable_recommendations:
                    console.print(f"  → {rec}")
            
            console.print("\n")
        
        # Display validation results
        if state.get('validation_result'):
            validation = state['validation_result']
            
            if validation.anomalies_detected:
                console.print(Panel.fit("⚠️ Validation Anomalies", style="bold yellow"))
                for anomaly in validation.anomalies_detected:
                    console.print(f"  ⚠️  {anomaly}")
                console.print("\n")
            
            if validation.recommendations:
                console.print(Panel.fit("🔧 Validation Recommendations", style="bold cyan"))
                for rec in validation.recommendations:
                    console.print(f"  → {rec}")
                console.print("\n")
    
    # Display errors if any
    if state.get('error_messages'):
        console.print(Panel.fit("❌ Errors", style="bold red"))
        for error in state['error_messages']:
            console.print(f"  ❌ {error}")
        console.print("\n")


def main():
    """Main execution function."""
    console = Console()
    
    console.print("\n")
    console.print(Panel.fit(
        "🤖 Automated Assignment Grading System\nMulti-Agent AI Powered Grading",
        style="bold green"
    ))
    console.print("\n")
    
    # File paths
    rubric_path = "data/sample_rubric.json"
    assignment_path = "data/sample_assignment.txt"
    
    # Load data
    console.print("[cyan]📂 Loading assignment data...[/cyan]")
    rubric = load_rubric(rubric_path)
    question, student_answer = load_assignment(assignment_path)
    
    console.print(f"[green]✓ Loaded {len(rubric)} rubric criteria[/green]")
    console.print(f"[green]✓ Loaded assignment question and student answer[/green]\n")
    
    # Create initial state
    initial_state = GradingState(
        assignment_question=question,
        student_answer_raw=student_answer,
        rubric=rubric,
        analysis_result=None,
        marking_result=None,
        feedback_result=None,
        validation_result=None,
        student_id="STU2024001",
        assignment_id="ML_ASSIGNMENT_01",
        processing_status="initialized",
        error_messages=[],
        final_grade=None,
        final_feedback=None,
        ready_for_review=False
    )
    
    # Execute workflow
    workflow = GradingWorkflow()
    final_state = workflow.execute(initial_state)
    
    # Display results
    display_results(final_state, console)
    
    # Summary
    console.print(Panel.fit(
        "✅ Grading Complete!\nCheck 'logs/' directory for detailed execution logs.",
        style="bold green"
    ))
    console.print("\n")


if __name__ == "__main__":
    main()
