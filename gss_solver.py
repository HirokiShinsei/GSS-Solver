"""
Golden Section Search (GSS) Optimization Solver
Author: CS Student
Description: Implements GSS algorithm for finding function minima.
             Includes plotting and detailed iteration tracking.
"""

import numpy as np
from sympy import symbols, sympify, lambdify
import matplotlib.pyplot as plt
import io
import base64

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
    golden_ratio = (3 - np.sqrt(5)) / 2
    iterations = []
    k = 0
    
    # Validate bounds
    if a >= b:
        raise ValueError("Left bound must be less than right bound")
    
    # Parse function using SymPy
    try:
        x = symbols('x')
        # Replace common latex symbols for compatibility
        processed_str = func_str.replace('\\', '').replace('^', '**')
        expr = sympify(processed_str)
        func = lambdify(x, expr, modules=['numpy'])
    except Exception as e:
        raise ValueError(f"Invalid function syntax: {str(e)}")
    
    # Golden Section Search algorithm
    original_a, original_b = a, b
    
    x1 = a + golden_ratio * (b - a)
    x2 = b - golden_ratio * (b - a)
    f_x1 = float(func(x1))
    f_x2 = float(func(x2))
    
    while (b - a) > tol and k < 100:
        k += 1
        
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
        
        if f_x1 < f_x2:
            b = x2
            x2 = x1
            f_x2 = f_x1
            x1 = a + golden_ratio * (b - a)
            f_x1 = float(func(x1))
        else:
            a = x1
            x1 = x2
            f_x1 = f_x2
            x2 = b - golden_ratio * (b - a)
            f_x2 = float(func(x2))
            
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


def create_plot(func_str, bounds, iterations, x_min, f_min):
    """
    Create visualization of GSS process using Matplotlib.
    
    Args:
        func_str (str): Function expression
        bounds (tuple): (a, b) search bounds
        iterations (list): Iteration details
        x_min (float): Minimum point found
        f_min (float): Function value at minimum
        
    Returns:
        str: Base64 encoded PNG image or None if plotting fails
    """
    try:
        x = symbols('x')
        processed_str = func_str.replace('\\', '').replace('^', '**')
        expr = sympify(processed_str)
        func = lambdify(x, expr, modules=['numpy'])
        
        a, b = bounds
        # Widen the plot range slightly for better visualization
        plot_a = a - (b - a) * 0.15
        plot_b = b + (b - a) * 0.15
        x_vals = np.linspace(plot_a, plot_b, 400)
        y_vals = func(x_vals)

        # Create figure with a transparent background
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        # Plot function curve
        ax.plot(x_vals, y_vals, color='#3b82f6', linewidth=2, label='f(x)')
        
        # Highlight minimum point
        ax.plot(x_min, f_min, 'o', color='#10b981', markersize=10, label=f'Minimum ({x_min:.4f}, {f_min:.4f})')
        
        # Style the plot
        ax.set_xlabel('x', fontsize=12, color='white')
        ax.set_ylabel('f(x)', fontsize=12, color='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_color('none')
        ax.spines['right'].set_color('none')
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='#ffffff', alpha=0.2)
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.1, transparent=True)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{img_base64}"
        
    except Exception:
        # If plotting fails for any reason, return None
        return None
