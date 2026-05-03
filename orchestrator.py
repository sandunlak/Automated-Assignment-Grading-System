"""
LangGraph Orchestration Framework

Defines the workflow graph that orchestrates the multi-agent grading system.
"""

from langgraph.graph import StateGraph, END
from state.graph_state import GradingState
from agents.answer_analyzer import AnswerAnalyzerAgent
from agents.marking_agent import MarkingAgent
from agents.feedback_generator import FeedbackGeneratorAgent
from agents.validator import ValidatorAgent
from observability.logger import AgentLogger


class GradingWorkflow:
    """
    Orchestrates the multi-agent grading workflow using LangGraph.
    
    Workflow:
    1. Answer Analyzer → 2. Marking Agent → 3. Feedback Generator → 4. Validator
    """
    
    def __init__(self):
        """Initialize the grading workflow with all agents."""
        self.logger = AgentLogger(log_dir="logs")
        
        # Initialize agents
        self.answer_analyzer = AnswerAnalyzerAgent(self.logger)
        self.marking_agent = MarkingAgent(self.logger)
        self.feedback_generator = FeedbackGeneratorAgent(self.logger)
        self.validator = ValidatorAgent(self.logger)
        
        # Build the graph
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow graph.
        
        Returns:
            Compiled LangGraph workflow
        """
        # Create the graph with state
        workflow = StateGraph(GradingState)
        
        # Add nodes (agents)
        workflow.add_node("analyze", self._run_answer_analyzer)
        workflow.add_node("mark", self._run_marking_agent)
        workflow.add_node("feedback", self._run_feedback_generator)
        workflow.add_node("validate", self._run_validator)
        
        # Define the workflow sequence
        workflow.set_entry_point("analyze")
        workflow.add_edge("analyze", "mark")
        workflow.add_edge("mark", "feedback")
        workflow.add_edge("feedback", "validate")
        workflow.add_edge("validate", END)
        
        # Compile the graph
        return workflow.compile()
    
    def _run_answer_analyzer(self, state: GradingState) -> dict:
        """
        Run the Answer Analyzer agent.
        
        Args:
            state: Current grading state
            
        Returns:
            Updated state
        """
        print("\n" + "="*60)
        print("🔍 STEP 1: Answer Analysis")
        print("="*60)
        return self.answer_analyzer.analyze(state)
    
    def _run_marking_agent(self, state: GradingState) -> dict:
        """
        Run the Marking Agent.
        
        Args:
            state: Current grading state
            
        Returns:
            Updated state
        """
        print("\n" + "="*60)
        print("📝 STEP 2: Marking")
        print("="*60)
        return self.marking_agent.mark(state)
    
    def _run_feedback_generator(self, state: GradingState) -> dict:
        """
        Run the Feedback Generator agent.
        
        Args:
            state: Current grading state
            
        Returns:
            Updated state
        """
        print("\n" + "="*60)
        print("💬 STEP 3: Feedback Generation")
        print("="*60)
        return self.feedback_generator.generate_feedback(state)
    
    def _run_validator(self, state: GradingState) -> dict:
        """
        Run the Validator agent.
        
        Args:
            state: Current grading state
            
        Returns:
            Updated state
        """
        print("\n" + "="*60)
        print("✅ STEP 4: Validation")
        print("="*60)
        return self.validator.validate(state)
    
    def execute(self, initial_state: GradingState) -> GradingState:
        """
        Execute the complete grading workflow.
        
        Args:
            initial_state: Initial state with assignment data
            
        Returns:
            Final state with grading results
        """
        print("\n" + "="*60)
        print("🚀 STARTING AUTOMATED ASSIGNMENT GRADING")
        print("="*60)
        print(f"Student ID: {initial_state['student_id']}")
        print(f"Assignment ID: {initial_state['assignment_id']}")
        print(f"Status: {initial_state['processing_status']}")
        print("="*60)
        
        # Log initial state
        self.logger.log_state_transition('start', 'initialized', initial_state)
        
        try:
            # Execute the workflow
            final_state = self.graph.invoke(initial_state)
            
            # Log final results
            summary = {
                'final_grade': final_state.get('final_grade'),
                'validation_passed': final_state.get('validation_result').validation_passed 
                    if final_state.get('validation_result') else False,
                'status': final_state.get('processing_status'),
                'errors': len(final_state.get('error_messages', []))
            }
            
            self.logger.finalize_session(summary)
            
            return final_state
            
        except Exception as e:
            error_msg = f"Workflow execution failed: {str(e)}"
            print(f"\n❌ {error_msg}")
            
            self.logger.log_error('WorkflowError', error_msg)
            self.logger.finalize_session({
                'status': 'failed',
                'error': error_msg
            })
            
            raise
