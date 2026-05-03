"""
Unit Tests for Custom Tools

Tests the functionality of all custom tools used by the agents.
"""

import pytest
import os
import json
from tools.file_reader import read_assignment_file, read_rubric_file, write_feedback_file
from tools.rubric_evaluator import evaluate_answer_against_rubric, calculate_grade_boundary
from tools.feedback_template import generate_feedback_template, create_detailed_comment
from tools.validation_checker import validate_grading_consistency, compare_with_baseline


class TestFileReader:
    """Tests for file reader tools."""
    
    def test_read_assignment_file_success(self, tmp_path):
        """Test successful file reading."""
        # Create a temporary file
        test_file = tmp_path / "test_assignment.txt"
        test_file.write_text("This is a test assignment answer.")
        
        # Read the file
        result = read_assignment_file.invoke({"file_path": str(test_file)})
        
        assert "test assignment answer" in result
        assert "Error" not in result
    
    def test_read_assignment_file_not_found(self):
        """Test reading non-existent file."""
        result = read_assignment_file.invoke({"file_path": "nonexistent_file.txt"})
        
        assert "Error" in result
        assert "not found" in result
    
    def test_read_rubric_file_success(self, tmp_path):
        """Test successful rubric file reading."""
        rubric_data = {
            "rubric": [
                {
                    "criterion_id": "C1",
                    "description": "Test criterion",
                    "max_marks": 10,
                    "keywords": ["test", "example"]
                }
            ]
        }
        
        test_file = tmp_path / "test_rubric.json"
        test_file.write_text(json.dumps(rubric_data))
        
        result = read_rubric_file.invoke({"file_path": str(test_file)})
        
        assert "C1" in result
        assert "Error" not in result
    
    def test_write_feedback_file_success(self, tmp_path):
        """Test successful feedback file writing."""
        feedback_content = "This is test feedback."
        output_file = tmp_path / "feedback.txt"
        
        result = write_feedback_file.invoke({
            "file_path": str(output_file),
            "feedback_content": feedback_content
        })
        
        assert "Successfully wrote" in result
        assert output_file.exists()
        assert output_file.read_text() == feedback_content


class TestRubricEvaluator:
    """Tests for rubric evaluator tools."""
    
    def test_evaluate_answer_with_keywords(self):
        """Test evaluation with keyword matching."""
        answer = "Machine learning involves supervised and unsupervised learning algorithms."
        rubric = [
            {
                "criterion_id": "C1",
                "description": "Knowledge",
                "max_marks": 10,
                "keywords": ["machine learning", "supervised", "unsupervised"]
            }
        ]
        
        result = evaluate_answer_against_rubric.invoke({
            "answer_text": answer,
            "rubric_criteria": rubric
        })
        
        assert "criterion_scores" in result
        assert "total_score" in result
        assert result["criterion_scores"]["C1"] > 0
        assert result["keyword_matches"]["C1"]["matched_count"] == 3
    
    def test_evaluate_answer_partial_match(self):
        """Test evaluation with partial keyword match."""
        answer = "Machine learning is about algorithms."
        rubric = [
            {
                "criterion_id": "C1",
                "description": "Knowledge",
                "max_marks": 10,
                "keywords": ["machine learning", "supervised", "unsupervised", "neural networks"]
            }
        ]
        
        result = evaluate_answer_against_rubric.invoke({
            "answer_text": answer,
            "rubric_criteria": rubric
        })
        
        # Should get partial credit
        assert result["criterion_scores"]["C1"] > 0
        assert result["criterion_scores"]["C1"] < 10
        assert result["keyword_matches"]["C1"]["matched_count"] == 1
    
    def test_evaluate_answer_no_match(self):
        """Test evaluation with no keyword matches."""
        answer = "This is completely unrelated content."
        rubric = [
            {
                "criterion_id": "C1",
                "description": "Knowledge",
                "max_marks": 10,
                "keywords": ["machine learning", "supervised", "unsupervised"]
            }
        ]
        
        result = evaluate_answer_against_rubric.invoke({
            "answer_text": answer,
            "rubric_criteria": rubric
        })
        
        # Should get minimal or zero credit
        assert result["keyword_matches"]["C1"]["matched_count"] == 0
    
    def test_calculate_grade_boundary_a_plus(self):
        """Test A+ grade boundary."""
        result = calculate_grade_boundary.invoke({"percentage": 95.0})
        
        assert result["grade"] == "A+"
        assert result["passed"] is True
        assert result["gpa"] == 4.0
    
    def test_calculate_grade_boundary_pass(self):
        """Test passing grade."""
        result = calculate_grade_boundary.invoke({"percentage": 55.0})
        
        assert result["grade"] == "C+"
        assert result["passed"] is True
    
    def test_calculate_grade_boundary_fail(self):
        """Test failing grade."""
        result = calculate_grade_boundary.invoke({"percentage": 35.0})
        
        assert result["grade"] == "F"
        assert result["passed"] is False
        assert result["gpa"] == 0.0
    
    def test_calculate_grade_boundary_edge_cases(self):
        """Test edge cases for grade boundaries."""
        # Test 0%
        result = calculate_grade_boundary.invoke({"percentage": 0.0})
        assert result["grade"] == "F"
        
        # Test 100%
        result = calculate_grade_boundary.invoke({"percentage": 100.0})
        assert result["grade"] == "A+"


