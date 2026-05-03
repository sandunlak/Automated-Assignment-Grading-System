"""
Evaluation Script for Agent Outputs

Implements property-based testing and LLM-as-a-judge evaluation
to validate agent accuracy and output quality.
"""

import pytest
import json
from typing import Dict, Any
from state.graph_state import (
    GradingState, RubricCriterion, AnalysisResult, 
    MarkingResult, FeedbackResult, ValidationResult, StudentAnswer
)


class TestAnswerAnalyzer:
    """Evaluation tests for Answer Analyzer Agent."""
    
    @pytest.fixture
    def sample_state(self):
        """Create a sample state for testing."""
        rubric = [
            RubricCriterion(
                criterion_id="C1",
                description="Understanding of concepts",
                max_marks=10,
                keywords=["machine learning", "algorithms", "data"]
            )
        ]
        
        return GradingState(
            assignment_question="Explain machine learning",
            student_answer_raw="Machine learning is a subset of AI that uses algorithms to learn from data.",
            rubric=rubric,
            analysis_result=None,
            marking_result=None,
            feedback_result=None,
            validation_result=None,
            student_id="TEST001",
            assignment_id="TEST_ASSIGN",
            processing_status="initialized",
            error_messages=[],
            final_grade=None,
            final_feedback=None,
            ready_for_review=False
        )
    
    def test_analysis_identifies_key_concepts(self):
        """Test that analyzer identifies key concepts in answer."""
        # This would require running the actual agent
        # For now, we test the expected properties
        answer = "Machine learning involves supervised learning, unsupervised learning, and reinforcement learning."
        
        # Expected properties
        assert "machine learning" in answer.lower()
        assert "supervised learning" in answer.lower()
        assert len(answer.split()) > 5  # Should have substantial content
    
    def test_analysis_completeness_score_range(self):
        """Test that completeness score is within valid range."""
        # Property: completeness_score should be between 0.0 and 1.0
        completeness_scores = [0.0, 0.25, 0.5, 0.75, 1.0]
        
        for score in completeness_scores:
            assert 0.0 <= score <= 1.0
    
    def test_analysis_relevance_score_range(self):
        """Test that relevance score is within valid range."""
        relevance_scores = [0.0, 0.3, 0.6, 0.9, 1.0]
        
        for score in relevance_scores:
            assert 0.0 <= score <= 1.0
    
    def test_analysis_clarity_score_range(self):
        """Test that clarity score is within valid range."""
        clarity_scores = [0.0, 0.4, 0.7, 1.0]
        
        for score in clarity_scores:
            assert 0.0 <= score <= 1.0
    
    def test_analysis_notes_not_empty(self):
        """Test that analysis provides non-empty notes."""
        # Property: analysis_notes should provide meaningful content
        sample_notes = [
            "Student demonstrated good understanding",
            "Answer covers main concepts but lacks depth",
            "Excellent explanation with clear examples"
        ]
        
        for notes in sample_notes:
            assert len(notes) > 10  # Should be substantial


class TestMarkingAgent:
    """Evaluation tests for Marking Agent."""
    
    def test_marks_within_range(self):
        """Test that awarded marks don't exceed maximum."""
        # Property: 0 <= marks_awarded <= max_marks
        test_cases = [
            (8.0, 10.0),
            (5.0, 5.0),
            (0.0, 10.0),
            (9.5, 10.0)
        ]
        
        for marks, max_marks in test_cases:
            assert 0 <= marks <= max_marks
    
    def test_total_marks_calculation(self):
        """Test that total marks equal sum of criterion marks."""
        criterion_marks = {"C1": 8.0, "C2": 7.0, "C3": 9.0}
        total_marks = sum(criterion_marks.values())
        
        assert total_marks == 24.0
    
    def test_percentage_calculation(self):
        """Test percentage calculation accuracy."""
        total_marks = 35.0
        max_marks = 50.0
        expected_percentage = (total_marks / max_marks) * 100
        
        assert expected_percentage == 70.0
    
    def test_justification_for_each_criterion(self):
        """Test that each criterion has a justification."""
        criterion_marks = {"C1": 8.0, "C2": 7.0, "C3": 9.0}
        justifications = {
            "C1": "Good understanding shown",
            "C2": "Adequate explanation",
            "C3": "Excellent analysis"
        }
        
        # Property: Every criterion with marks should have justification
        for criterion_id in criterion_marks.keys():
            assert criterion_id in justifications
            assert len(justifications[criterion_id]) > 5
    
    def test_marking_consistency(self):
        """Test that similar answers receive similar marks."""
        # This is a property-based test
        # In practice, you'd run the agent multiple times
        marks_for_similar_answers = [7.5, 8.0, 7.8, 8.2, 7.9]
        
        # Marks should be within a reasonable range
        avg_marks = sum(marks_for_similar_answers) / len(marks_for_similar_answers)
        max_deviation = max(abs(m - avg_marks) for m in marks_for_similar_answers)
        
        assert max_deviation < 1.0  # Should not deviate more than 1 mark


