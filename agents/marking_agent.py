"""
Marking Agent

Evaluates student answers against rubrics and assigns marks based on
the analysis provided by the Answer Analyzer.
"""

import time
import json
from typing import Dict, Any
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from state.graph_state import GradingState, MarkingResult
from tools.rubric_evaluator import evaluate_answer_against_rubric, calculate_grade_boundary
from observability.logger import AgentLogger


class MarkingAgent:
    """
    Agent responsible for marking student assignments.
    
    Responsibilities:
    - Evaluate answers against provided rubric criteria
    - Assign marks for each criterion
    - Provide justification for marks awarded
    - Calculate total score and percentage
    """
    
    def __init__(self, logger: AgentLogger):
        """
        Initialize the Marking Agent.
        
        Args:
            logger: Logger instance for tracking operations
        """
        self.logger = logger
        self.agent_name = "Marking Agent"
        
        # Initialize local LLM
        self.llm = ChatOllama(
            model="llama3:8b",
            temperature=0.2,  # Lower temperature for more consistent marking
            base_url="http://localhost:11434"
        )
        
        # Define system prompt
        self.system_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Marking Agent for an automated assignment grading system.

Your role is to evaluate student answers against a rubric and assign fair, consistent marks.

MARKING PRINCIPLES:
1. Fairness: Apply the rubric consistently and objectively
2. Justification: Provide clear reasoning for each mark awarded
3. Proportionality: Marks should reflect the quality and completeness of the answer
4. Constructive: Focus on what the student demonstrated, not just what's missing

RUBRIC EVALUATION:
- For each criterion, evaluate how well the answer meets the requirements
- Consider keyword matches, conceptual understanding, and depth of explanation
- Award partial marks when appropriate
- Never exceed the maximum marks for any criterion

CONSTRAINTS:
- Base marks on the rubric, not personal opinion
- Provide specific justification for EACH criterion
- Use the analysis provided by the Answer Analyzer
- Be precise with calculations
- Total marks must equal sum of criterion marks

OUTPUT FORMAT:
Provide your marking in the following JSON format:
{{
  "criterion_marks": {{
    "criterion_id_1": marks_awarded,
    "criterion_id_2": marks_awarded
  }},
  "total_marks": total_awarded,
  "max_possible_marks": maximum_possible,
  "percentage": percentage_score,
  "marking_justification": {{
    "criterion_id_1": "Justification for marks...",
    "criterion_id_2": "Justification for marks..."
  }}
}}"""),
            ("human", """Assignment Question: {question}

Student Answer Analysis:
- Key Concepts Identified: {key_concepts}
- Completeness Score: {completeness}
- Relevance Score: {relevance}
- Clarity Score: {clarity}
- Analysis Notes: {analysis_notes}

Rubric Criteria:
{rubric}

Student's Full Answer:
{answer}