class TestFeedbackTemplate:
    """Tests for feedback template tools."""
    
    def test_generate_feedback_template(self):
        """Test feedback template generation."""
        result = generate_feedback_template.invoke({
            "student_name": "STU001",
            "assignment_title": "ML Assignment 1",
            "marks_awarded": 35.0,
            "max_marks": 50.0,
            "strengths": ["Good understanding of concepts", "Clear examples"],
            "weaknesses": ["Missing discussion on limitations", "Could elaborate more"],
            "recommendations": ["Review chapter 5", "Practice more examples"]
        })
        
        assert "STU001" in result
        assert "ML Assignment 1" in result
        assert "70.0%" in result
        assert "Good understanding of concepts" in result
        assert "Missing discussion on limitations" in result
    
    def test_create_detailed_comment(self):
        """Test detailed comment creation."""
        result = create_detailed_comment.invoke({
            "criterion_name": "C1_Knowledge",
            "marks_awarded": 8.0,
            "max_marks": 10.0,
            "justification": "Student demonstrated strong understanding"
        })
        
        assert "C1_Knowledge" in result
        assert "8.0/10.0" in result
        assert "80%" in result
        assert "strong understanding" in result


class TestValidationChecker:
    """Tests for validation checker tools."""
    
    def test_validate_consistent_grading(self):
        """Test validation of consistent grading."""
        result = validate_grading_consistency.invoke({
            "marks_awarded": 35.0,
            "max_marks": 50.0,
            "analysis_scores": {"C1": 8.0, "C2": 7.0, "C3": 10.0, "C4": 5.0, "C5": 5.0},
            "rubric_weights": {"C1": 10.0, "C2": 10.0, "C3": 10.0, "C4": 5.0, "C5": 5.0}
        })
        
        assert result["validation_passed"] is True
        assert result["consistency_score"] > 0.8
        assert len(result["anomalies_detected"]) == 0
    
    def test_validate_marks_exceed_maximum(self):
        """Test validation when marks exceed maximum."""
        result = validate_grading_consistency.invoke({
            "marks_awarded": 55.0,  # Exceeds max of 50
            "max_marks": 50.0,
            "analysis_scores": {"C1": 12.0, "C2": 10.0, "C3": 10.0, "C4": 5.0, "C5": 5.0},
            "rubric_weights": {"C1": 10.0, "C2": 10.0, "C3": 10.0, "C4": 5.0, "C5": 5.0}
        })
        
        assert result["validation_passed"] is False
        assert any("exceed maximum" in anomaly for anomaly in result["anomalies_detected"])
    
    def test_validate_negative_marks(self):
        """Test validation with negative marks."""
        result = validate_grading_consistency.invoke({
            "marks_awarded": -5.0,
            "max_marks": 50.0,
            "analysis_scores": {"C1": -5.0},
            "rubric_weights": {"C1": 10.0}
        })
        
        assert result["validation_passed"] is False
        assert any("negative" in anomaly.lower() for anomaly in result["anomalies_detected"])
    
    def test_validate_sum_mismatch(self):
        """Test validation when sum doesn't match."""
        result = validate_grading_consistency.invoke({
            "marks_awarded": 40.0,  # Doesn't match sum of 35
            "max_marks": 50.0,
            "analysis_scores": {"C1": 8.0, "C2": 7.0, "C3": 10.0, "C4": 5.0, "C5": 5.0},
            "rubric_weights": {"C1": 10.0, "C2": 10.0, "C3": 10.0, "C4": 5.0, "C5": 5.0}
        })
        
        assert result["validation_passed"] is False
        assert any("doesn't match" in anomaly for anomaly in result["anomalies_detected"])
    
    def test_compare_with_baseline_normal(self):
        """Test normal score comparison."""
        result = compare_with_baseline.invoke({
            "current_score": 70.0,
            "baseline_average": 65.0,
            "baseline_std_dev": 15.0
        })
        
        assert result["is_outlier"] is False
        assert abs(result["z_score"]) < 2.0
    
    def test_compare_with_baseline_outlier(self):
        """Test outlier detection."""
        result = compare_with_baseline.invoke({
            "current_score": 10.0,  # Very low
            "baseline_average": 65.0,
            "baseline_std_dev": 15.0
        })
        
        assert result["is_outlier"] is True
        assert result["z_score"] < -2.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
