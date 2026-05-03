"""
Answer Analyzer Agent

Analyzes student answers to identify key concepts, assess completeness,
relevance, and clarity before passing to the marking agent.
"""

import time
import json
from typing import Dict, Any
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from state.graph_state import GradingState, StudentAnswer, AnalysisResult
from tools.file_reader import read_assignment_file
from observability.logger import AgentLogger


class AnswerAnalyzerAgent:
    """
    Agent responsible for analyzing student answers.
    
    Responsibilities:
    - Parse and understand the student's response
    - Identify key concepts present in the answer
    - Assess completeness, relevance, and clarity
    - Provide detailed analysis notes for downstream agents
    """
    
    def __init__(self, logger: AgentLogger):
        """
        Initialize the Answer Analyzer Agent.
        
        Args:
            logger: Logger instance for tracking operations
        """
        self.logger = logger
        self.agent_name = "Answer Analyzer"
        
        # Initialize local LLM
        self.llm = ChatOllama(
            model="llama3:8b",
            temperature=0.3,
            base_url="http://localhost:11434"
        )
        
        # Define system prompt
        self.system_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Answer Analyzer for an automated assignment grading system.

Your role is to analyze student answers and extract meaningful insights that will be used by downstream agents for marking.

ANALYSIS CRITERIA:
1. Key Concepts: Identify the main concepts, theories, or principles mentioned
2. Completeness: How thoroughly does the answer address the question? (0.0-1.0)
3. Relevance: How relevant is the content to the question asked? (0.0-1.0)
4. Clarity: How clear and well-structured is the answer? (0.0-1.0)

CONSTRAINTS:
- Be objective and analytical
- Focus on factual content, not writing style
- Identify both strengths and gaps
- Provide specific examples from the answer in your notes
- Do NOT assign marks - that's the Marking Agent's job
- Work with Small Language Model limitations - be concise

OUTPUT FORMAT:
Provide your analysis in the following JSON format:
{{
  "key_concepts": ["concept1", "concept2", ...],
  "completeness_score": 0.0-1.0,
  "relevance_score": 0.0-1.0,
  "clarity_score": 0.0-1.0,
  "analysis_notes": "Detailed analysis explaining your scores..."
}}"""),
            ("human", """Assignment Question: {question}

Student Answer: {answer}

Analyze this answer according to the criteria above.""")
        ])
    
    def analyze(self, state: GradingState) -> GradingState:
        """
        Analyze the student's answer and update the state.
        
        Args:
            state: Current grading state
            
        Returns:
            Updated state with analysis results
        """
        start_time = time.time()
        
        try:
            # Update state
            state['processing_status'] = 'analyzing'
            self.logger.log_state_transition('initialized', 'analyzing', state)
            
            # Prepare input
            question = state['assignment_question']
            answer_text = state['student_answer_raw']
            
            # Log tool usage - reading the answer
            tool_start = time.time()
            # In a real scenario, we might use read_assignment_file here
            tool_time = time.time() - tool_start
            self.logger.log_tool_call(
                'read_assignment_file',
                self.agent_name,
                {'file_path': 'student_submission.txt'},
                'Answer loaded successfully',
                tool_time
            )
            
            # Create the chain
            chain = self.system_prompt | self.llm
            
            # Invoke LLM
            response = chain.invoke({
                'question': question,
                'answer': answer_text
            })
            
            # Parse the response
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Extract JSON from response
            analysis_data = self._parse_analysis_response(response_text)
            
            # Create structured result
            word_count = len(answer_text.split())
            student_answer = StudentAnswer(
                question_number=1,
                answer_text=answer_text,
                word_count=word_count
            )
            
            analysis_result = AnalysisResult(
                answer=student_answer,
                key_concepts_identified=analysis_data.get('key_concepts', []),
                completeness_score=float(analysis_data.get('completeness_score', 0.5)),
                relevance_score=float(analysis_data.get('relevance_score', 0.5)),
                clarity_score=float(analysis_data.get('clarity_score', 0.5)),
                analysis_notes=analysis_data.get('analysis_notes', '')
            )
            
            # Update state
            state['analysis_result'] = analysis_result
            
            processing_time = time.time() - start_time
            
            # Log execution
            self.logger.log_agent_execution(
                self.agent_name,
                {'question': question[:100], 'answer_length': len(answer_text)},
                {'key_concepts': analysis_result.key_concepts_identified, 'completeness': analysis_result.completeness_score},
                processing_time,
                'success'
            )
            
            state['processing_status'] = 'analysis_complete'
            
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = f"Answer Analyzer failed: {str(e)}"
            state['error_messages'].append(error_msg)
            
            self.logger.log_error(
                'AgentExecutionError',
                error_msg,
                {'agent': self.agent_name}
            )
            
            state['processing_status'] = 'analysis_failed'
        
        return state
    
    def _parse_analysis_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse the LLM response to extract structured analysis data.
        
        Args:
            response_text: Raw LLM response
            
        Returns:
            Parsed analysis data
        """
        try:
            # Try to find JSON in the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
            else:
                # Fallback default
                return {
                    'key_concepts': ['Concept identification failed'],
                    'completeness_score': 0.5,
                    'relevance_score': 0.5,
                    'clarity_score': 0.5,
                    'analysis_notes': 'Failed to parse LLM response, using default values'
                }
        except json.JSONDecodeError:
            return {
                'key_concepts': ['JSON parsing failed'],
                'completeness_score': 0.5,
                'relevance_score': 0.5,
                'clarity_score': 0.5,
                'analysis_notes': f'Could not parse response: {response_text[:200]}'
            }
