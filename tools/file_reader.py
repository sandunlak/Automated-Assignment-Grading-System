"""
File Reader Tool

Provides functionality to read assignment submissions and rubrics from local files.
"""

import os
from typing import Optional
from langchain_core.tools import tool


@tool
def read_assignment_file(file_path: str) -> str:
    """
    Read the content of an assignment submission file.
    
    Args:
        file_path: Path to the assignment file (relative or absolute)
        
    Returns:
        The content of the file as a string
        
    Raises:
        FileNotFoundError: If the file does not exist
        PermissionError: If the file cannot be read
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return f"Error: File not found at path: {file_path}"
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return content
    
    except PermissionError:
        return f"Error: Permission denied to read file: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


@tool
def read_rubric_file(file_path: str) -> str:
    """
    Read the content of a rubric/marking scheme file.
    
    Args:
        file_path: Path to the rubric file (JSON or text format)
        
    Returns:
        The content of the rubric file as a string
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: Rubric file not found at path: {file_path}"
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return content
    
    except Exception as e:
        return f"Error reading rubric file: {str(e)}"


@tool
def write_feedback_file(file_path: str, feedback_content: str) -> str:
    """
    Write grading feedback to a file.
    
    Args:
        file_path: Path where feedback should be saved
        feedback_content: The feedback content to write
        
    Returns:
        Success message or error description
    """
    try:
        # Ensure directory exists
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        # Write feedback
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(feedback_content)
        
        return f"Successfully wrote feedback to: {file_path}"
    
    except Exception as e:
        return f"Error writing feedback file: {str(e)}"
