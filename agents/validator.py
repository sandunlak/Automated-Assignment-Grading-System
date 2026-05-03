"""
Validator Agent

Validates the grading results for consistency, fairness, and accuracy
before finalizing the grade.
"""

import time
import json
from typing import Dict, Any, List
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from state.graph_state import GradingState, ValidationResult
from tools.validation_checker import validate_grading_consistency, compare_with_baseline
from observability.logger import AgentLogger


class ValidatorAgent:
    """
    Agent responsible for validating grading results.
    
    Responsibilities:
    - Check grading consistency across criteria
    - Detect anomalies in marking
    - Validate marks against rubric constraints
    - Provide recommendations for adjustments if needed
    - Ensure fairness and objectivity
    """
    
    def __init__(self, logger: AgentLogger):
        """
        Initialize the Validator Agent.
        
        Args:
            logger: Logger instance for tracking operations
        """
        self.logger = logger
        self.agent_name = "Validator"
        
        # Initialize local LLM
        self.llm = ChatOllama(
            model="llama3:8b",
            temperature=0.1,  # Very low temperature for consistent validation
            base_url="http://localhost:11434"
        )
        
        # Define system prompt
        self.system_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Validator Agent for an automated assignment grading system.

Your role is to audit and validate the grading results to ensure fairness, consistency, and accuracy.

VALIDATION CHECKS:
1. Range Validation: Marks are within valid ranges (0 to max)
2. Sum Validation: Total marks equal sum of criterion marks
3. Proportionality: Marks awarded are proportional to quality demonstrated
4. Consistency: Similar quality answers would receive similar marks
5. Rubric Adherence: Marking aligns with rubric criteria
6. Anomaly Detection: Identify unusually high or low scores

VALIDATION PRINCIPLES:
- Be objective and systematic
- Flag genuine inconsistencies, not minor variations
- Provide specific recommendations when issues are found
- Consider the full context of the answer and analysis

CONSTRAINTS:
- Do not re-mark the answer - only validate existing marks
- Focus on systematic errors, not subjective disagreements
- Provide clear evidence when flagging anomalies
- Be constructive in recommendations
- Validation score should reflect overall confidence (0.0-1.0)

OUTPUT FORMAT:
Provide your validation in the following JSON format:
{{
  "is_consistent": true/false,
  "consistency_score": 0.0-1.0,
  "anomalies_detected": ["anomaly1", "anomaly2", ...],
  "validation_passed": true/false,
  "recommendations": ["recommendation1", "recommendation2", ...]
}}"""),
            ("human", """Assignment Question: {question}

Analysis Summary:
- Key Concepts: {key_concepts}
- Completeness: {completeness}%
- Relevance: {relevance}%
- Clarity: {clarity}%

Marking Results:
- Total Marks: {total_marks}/{max_marks}
- Percentage: {percentage}%
- Criterion Marks: {criterion_marks}
- Justifications: {justifications}

Rubric Criteria:
{rubric}

Validation Tool Results:
{tool_validation}