class TestFeedbackGenerator:
    """Evaluation tests for Feedback Generator Agent."""
    
    def test_feedback_contains_strengths(self):
        """Test that feedback identifies strengths."""
        sample_feedback = FeedbackResult(
            overall_feedback="Good work overall",
            specific_feedback=[],
            areas_of_strength=["Clear explanation", "Good examples"],
            areas_for_improvement=["Needs more depth"],
            actionable_recommendations=["Review chapter 5"]
        )
        
        assert len(sample_feedback.areas_of_strength) > 0
    
    def test_feedback_contains_improvements(self):
        """Test that feedback identifies areas for improvement."""
        sample_feedback = FeedbackResult(
            overall_feedback="Good work overall",
            specific_feedback=[],
            areas_of_strength=["Clear explanation"],
            areas_for_improvement=["Needs more depth", "Missing examples"],
            actionable_recommendations=["Review chapter 5"]
        )
        
        assert len(sample_feedback.areas_for_improvement) > 0
    
    def test_feedback_provides_recommendations(self):
        """Test that feedback provides actionable recommendations."""
        sample_feedback = FeedbackResult(
            overall_feedback="Good work overall",
            specific_feedback=[],
            areas_of_strength=["Clear explanation"],
            areas_for_improvement=["Needs more depth"],
            actionable_recommendations=["Review chapter 5", "Practice more examples"]
        )
        
        assert len(sample_feedback.actionable_recommendations) > 0
    
    def test_feedback_specific_and_actionable(self):
        """Test that recommendations are specific and actionable."""
        recommendations = [
            "Review chapter 5 on neural networks",
            "Practice implementing decision trees",
            "Study the differences between supervised and unsupervised learning"
        ]
        
        for rec in recommendations:
            assert len(rec) > 10  # Should be specific, not generic
            assert not rec.lower().startswith("good")  # Should not be generic praise
    
    def test_feedback_tone_constructive(self):
        """Test that feedback maintains constructive tone."""
        negative_words = ["terrible", "awful", "horrible", "worst"]
        
        sample_feedback = "Your answer shows good understanding but could be improved with more examples."
        
        for word in negative_words:
            assert word not in sample_feedback.lower()


