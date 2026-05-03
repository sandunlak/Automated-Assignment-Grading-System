"""
Feedback Generator Agent

Creates constructive, actionable feedback for students based on
the marking results and answer analysis.
"""

import time
import json
from typing import Dict, Any, List
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from state.graph_state import GradingState, FeedbackResult, FeedbackItem
from tools.feedback_template import generate_feedback_template, create_detailed_comment
from observability.logger import AgentLogger


class FeedbackGeneratorAgent:
    """
    Agent responsible for generating constructive feedback.
    
    Responsibilities:
    - Create overall summary feedback
    - Identify specific strengths and weaknesses
    - Provide actionable recommendations for improvement
    - Generate structured, professional feedback reports
    """
    
    def __init__(self, logger: AgentLogger):
        """
        Initialize the Feedback Generator Agent.
        
        Args:
            logger: Logger instance for tracking operations
        """
        self.logger = logger
        self.agent_name = "Feedback Generator"
        
        # Initialize local LLM
        self.llm = ChatOllama(
            model="llama3:8b",
            temperature=0.4,  # Slightly higher for more natural feedback
            base_url="http://localhost:11434"
        )
        
        # Define system prompt
        self.system_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Feedback Generator for an automated assignment grading system.

Your role is to create constructive, specific, and actionable feedback that helps students improve.

FEEDBACK PRINCIPLES:
1. Specific: Reference actual content from the student's answer
2. Constructive: Focus on how to improve, not just what's wrong
3. Balanced: Acknowledge strengths while addressing weaknesses
4. Actionable: Provide clear steps the student can take
5. Encouraging: Maintain a supportive, professional tone

FEEDBACK STRUCTURE:
- Overall Summary: High-level assessment of the answer
- Strengths: What the student did well (be specific)
- Areas for Improvement: What needs work (be constructive)
- Recommendations: Actionable steps to improve

CONSTRAINTS:
- Reference specific parts of the answer when possible
- Avoid generic feedback like "good effort"
- Don't mention marks/grades in feedback - focus on learning
- Keep feedback professional and encouraging
- Prioritize the most important improvements
- Limit to 3-5 strengths and 3-5 areas for improvement

OUTPUT FORMAT:
Provide your feedback in the following JSON format:
{{
  "overall_feedback": "Summary paragraph...",
  "areas_of_strength": ["strength1", "strength2", ...],
  "areas_for_improvement": ["weakness1", "weakness2", ...],
  "actionable_recommendations": ["recommendation1", "recommendation2", ...],
  "specific_feedback": [
    {{
      "category": "strengths|weaknesses|suggestions",
      "comment": "Detailed comment...",
      "priority": "high|medium|low"
    }}
  ]
}}"""),
            ("human", """Assignment Question: {question}

Student Answer:
{answer}

Analysis Results:
- Key Concepts: {key_concepts}
- Completeness: {completeness}%
- Relevance: {relevance}%
- Clarity: {clarity}%

Marking Results:
- Total Marks: {total_marks}/{max_marks}
- Percentage: {percentage}%
- Criterion Justifications: {justifications}