Validate this grading result and identify any issues.""")
        ])
    
    def validate(self, state: GradingState) -> GradingState:
        """
        Validate the grading results and update the state.
        
        Args:
            state: Current grading state
            
        Returns:
            Updated state with validation results
        """
        start_time = time.time()
        
        try:
            # Update state
            state['processing_status'] = 'validating'
            self.logger.log_state_transition('feedback_complete', 'validating', state)
            
            # Check prerequisites
            if not state.get('marking_result'):
                raise ValueError("No marking result available for validation")
            
            if not state.get('analysis_result'):
                raise ValueError("No analysis result available for validation")
            
            analysis = state['analysis_result']
            marking = state['marking_result']
            
            # Use validation checker tool
            tool_start = time.time()
            
            # Prepare rubric weights
            rubric_weights = {c.criterion_id: c.max_marks for c in state['rubric']}
            
            tool_validation = validate_grading_consistency.invoke({
                'marks_awarded': marking.total_marks,
                'max_marks': marking.max_possible_marks,
                'analysis_scores': marking.criterion_marks,
                'rubric_weights': rubric_weights
            })
            tool_time = time.time() - tool_start
            
            self.logger.log_tool_call(
                'validate_grading_consistency',
                self.agent_name,
                {
                    'marks_awarded': marking.total_marks,
                    'max_marks': marking.max_possible_marks
                },
                tool_validation,
                tool_time
            )
            
            # Optional: Compare with baseline (if historical data available)
            # For now, we'll use a typical class average of 65% with std dev of 15%
            tool_start = time.time()
            baseline_comparison = compare_with_baseline.invoke({
                'current_score': marking.percentage,
                'baseline_average': 65.0,
                'baseline_std_dev': 15.0,
                'threshold_z_score': 2.0
            })
            tool_time = time.time() - tool_start
            
            self.logger.log_tool_call(
                'compare_with_baseline',
                self.agent_name,
                {'current_score': marking.percentage},
                baseline_comparison,
                tool_time
            )
            
            # Prepare rubric string
            rubric_str = json.dumps([
                {
                    'criterion_id': c.criterion_id,
                    'max_marks': c.max_marks,
                    'description': c.description
                }
                for c in state['rubric']
            ], indent=2)
            
            # Create the chain
            chain = self.system_prompt | self.llm
            
            # Invoke LLM
            response = chain.invoke({
                'question': state['assignment_question'],
                'key_concepts': ', '.join(analysis.key_concepts_identified),
                'completeness': analysis.completeness_score * 100,
                'relevance': analysis.relevance_score * 100,
                'clarity': analysis.clarity_score * 100,
                'total_marks': marking.total_marks,
                'max_marks': marking.max_possible_marks,
                'percentage': marking.percentage,
                'criterion_marks': json.dumps(marking.criterion_marks, indent=2),
                'justifications': json.dumps(marking.marking_justification, indent=2),
                'rubric': rubric_str,
                'tool_validation': json.dumps(tool_validation, indent=2)
            })
            
            # Parse the response
            response_text = response.content if hasattr(response, 'content') else str(response)
            validation_data = self._parse_validation_response(response_text)
            
            # Combine tool validation with LLM validation
            anomalies = validation_data.get('anomalies_detected', [])
            if 'anomalies_detected' in tool_validation:
                anomalies.extend(tool_validation['anomalies_detected'])
            
            # Determine overall validation status
            validation_passed = (
                validation_data.get('validation_passed', True) and
                tool_validation.get('validation_passed', True) and
                len(anomalies) == 0
            )
            
            # Calculate final consistency score
            consistency_score = (
                validation_data.get('consistency_score', 0.8) * 0.6 +
                tool_validation.get('consistency_score', 0.8) * 0.4
            )
            
            # Create validation result
            validation_result = ValidationResult(
                is_consistent=validation_data.get('is_consistent', True),
                consistency_score=round(consistency_score, 2),
                anomalies_detected=anomalies,
                validation_passed=validation_passed,
                recommendations=validation_data.get('recommendations', [])
            )
            
            # Update state with final grade if validation passed
            if validation_passed:
                state['final_grade'] = marking.total_marks
                state['ready_for_review'] = True
            else:
                # Flag for manual review
                state['ready_for_review'] = False
                state['error_messages'].append(
                    f"Validation failed with {len(anomalies)} anomalies - manual review recommended"
                )
            
            # Update state
            state['validation_result'] = validation_result
            
            processing_time = time.time() - start_time
            
            # Log execution
            self.logger.log_agent_execution(
                self.agent_name,
                {'marks_to_validate': marking.total_marks},
                {'validation_passed': validation_passed, 'consistency': consistency_score},
                processing_time,
                'success'
            )
            
            state['processing_status'] = 'complete'
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = f"Validator failed: {str(e)}"
            state['error_messages'].append(error_msg)
            
            self.logger.log_error(
                'AgentExecutionError',
                error_msg,
                {'agent': self.agent_name}
            )
            
            state['processing_status'] = 'validation_failed'
            state['ready_for_review'] = False
        
        return state
    
    def _parse_validation_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse the LLM response to extract structured validation data.
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            Parsed validation data
        """
        try:
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {
                    'is_consistent': True,
                    'consistency_score': 0.5,
                    'anomalies_detected': ['Failed to parse validation response'],
                    'validation_passed': False,
                    'recommendations': ['Manual review required']
                }
        except json.JSONDecodeError:
            return {
                'is_consistent': False,
                'consistency_score': 0.0,
                'anomalies_detected': ['JSON parsing failed'],
                'validation_passed': False,
                'recommendations': ['Manual review required due to parsing error']
            }