Evaluate this answer against the rubric and provide marks with justifications.""")
        ])
    
    def mark(self, state: GradingState) -> GradingState:
        """
        Mark the student's answer and update the state.
        
        Args:
            state: Current grading state
            
        Returns:
            Updated state with marking results
        """
        start_time = time.time()
        
        try:
            # Update state
            state['processing_status'] = 'marking'
            self.logger.log_state_transition('analysis_complete', 'marking', state)
            
            # Get analysis results
            if not state.get('analysis_result'):
                raise ValueError("No analysis result available - Answer Analyzer must run first")
            
            analysis = state['analysis_result']
            
            # Use rubric evaluator tool first
            tool_start = time.time()
            rubric_dict = []
            for criterion in state['rubric']:
                rubric_dict.append({
                    'criterion_id': criterion.criterion_id,
                    'description': criterion.description,
                    'max_marks': criterion.max_marks,
                    'keywords': criterion.keywords
                })
            
            evaluation_result = evaluate_answer_against_rubric.invoke({
                'answer_text': analysis.answer.answer_text,
                'rubric_criteria': rubric_dict
            })
            tool_time = time.time() - tool_start
            
            self.logger.log_tool_call(
                'evaluate_answer_against_rubric',
                self.agent_name,
                {'num_criteria': len(rubric_dict)},
                evaluation_result,
                tool_time
            )
            
            # Prepare rubric string for LLM
            rubric_str = json.dumps(rubric_dict, indent=2)
            
            # Create the chain
            chain = self.system_prompt | self.llm
            
            # Invoke LLM
            response = chain.invoke({
                'question': state['assignment_question'],
                'key_concepts': ', '.join(analysis.key_concepts_identified),
                'completeness': analysis.completeness_score,
                'relevance': analysis.relevance_score,
                'clarity': analysis.clarity_score,
                'analysis_notes': analysis.analysis_notes,
                'rubric': rubric_str,
                'answer': analysis.answer.answer_text
            })
            
            # Parse the response
            response_text = response.content if hasattr(response, 'content') else str(response)
            marking_data = self._parse_marking_response(response_text)
            
            # Use tool results to validate/enhance LLM output
            if 'criterion_scores' in evaluation_result:
                # Blend tool evaluation (40%) with LLM evaluation (60%)
                blended_marks = {}
                for criterion_id in marking_data.get('criterion_marks', {}).keys():
                    llm_marks = marking_data['criterion_marks'].get(criterion_id, 0)
                    tool_marks = evaluation_result['criterion_scores'].get(criterion_id, 0)
                    blended_marks[criterion_id] = round(0.6 * llm_marks + 0.4 * tool_marks, 2)
                
                marking_data['criterion_marks'] = blended_marks
                marking_data['total_marks'] = round(sum(blended_marks.values()), 2)
                
                max_possible = sum(c.max_marks for c in state['rubric'])
                marking_data['max_possible_marks'] = max_possible
                marking_data['percentage'] = round(
                    (marking_data['total_marks'] / max_possible * 100) if max_possible > 0 else 0, 2
                )
            
            # Create structured result
            marking_result = MarkingResult(
                criterion_marks=marking_data.get('criterion_marks', {}),
                total_marks=marking_data.get('total_marks', 0),
                max_possible_marks=marking_data.get('max_possible_marks', 0),
                percentage=marking_data.get('percentage', 0),
                marking_justification=marking_data.get('marking_justification', {})
            )
            
            # Use grade boundary tool
            tool_start = time.time()
            grade_info = calculate_grade_boundary.invoke({
                'percentage': marking_result.percentage
            })
            tool_time = time.time() - tool_start
            
            self.logger.log_tool_call(
                'calculate_grade_boundary',
                self.agent_name,
                {'percentage': marking_result.percentage},
                grade_info,
                tool_time
            )
            
            # Update state
            state['marking_result'] = marking_result
            
            processing_time = time.time() - start_time
            
            # Log execution
            self.logger.log_agent_execution(
                self.agent_name,
                {'rubric_criteria': len(state['rubric'])},
                {'total_marks': marking_result.total_marks, 'percentage': marking_result.percentage},
                processing_time,
                'success'
            )
            
            state['processing_status'] = 'marking_complete'
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = f"Marking Agent failed: {str(e)}"
            state['error_messages'].append(error_msg)
            
            self.logger.log_error(
                'AgentExecutionError',
                error_msg,
                {'agent': self.agent_name}
            )
            
            state['processing_status'] = 'marking_failed'
        
        return state
    
    def _parse_marking_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse the LLM response to extract structured marking data.
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            Parsed marking data
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
                    'criterion_marks': {},
                    'total_marks': 0,
                    'max_possible_marks': 0,
                    'percentage': 0,
                    'marking_justification': {}
                }
        except json.JSONDecodeError:
            return {
                'criterion_marks': {},
                'total_marks': 0,
                'max_possible_marks': 0,
                'percentage': 0,
                'marking_justification': {'error': 'Failed to parse marking response'}
            }
