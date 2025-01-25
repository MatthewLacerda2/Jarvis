from typing import Any
import sys
from io import StringIO

def execute_python_code(code: str) -> tuple[Any, str, str]:
    """
    Executes Python code provided as a string and returns the result, stdout, and stderr.
    
    The function creates a safe environment to execute the code by capturing standard
    output and standard error streams. It handles both expression evaluation and
    statement execution.
    
    Args:
        code (str): A string containing valid Python code to be executed.
        
    Returns:
        tuple[Any, str, str]: A tuple containing:
            - The result of the last expression (if any)
            - Captured stdout as a string
            - Captured stderr as a string
            
    Example:
        >>> result, stdout, stderr = execute_python_code('print("Hello"); 2 + 2')
        >>> print(result)  # 4
        >>> print(stdout)  # "Hello\n"
        >>> print(stderr)  # ""
    """
    # Save original stdout and stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    # Create string buffers for capturing output
    stdout_buffer = StringIO()
    stderr_buffer = StringIO()
    
    try:
        # Redirect output to our buffers
        sys.stdout = stdout_buffer
        sys.stderr = stderr_buffer
        
        # Execute the code and get the result
        result = eval(code, {}, {})
        
        return (
            result,
            stdout_buffer.getvalue(),
            stderr_buffer.getvalue()
        )
    except SyntaxError:
        # If eval fails, try exec for statements that don't return values
        try:
            exec(code, {}, {})
            return (
                None,
                stdout_buffer.getvalue(),
                stderr_buffer.getvalue()
            )
        except Exception as e:
            print(f"Error: {str(e)}", file=sys.stderr)
            return (
                None,
                stdout_buffer.getvalue(),
                stderr_buffer.getvalue()
            )
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return (
            None,
            stdout_buffer.getvalue(),
            stderr_buffer.getvalue()
        )
    finally:
        # Restore original stdout and stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr

def execute_python_function(function_code: str, parameters: dict[str, Any]) -> tuple[Any, str, str]:
    """
    Executes a Python function provided as a string with the given parameters and returns the result.
    
    This function creates a safe environment to execute the function by first executing the function
    definition and then calling it with the provided parameters. It captures standard output and
    standard error streams during execution.
    
    Args:
        function_code (str): A string containing a valid Python function definition.
        parameters (dict[str, Any]): A dictionary mapping parameter names to their values.
                                   Values should be primitive types (numbers, strings) or
                                   their collections (lists, tuples, dicts).
    
    Returns:
        tuple[Any, str, str]: A tuple containing:
            - The return value of the function
            - Captured stdout as a string
            - Captured stderr as a string
            
    Example:
        >>> func = '''
        ... def add_numbers(a, b):
        ...     print(f"Adding {a} and {b}")
        ...     return a + b
        ... '''
        >>> result, stdout, stderr = execute_python_function(func, {'a': 5, 'b': 3})
        >>> print(result)  # 8
        >>> print(stdout)  # "Adding 5 and 3\n"
        >>> print(stderr)  # ""
    """
    # Save original stdout and stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    
    # Create string buffers for capturing output
    stdout_buffer = StringIO()
    stderr_buffer = StringIO()
    
    try:
        # Redirect output to our buffers
        sys.stdout = stdout_buffer
        sys.stderr = stderr_buffer
        
        # Create a new dictionary for local scope
        local_scope = {}
        
        # Execute the function definition
        exec(function_code, {}, local_scope)
        
        # Get the function name (assuming it's the first function defined in the code)
        function_name = next(name for name, obj in local_scope.items() 
                           if callable(obj) and not name.startswith('__'))
        
        # Get the function object
        function = local_scope[function_name]
        
        # Call the function with parameters
        result = function(**parameters)
        
        return (
            result,
            stdout_buffer.getvalue(),
            stderr_buffer.getvalue()
        )
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return (
            None,
            stdout_buffer.getvalue(),
            stderr_buffer.getvalue()
        )
    finally:
        # Restore original stdout and stderr
        sys.stdout = old_stdout
        sys.stderr = old_stderr

