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
    Generates a Plotly graph of the function, search bounds, and minimum.
    
    Args:
        func_str (str): The mathematical function.
        bounds (tuple): The initial (a, b) bounds.
        iterations (list): A list of iteration dictionaries from the search.
        x_min (float): The calculated minimum x-value.
        f_min (float): The calculated minimum function value.
        
    Returns:
        str: A base64 encoded PNG image of the plot.
    """
    import matplotlib
    matplotlib.use('Agg') # Use a non-interactive backend
    import matplotlib.pyplot as plt
    import io
    import base64

    a, b = bounds
    x = symbols('x')
    expr = sympify(func_str)
    func = lambdify(x, expr, 'numpy')

    # Generate points for the function curve
    x_vals = np.linspace(a - (b-a)*0.2, b + (b-a)*0.2, 400)
    y_vals = func(x_vals)

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the function
    ax.plot(x_vals, y_vals, label=f'$f(x) = {func_str}$', color='royalblue', linewidth=2)

    # Highlight the final minimum point
    ax.plot(x_min, f_min, 'o', color='red', markersize=10, label=f'Minimum ({x_min:.4f}, {f_min:.4f})')

    # Add iteration markers
    if iterations:
        iter_x1 = [i['x1'] for i in iterations]
        iter_fx1 = [i['f_x1'] for i in iterations]
        iter_x2 = [i['x2'] for i in iterations]
        iter_fx2 = [i['f_x2'] for i in iterations]
        ax.plot(iter_x1, iter_fx1, 'x', color='darkorange', alpha=0.6, label='x1 points')
        ax.plot(iter_x2, iter_fx2, '+', color='green', alpha=0.6, label='x2 points')

    # Style the plot
    ax.set_title('Golden Section Search Visualization', fontsize=16, fontweight='bold')
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.legend(frameon=True, shadow=True)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    
    # Save plot to a memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    
    # Encode as base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    
    return image_base64