Generate constructive feedback for this student.""")
        ])
    
    def generate_feedback(self, state: GradingState) -> GradingState:
        """
        Generate feedback for the student and update the state.
        
        Args:
            state: Current grading state
            
        Returns:
            Updated state with feedback results
        """
        start_time = time.time()
        
        try:
            # Update state
            state['processing_status'] = 'feedback'
            self.logger.log_state_transition('marking_complete', 'feedback', state)
            
            # Check prerequisites
            if not state.get('marking_result'):
                raise ValueError("No marking result available - Marking Agent must run first")
            
            if not state.get('analysis_result'):
                raise ValueError("No analysis result available - Answer Analyzer must run first")
            
            analysis = state['analysis_result']
            marking = state['marking_result']
            
            # Prepare justifications string
            justifications_str = json.dumps(marking.marking_justification, indent=2)
            
            # Create the chain
            chain = self.system_prompt | self.llm
            
            # Invoke LLM
            response = chain.invoke({
                'question': state['assignment_question'],
                'answer': analysis.answer.answer_text,
                'key_concepts': ', '.join(analysis.key_concepts_identified),
                'completeness': analysis.completeness_score * 100,
                'relevance': analysis.relevance_score * 100,
                'clarity': analysis.clarity_score * 100,
                'total_marks': marking.total_marks,
                'max_marks': marking.max_possible_marks,
                'percentage': marking.percentage,
                'justifications': justifications_str
            })
            
            # Parse the response
            response_text = response.content if hasattr(response, 'content') else str(response)
            feedback_data = self._parse_feedback_response(response_text)
            
            # Create structured feedback items
            specific_feedback = []
            for item in feedback_data.get('specific_feedback', []):
                feedback_item = FeedbackItem(
                    category=item.get('category', 'suggestions'),
                    comment=item.get('comment', ''),
                    priority=item.get('priority', 'medium')
                )
                specific_feedback.append(feedback_item)
            
            # Create feedback result
            feedback_result = FeedbackResult(
                overall_feedback=feedback_data.get('overall_feedback', ''),
                specific_feedback=specific_feedback,
                areas_of_strength=feedback_data.get('areas_of_strength', []),
                areas_for_improvement=feedback_data.get('areas_for_improvement', []),
                actionable_recommendations=feedback_data.get('actionable_recommendations', [])
            )
            
            # Use feedback template tool
            tool_start = time.time()
            formatted_feedback = generate_feedback_template.invoke({
                'student_name': state['student_id'],
                'assignment_title': state['assignment_id'],
                'marks_awarded': marking.total_marks,
                'max_marks': marking.max_possible_marks,
                'strengths': feedback_result.areas_of_strength,
                'weaknesses': feedback_result.areas_for_improvement,
                'recommendations': feedback_result.actionable_recommendations
            })
            tool_time = time.time() - tool_start
            
            self.logger.log_tool_call(
                'generate_feedback_template',
                self.agent_name,
                {'student_id': state['student_id']},
                'Feedback template generated',
                tool_time
            )
            
            # Create detailed comments for each criterion
            tool_start = time.time()
            criterion_comments = []
            for criterion_id, marks in marking.criterion_marks.items():
                max_for_criterion = next(
                    (c.max_marks for c in state['rubric'] if c.criterion_id == criterion_id),
                    0
                )
                justification = marking.marking_justification.get(criterion_id, '')
                
                comment = create_detailed_comment.invoke({
                    'criterion_name': criterion_id,
                    'marks_awarded': marks,
                    'max_marks': max_for_criterion,
                    'justification': justification
                })
                criterion_comments.append(comment)
            tool_time = time.time() - tool_start
            
            self.logger.log_tool_call(
                'create_detailed_comment',
                self.agent_name,
                {'num_criteria': len(marking.criterion_marks)},
                f'Generated {len(criterion_comments)} criterion comments',
                tool_time
            )
            
            # Update state
            state['feedback_result'] = feedback_result
            
            processing_time = time.time() - start_time
            
            # Log execution
            self.logger.log_agent_execution(
                self.agent_name,
                {'marks': marking.total_marks},
                {'strengths_count': len(feedback_result.areas_of_strength), 
                 'recommendations_count': len(feedback_result.actionable_recommendations)},
                processing_time,
                'success'
            )
            
            state['processing_status'] = 'feedback_complete'
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = f"Feedback Generator failed: {str(e)}"
            state['error_messages'].append(error_msg)
            
            self.logger.log_error(
                'AgentExecutionError',
                error_msg,
                {'agent': self.agent_name}
            )
            
            state['processing_status'] = 'feedback_failed'
        
        return state
    
    def _parse_feedback_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse the LLM response to extract structured feedback data.
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            Parsed feedback data
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
                    'overall_feedback': 'Feedback generation failed',
                    'areas_of_strength': [],
                    'areas_for_improvement': [],
                    'actionable_recommendations': [],
                    'specific_feedback': []
                }
        except json.JSONDecodeError:
            return {
                'overall_feedback': 'Could not parse feedback response',
                'areas_of_strength': [],
                'areas_for_improvement': [],
                'actionable_recommendations': [],
                'specific_feedback': []
            }
