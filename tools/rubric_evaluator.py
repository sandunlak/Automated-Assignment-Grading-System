"""
Rubric Evaluator Tool

Evaluates student answers against marking criteria and rubrics.
"""

from typing import List, Dict
from langchain_core.tools import tool
from state.graph_state import RubricCriterion


@tool
def evaluate_answer_against_rubric(
    answer_text: str,
    rubric_criteria: List[Dict]
) -> Dict:
    """
    Evaluate a student's answer against provided rubric criteria.
    
    This tool performs keyword matching and completeness analysis
    to determine how well an answer meets each criterion.
    
    Args:
        answer_text: The student's answer text to evaluate
        rubric_criteria: List of rubric criteria, each containing:
            - criterion_id: Unique identifier
            - description: What the criterion assesses
            - max_marks: Maximum marks for this criterion
            - keywords: Key concepts to look for (list of strings)
            
    Returns:
        Dictionary containing:
            - criterion_scores: Dict mapping criterion_id to awarded marks
            - total_score: Sum of all criterion marks
            - max_possible: Maximum possible marks
            - percentage: Score as percentage
            - keyword_matches: Dict showing which keywords were found
    """
    try:
        criterion_scores = {}
        keyword_matches = {}
        total_score = 0.0
        max_possible = 0.0
        
        # Convert answer to lowercase for matching
        answer_lower = answer_text.lower()
        
        for criterion in rubric_criteria:
            criterion_id = criterion.get('criterion_id', '')
            max_marks = float(criterion.get('max_marks', 0))
            keywords = criterion.get('keywords', [])
            
            max_possible += max_marks
            
            # Count keyword matches
            matched_keywords = []
            for keyword in keywords:
                if keyword.lower() in answer_lower:
                    matched_keywords.append(keyword)
            
            keyword_matches[criterion_id] = {
                'found': matched_keywords,
                'total_keywords': len(keywords),
                'matched_count': len(matched_keywords)
            }
            
            # Calculate score based on keyword coverage
            if len(keywords) > 0:
                coverage_ratio = len(matched_keywords) / len(keywords)
                # Apply some intelligence: not just keyword counting
                # Consider if answer is substantial (has enough content)
                word_count = len(answer_text.split())
                content_factor = min(1.0, word_count / 50.0)  # Expect at least 50 words
                
                # Weighted score: 70% keyword match, 30% content depth
                score_ratio = (0.7 * coverage_ratio) + (0.3 * content_factor)
                awarded_marks = min(max_marks, max_marks * score_ratio)
            else:
                # If no keywords specified, give partial credit based on content
                word_count = len(answer_text.split())
                content_factor = min(1.0, word_count / 100.0)
                awarded_marks = max_marks * content_factor * 0.5
            
            criterion_scores[criterion_id] = round(awarded_marks, 2)
            total_score += awarded_marks
        
        percentage = (total_score / max_possible * 100) if max_possible > 0 else 0
        
        return {
            'criterion_scores': criterion_scores,
            'total_score': round(total_score, 2),
            'max_possible': round(max_possible, 2),
            'percentage': round(percentage, 2),
            'keyword_matches': keyword_matches
        }
    
    except Exception as e:
        return {
            'error': f"Error evaluating answer: {str(e)}",
            'criterion_scores': {},
            'total_score': 0,
            'max_possible': 0,
            'percentage': 0
        }


@tool
def calculate_grade_boundary(percentage: float) -> Dict:
    """
    Determine the grade boundary based on percentage score.
    
    Args:
        percentage: Score percentage (0-100)
        
    Returns:
        Dictionary with grade letter, description, and GPA equivalent
    """
    try:
        percentage = float(percentage)
        
        if percentage >= 90:
            grade = 'A+'
            description = 'Outstanding'
            gpa = 4.0
        elif percentage >= 80:
            grade = 'A'
            description = 'Excellent'
            gpa = 4.0
        elif percentage >= 75:
            grade = 'A-'
            description = 'Very Good'
            gpa = 3.7
        elif percentage >= 70:
            grade = 'B+'
            description = 'Good'
            gpa = 3.3
        elif percentage >= 65:
            grade = 'B'
            description = 'Above Average'
            gpa = 3.0
        elif percentage >= 60:
            grade = 'B-'
            description = 'Average'
            gpa = 2.7
        elif percentage >= 55:
            grade = 'C+'
            description = 'Satisfactory'
            gpa = 2.3
        elif percentage >= 50:
            grade = 'C'
            description = 'Pass'
            gpa = 2.0
        elif percentage >= 45:
            grade = 'C-'
            description = 'Weak Pass'
            gpa = 1.7
        elif percentage >= 40:
            grade = 'D'
            description = 'Marginal Fail'
            gpa = 1.0
        else:
            grade = 'F'
            description = 'Fail'
            gpa = 0.0
        
        return {
            'percentage': percentage,
            'grade': grade,
            'description': description,
            'gpa': gpa,
            'passed': percentage >= 50
        }
    
    except Exception as e:
        return {
            'error': f"Error calculating grade: {str(e)}",
            'grade': 'F',
            'passed': False
        }
