"""
Global State Management for the Assignment Grading System

This module defines the state structure that is passed between agents
in the multi-agent grading workflow.
"""

from typing import TypedDict, List, Optional, Dict, Any
from pydantic import BaseModel, Field


class StudentAnswer(BaseModel):
    """Represents a student's answer to a question"""
    question_number: int = Field(description="Question number")
    answer_text: str = Field(description="Student's answer text")
    word_count: int = Field(description="Number of words in the answer")


class RubricCriterion(BaseModel):
    """Represents a single grading criterion"""
    criterion_id: str = Field(description="Unique identifier for criterion")
    description: str = Field(description="Description of the criterion")
    max_marks: float = Field(description="Maximum marks for this criterion")
    keywords: List[str] = Field(default=[], description="Key concepts to look for")


class AnalysisResult(BaseModel):
    """Result from the Answer Analyzer Agent"""
    answer: StudentAnswer = Field(description="The analyzed answer")
    key_concepts_identified: List[str] = Field(description="Main concepts found in answer")
    completeness_score: float = Field(ge=0.0, le=1.0, description="How complete the answer is")
    relevance_score: float = Field(ge=0.0, le=1.0, description="How relevant to the question")
    clarity_score: float = Field(ge=0.0, le=1.0, description="How clear and well-structured")
    analysis_notes: str = Field(description="Detailed analysis notes")


class MarkingResult(BaseModel):
    """Result from the Marking Agent"""
    criterion_marks: Dict[str, float] = Field(description="Marks per criterion")
    total_marks: float = Field(description="Total marks awarded")
    max_possible_marks: float = Field(description="Maximum possible marks")
    percentage: float = Field(ge=0.0, le=100.0, description="Percentage score")
    marking_justification: Dict[str, str] = Field(description="Justification for marks per criterion")


class FeedbackItem(BaseModel):
    """A single feedback item"""
    category: str = Field(description="Feedback category (strengths, weaknesses, suggestions)")
    comment: str = Field(description="Feedback comment")
    priority: str = Field(description="Priority level: high, medium, low")


class FeedbackResult(BaseModel):
    """Result from the Feedback Generator Agent"""
    overall_feedback: str = Field(description="Overall summary feedback")
    specific_feedback: List[FeedbackItem] = Field(description="Detailed feedback items")
    areas_of_strength: List[str] = Field(description="What the student did well")
    areas_for_improvement: List[str] = Field(description="What needs improvement")
    actionable_recommendations: List[str] = Field(description="Specific steps to improve")


class ValidationResult(BaseModel):
    """Result from the Validator Agent"""
    is_consistent: bool = Field(description="Whether grading is consistent")
    consistency_score: float = Field(ge=0.0, le=1.0, description="Consistency measurement")
    anomalies_detected: List[str] = Field(description="Any grading anomalies")
    validation_passed: bool = Field(description="Whether validation passed")
    recommendations: List[str] = Field(description="Recommendations for grade adjustment")


class GradingState(TypedDict):
    """
    Global state passed between agents in the grading workflow
    
    This state maintains all context as data flows through:
    Answer Analyzer → Marking Agent → Feedback Generator → Validator
    """
    # Input data
    assignment_question: str
    student_answer_raw: str
    rubric: List[RubricCriterion]
    
    # Agent outputs (populated sequentially)
    analysis_result: Optional[AnalysisResult]
    marking_result: Optional[MarkingResult]
    feedback_result: Optional[FeedbackResult]
    validation_result: Optional[ValidationResult]
    
    # Metadata
    student_id: str
    assignment_id: str
    processing_status: str  # "initialized", "analyzing", "marking", "feedback", "validating", "complete"
    error_messages: List[str]
    
    # Final output
    final_grade: Optional[float]
    final_feedback: Optional[str]
    ready_for_review: bool
