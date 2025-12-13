"""
Golden Section Search (GSS) Optimization Solver
Author: CS Student
Description: Implements GSS algorithm using SciPy for finding function minima.
             Includes iteration tracking for visualization and analysis.
"""

import numpy as np
from scipy.optimize import minimize_scalar
import json
from datetime import datetime


class GSSolver:
    """Golden Section Search Solver with detailed iteration tracking."""
    
    def __init__(self):
        self.iterations = []
        self.result = None
        self.function_str = ""
        self.bounds = (None, None)
        self.tolerance = None
        
    def parse_function(self, func_str):
        """
        Parse and validate mathematical expression.
        Supports: +, -, *, /, **, sin, cos, tan, exp, log, sqrt, pi, e
        
        Args:
            func_str (str): Mathematical expression in terms of x
            
        Returns:
            callable: Python function object
            
        Raises:
            ValueError: If function syntax is invalid
        """
        from sympy import symbols, sympify, lambdify
        
        try:
            x = symbols('x')
            expr = sympify(func_str)
            func = lambdify(x, expr, modules=['numpy'])
            return func
        except Exception as e:
            raise ValueError(f"Invalid function: {str(e)}")
    
    def golden_section_search(self, func_str, a, b, tol=1e-4):
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
        self.function_str = func_str
        self.bounds = (a, b)
        self.tolerance = tol
        self.iterations = []
        
        # Validate bounds
        if a >= b:
            raise ValueError("Left bound must be less than right bound")
        
        # Parse function
        func = self.parse_function(func_str)
        
        # Use SciPy's minimize_scalar with GSS method
        result = minimize_scalar(
            func, 
            bounds=(a, b), 
            method='golden',
            options={'xatol': tol}
        )
        
        # Extract results
        x_min = result.x
        f_min = result.fun
        num_iterations = result.nit
        
        self.result = {
            'x_min': float(x_min),
            'f_min': float(f_min),
            'num_iterations': int(num_iterations),
            'tolerance': tol,
            'function': func_str,
            'bounds': {'a': float(a), 'b': float(b)},
            'success': result.success,
            'message': result.message if hasattr(result, 'message') else 'Success'
        }
        
        # Generate iteration details (approximate based on GSS algorithm)
        self._generate_iteration_details(func, a, b, tol)
        
        return self.result
    
    def _generate_iteration_details(self, func, a, b, tol):
        """
        Generate detailed iteration information for GSS process.
        
        Args:
            func: Compiled function
            a (float): Left bound
            b (float): Right bound
            tol (float): Tolerance
        """
        golden_ratio = 0.381966  # (3 - sqrt(5)) / 2
        iteration = 0
        
        while (b - a) > tol and iteration < 100:
            iteration += 1
            
            x1 = a + (1 - golden_ratio) * (b - a)
            x2 = a + golden_ratio * (b - a)
            
            f_x1 = float(func(x1))
            f_x2 = float(func(x2))
            
            interval_width = float(b - a)
            
            self.iterations.append({
                'iteration': iteration,
                'a': float(a),
                'b': float(b),
                'x1': float(x1),
                'x2': float(x2),
                'f_x1': f_x1,
                'f_x2': f_x2,
                'interval_width': interval_width
            })
            
            # Update bounds based on function values
            if f_x1 < f_x2:
                b = x2
            else:
                a = x1
    
    def get_iterations(self):
        """Return list of all iteration details."""
        return self.iterations
    
    def get_result(self):
        """Return final optimization result."""
        return self.result
    
    def to_dict(self):
        """Convert full results to dictionary for JSON export."""
        return {
            'timestamp': datetime.now().isoformat(),
            'function': self.function_str,
            'bounds': self.bounds,
            'tolerance': self.tolerance,
            'result': self.result,
            'iterations': self.iterations
        }


def create_plot(func_str, bounds, iterations, x_min, f_min):
    """
    Create visualization of GSS process using Matplotlib.
    Shows function curve and iteration history with visual halving.
    
    Args:
        func_str (str): Function expression
        bounds (tuple): (a, b) search bounds
        iterations (list): Iteration details
        x_min (float): Minimum point found
        f_min (float): Function value at minimum
        
    Returns:
        str: Base64 encoded PNG image
    """
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    from sympy import symbols, sympify, lambdify
    import io
    import base64
    
    try:
        # Parse function
        x = symbols('x')
        expr = sympify(func_str)
        func = lambdify(x, expr, modules=['numpy'])
        
        # Create figure
        fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
        
        # Plot function curve
        a, b = bounds
        x_vals = np.linspace(a - (b-a)*0.1, b + (b-a)*0.1, 500)
        y_vals = [func(xi) for xi in x_vals]
        
        ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
        
        # Plot iteration intervals with color gradient
        num_iters = len(iterations)
        for i, iter_data in enumerate(iterations):
            alpha = 0.1 + (i / num_iters) * 0.3
            color_intensity = i / num_iters
            
            iter_a = iter_data['a']
            iter_b = iter_data['b']
            
            # Shade interval
            ax.axvspan(iter_a, iter_b, alpha=alpha*0.5, 
                      color=cm.get_cmap('viridis')(color_intensity))
            
            # Mark x1, x2 points
            if i < min(5, num_iters):  # Show only first few for clarity
                x1 = iter_data['x1']
                x2 = iter_data['x2']
                ax.plot([x1, x2], [iter_data['f_x1'], iter_data['f_x2']], 
                       'ro', markersize=4, alpha=0.6)
        
        # Highlight minimum found
        ax.plot(x_min, f_min, 'g*', markersize=20, label=f'Minimum (x={x_min:.4f})', 
               zorder=5)
        
        # Formatting
        ax.set_xlabel('x', fontsize=12, fontweight='bold')
        ax.set_ylabel('f(x)', fontsize=12, fontweight='bold')
        ax.set_title(f'Golden Section Search: {func_str}', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=10)
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(fig)
        
        return f"data:image/png;base64,{img_base64}"
        
    except Exception as e:
        return None
