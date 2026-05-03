"""
Validation Checker Tool

Validates grading consistency and detects anomalies in the assessment.
"""

from typing import Dict, List
from langchain_core.tools import tool


@tool
def validate_grading_consistency(
    marks_awarded: float,
    max_marks: float,
    analysis_scores: Dict[str, float],
    rubric_weights: Dict[str, float]
) -> Dict:
    """
    Validate that the grading is consistent and fair.
    
    Checks for:
    - Marks don't exceed maximum
    - Marks are not negative
    - Distribution across criteria is reasonable
    - No anomalous scoring patterns
    
    Args:
        marks_awarded: Total marks awarded
        max_marks: Maximum possible marks
        analysis_scores: Scores per criterion from marking
        rubric_weights: Expected weight distribution per criterion
        
    Returns:
        Validation result with consistency checks and anomalies
    """
    try:
        anomalies = []
        validation_passed = True
        
        # Check 1: Marks within valid range
        if marks_awarded < 0:
            anomalies.append("Marks awarded cannot be negative")
            validation_passed = False
        
        if marks_awarded > max_marks:
            anomalies.append(f"Marks awarded ({marks_awarded}) exceed maximum ({max_marks})")
            validation_passed = False
        
        # Check 2: Percentage calculation accuracy
        expected_percentage = (marks_awarded / max_marks * 100) if max_marks > 0 else 0
        if expected_percentage < 0 or expected_percentage > 100:
            anomalies.append("Percentage calculation is out of valid range (0-100)")
            validation_passed = False
        
        # Check 3: Criterion scores sum consistency
        total_criterion_marks = sum(analysis_scores.values())
        if abs(total_criterion_marks - marks_awarded) > 0.01:  # Allow small floating point errors
            anomalies.append(
                f"Sum of criterion marks ({total_criterion_marks}) doesn't match total awarded ({marks_awarded})"
            )
            validation_passed = False
        
        # Check 4: Individual criterion marks validation
        for criterion_id, marks in analysis_scores.items():
            if criterion_id in rubric_weights:
                max_for_criterion = rubric_weights[criterion_id]
                if marks < 0:
                    anomalies.append(f"Negative marks for criterion {criterion_id}")
                    validation_passed = False
                if marks > max_for_criterion:
                    anomalies.append(
                        f"Marks for {criterion_id} ({marks}) exceed maximum ({max_for_criterion})"
                    )
                    validation_passed = False
        
        # Check 5: Detect extreme scoring (all very high or very low)
        if len(analysis_scores) > 0:
            avg_score_per_criterion = marks_awarded / len(analysis_scores)
            avg_max_per_criterion = max_marks / len(analysis_scores)
            avg_ratio = avg_score_per_criterion / avg_max_per_criterion if avg_max_per_criterion > 0 else 0
            
            if avg_ratio > 0.95:
                anomalies.append("Warning: Extremely high scores across all criteria - may indicate lenient grading")
            elif avg_ratio < 0.15:
                anomalies.append("Warning: Extremely low scores across all criteria - may indicate harsh grading")
        
        # Calculate consistency score (1.0 = perfectly consistent)
        consistency_score = 1.0 - (len(anomalies) * 0.2)
        consistency_score = max(0.0, min(1.0, consistency_score))
        
        return {
            'validation_passed': validation_passed,
            'consistency_score': round(consistency_score, 2),
            'anomalies_detected': anomalies,
            'marks_awarded': marks_awarded,
            'max_marks': max_marks,
            'percentage': round(expected_percentage, 2)
        }
    
    except Exception as e:
        return {
            'validation_passed': False,
            'consistency_score': 0.0,
            'anomalies_detected': [f"Validation error: {str(e)}"],
            'error': str(e)
        }


@tool
def compare_with_baseline(
    current_score: float,
    baseline_average: float,
    baseline_std_dev: float,
    threshold_z_score: float = 2.0
) -> Dict:
    """
    Compare a score with historical baseline to detect outliers.
    
    Args:
        current_score: The score to validate
        baseline_average: Historical average score
        baseline_std_dev: Historical standard deviation
        threshold_z_score: Z-score threshold for anomaly detection (default: 2.0)
        
    Returns:
        Comparison result with outlier detection
    """
    try:
        if baseline_std_dev == 0:
            return {
                'is_outlier': False,
                'z_score': 0,
                'message': "No variance in baseline data"
            }
        
        # Calculate z-score
        z_score = (current_score - baseline_average) / baseline_std_dev
        
        # Check if outlier
        is_outlier = abs(z_score) > threshold_z_score
        
        message = ""
        if is_outlier:
            if z_score > 0:
                message = f"Score is significantly above average (z={z_score:.2f})"
            else:
                message = f"Score is significantly below average (z={z_score:.2f})"
        else:
            message = f"Score is within normal range (z={z_score:.2f})"
        
        return {
            'is_outlier': is_outlier,
            'z_score': round(z_score, 2),
            'current_score': current_score,
            'baseline_average': baseline_average,
            'message': message
        }
    
    except Exception as e:
        return {
            'is_outlier': False,
            'error': f"Error in baseline comparison: {str(e)}"
        }
