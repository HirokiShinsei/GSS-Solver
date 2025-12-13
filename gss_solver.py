"""
Golden Section Search (GSS) Optimization Solver
Author: CS Student
Description: Implements GSS algorithm for finding function minima.
             Optimized for browser execution via Pyodide.
"""

import numpy as np
from sympy import symbols, sympify, lambdify


def golden_section_search(func_str, a, b, tol=1e-4):
    """
    Perform Golden Section Search optimization.
    
    Args:
        func_str (str): Function expression as string
        a (float): Left bound
        b (float): Right bound
        tol (float): Tolerance for convergence
        
    Returns:
        dict: Results with minimum point, function value, iterations
    """
    golden_ratio = 0.381966  # (3 - sqrt(5)) / 2
    iterations = []
    k = 0
    
    # Validate bounds
    if a >= b:
        raise ValueError("Left bound must be less than right bound")
    
    # Parse function using SymPy
    try:
        x = symbols('x')
        expr = sympify(func_str)
        func = lambdify(x, expr, modules=['numpy'])
    except Exception as e:
        raise ValueError(f"Invalid function: {str(e)}")
    
    # Golden Section Search algorithm
    original_a, original_b = a, b
    
    while (b - a) > tol and k < 100:
        k += 1
        
        x1 = a + (1 - golden_ratio) * (b - a)
        x2 = a + golden_ratio * (b - a)
        
        f_x1 = float(func(x1))
        f_x2 = float(func(x2))
        
        iterations.append({
            'k': k,
            'a': float(a),
            'b': float(b),
            'x1': float(x1),
            'x2': float(x2),
            'f_x1': f_x1,
            'f_x2': f_x2,
            'interval': float(b - a)
        })
        
        # Update bounds based on function values
        if f_x1 < f_x2:
            b = x2
        else:
            a = x1
    
    # Calculate final minimum
    x_min = (a + b) / 2
    f_min = float(func(x_min))
    
    return {
        'x_min': float(x_min),
        'f_min': f_min,
        'iterations': iterations,
        'num_iterations': k,
        'tolerance': tol,
        'function': func_str,
        'bounds': {'a': float(original_a), 'b': float(original_b)},
        'success': True
    }


def evaluate_function(func_str, x_values):
    """
    Evaluate function at given x values for plotting.
    
    Args:
        func_str (str): Function expression
        x_values (list): List of x values
        
    Returns:
        list: Corresponding y values
    """
    try:
        x = symbols('x')
        expr = sympify(func_str)
        func = lambdify(x, expr, modules=['numpy'])
        
        y_values = [float(func(xi)) for xi in x_values]
        return y_values
    except Exception as e:
        raise ValueError(f"Function evaluation failed: {str(e)}")