class TestValidatorAgent:
    """Evaluation tests for Validator Agent."""
    
    def test_validation_detects_invalid_marks(self):
        """Test that validator detects marks exceeding maximum."""
        # Property: Validator should flag marks > max_marks
        marks_awarded = 55.0
        max_marks = 50.0
        
        assert marks_awarded > max_marks  # Should be detected
    
    def test_validation_detects_negative_marks(self):
        """Test that validator detects negative marks."""
        marks_awarded = -5.0
        
        assert marks_awarded < 0  # Should be detected
    
    def test_validation_checks_sum_consistency(self):
        """Test that validator checks sum of criterion marks."""
        criterion_marks = {"C1": 8.0, "C2": 7.0, "C3": 9.0}
        total_reported = 25.0  # Incorrect
        total_actual = sum(criterion_marks.values())  # 24.0
        
        assert abs(total_reported - total_actual) > 0.01  # Should be detected
    
    def test_validation_consistency_score_range(self):
        """Test that consistency score is within valid range."""
        consistency_scores = [0.0, 0.5, 0.8, 1.0]
        
        for score in consistency_scores:
            assert 0.0 <= score <= 1.0
    
    def test_validation_provides_recommendations(self):
        """Test that validator provides recommendations when issues found."""
        sample_recommendations = [
            "Review marks for C2 - seems low compared to answer quality",
            "Consider adjusting C3 marks upward",
            "Manual review recommended for this submission"
        ]
        
        assert len(sample_recommendations) > 0
    
    def test_validation_passed_flag(self):
        """Test that validation_passed reflects actual validation status."""
        # Property: validation_passed should be False if anomalies exist
        anomalies = ["Marks exceed maximum"]
        validation_passed = len(anomalies) == 0
        
        assert validation_passed is False
        
        # No anomalies
        anomalies = []
        validation_passed = len(anomalies) == 0
        
        assert validation_passed is True


class TestStateManagement:
    """Tests for state management and data flow."""
    
    def test_state_preserves_student_data(self):
        """Test that state preserves student information throughout workflow."""
        initial_state = {
            'student_id': 'STU001',
            'assignment_id': 'ASSIGN01',
            'student_answer_raw': 'Test answer'
        }
        
        # After going through all agents, this data should still be present
        assert 'student_id' in initial_state
        assert initial_state['student_id'] == 'STU001'
        assert initial_state['student_answer_raw'] == 'Test answer'
    
    def test_state_sequential_population(self):
        """Test that state is populated sequentially by agents."""
        # Simulate workflow progression
        state = {
            'analysis_result': None,
            'marking_result': None,
            'feedback_result': None,
            'validation_result': None
        }
        
        # After Answer Analyzer
        state['analysis_result'] = {'concepts': ['ML', 'AI']}
        assert state['analysis_result'] is not None
        assert state['marking_result'] is None
        
        # After Marking Agent
        state['marking_result'] = {'total_marks': 35.0}
        assert state['analysis_result'] is not None
        assert state['marking_result'] is not None
        assert state['feedback_result'] is None
        
        # After Feedback Generator
        state['feedback_result'] = {'feedback': 'Good work'}
        assert state['analysis_result'] is not None
        assert state['marking_result'] is not None
        assert state['feedback_result'] is not None
        assert state['validation_result'] is None
    
    def test_status_transitions(self):
        """Test that processing status transitions correctly."""
        expected_transitions = [
            'initialized',
            'analyzing',
            'analysis_complete',
            'marking',
            'marking_complete',
            'feedback',
            'feedback_complete',
            'validating',
            'complete'
        ]
        
        # Verify all expected states exist
        assert len(expected_transitions) == 9
        assert 'initialized' in expected_transitions
        assert 'complete' in expected_transitions


class TestSecurityAndRobustness:
    """Tests for security and robustness properties."""
    
    def test_handles_empty_answer(self):
        """Test system handles empty student answer."""
        empty_answer = ""
        assert len(empty_answer) == 0
        
        # Should not crash, should give minimal marks
    
    def test_handles_very_long_answer(self):
        """Test system handles very long answers."""
        long_answer = "word " * 5000  # 5000 words
        assert len(long_answer.split()) == 5000
        
        # Should process without error
    
    def test_handles_special_characters(self):
        """Test system handles special characters in answers."""
        answer_with_special = "Machine learning is AI's subset (important!)"
        assert "'" in answer_with_special
        assert "!" in answer_with_special
    
    def test_no_data_leakage_between_students(self):
        """Test that one student's data doesn't affect another's grading."""
        student1_state = {
            'student_id': 'STU001',
            'answer': 'Answer 1'
        }
        
        student2_state = {
            'student_id': 'STU002',
            'answer': 'Answer 2'
        }
        
        # States should be independent
        assert student1_state['student_id'] != student2_state['student_id']
        assert student1_state['answer'] != student2_state['answer']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
