
import numpy as np
from sympy import symbols, sympify, lambdify
import matplotlib.pyplot as plt
import io
import base64

# Configure Matplotlib for headless environments
plt.switch_backend('Agg')

def golden_section_search(func_str, a, b, tol=1e-4):
    """
    Perform Golden Section Search optimization.
    
    Args:
        func_str (str): Function expression as a string.
        a (float): Left bound of the interval.
        b (float): Right bound of the interval.
        tol (float): Tolerance for the stopping criterion.
        
    Returns:
        dict: A dictionary containing the results, including the minimum point,
              function value at the minimum, and iteration details.
    """
    golden_ratio = (3 - np.sqrt(5)) / 2  # Approximately 0.381966
    iterations = []
    k = 0
    
    if a >= b:
        raise ValueError("Invalid bounds: Left bound 'a' must be less than right bound 'b'.")
    
    try:
        x = symbols('x')
        expr = sympify(func_str)
        func = lambdify(x, expr, modules=['numpy'])
    except Exception as e:
        raise ValueError(f"Invalid function string: {str(e)}")
    

    x1 = a + golden_ratio * (b - a)
    x2 = b - golden_ratio * (b - a)
    f_x1 = float(func(x1))
    f_x2 = float(func(x2))

    # Check initial points for domain errors
    if np.isnan(f_x1) or np.isinf(f_x1):
        raise ValueError(f"Function evaluation resulted in NaN or Inf at x = {x1}")
    if np.isnan(f_x2) or np.isinf(f_x2):
        raise ValueError(f"Function evaluation resulted in NaN or Inf at x = {x2}")

    max_iter = 100
    while (b - a) > tol and k < max_iter:
        iterations.append({
            'k': k, 'a': float(a), 'b': float(b),
            'x1': float(x1), 'x2': float(x2),
            'f_x1': f_x1, 'f_x2': f_x2,
            'interval': float(b - a)
        })

        k += 1

        if f_x1 < f_x2:
            b = x2
            x2 = x1
            f_x2 = f_x1
            x1 = a + golden_ratio * (b - a)
            f_x1 = float(func(x1))
            if np.isnan(f_x1) or np.isinf(f_x1):
                raise ValueError(f"Function evaluation resulted in NaN or Inf at x = {x1}")
        else:
            a = x1
            x1 = x2
            f_x1 = f_x2
            x2 = b - golden_ratio * (b - a)
            f_x2 = float(func(x2))
            if np.isnan(f_x2) or np.isinf(f_x2):
                raise ValueError(f"Function evaluation resulted in NaN or Inf at x = {x2}")

    x_min = (a + b) / 2
    f_min = float(func(x_min))
    if np.isnan(f_min) or np.isinf(f_min):
        raise ValueError(f"Function evaluation resulted in NaN or Inf at x = {x_min}")

    result = {
        'x_min': float(x_min),
        'f_min': f_min,
        'iterations': iterations,
        'num_iterations': len(iterations)
    }
    if k >= max_iter:
        result['warning'] = f"Maximum iteration limit ({max_iter}) reached before tolerance was met. Result may be less accurate."
    return result


def create_plot(func_str, bounds, iterations, x_min, f_min):
    """
    Generates a plot of the function, search interval, and minimum point.
    
    Args:
        func_str (str): The function expression.
        bounds (tuple): The initial (a, b) search bounds.
        iterations (list): A list of dictionaries with iteration data.
        x_min (float): The calculated x-coordinate of the minimum.
        f_min (float): The calculated function value at the minimum.
        
    Returns:
        str: A base64 encoded string of the plot image.
    """
    try:
        x = symbols('x')
        expr = sympify(func_str)
        func = lambdify(x, expr, 'numpy')
    except Exception as e:
        raise ValueError(f"Invalid function for plotting: {str(e)}")

    a, b = bounds
    x_vals = np.linspace(a - 0.1 * (b - a), b + 0.1 * (b - a), 400)
    y_vals = func(x_vals)
    # Filter out nan/inf for plotting
    valid = ~(np.isnan(y_vals) | np.isinf(y_vals))
    x_plot = x_vals[valid]
    y_plot = y_vals[valid]

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the function
    ax.plot(x_plot, y_plot, label=f'f(x) = ${func_str}$', color='royalblue', linewidth=2)

    # Highlight the final minimum point
    ax.plot(x_min, f_min, 'ro', markersize=8, label=f'Minimum ({x_min:.4f}, {f_min:.4f})')

    # Show initial search bounds
    ax.axvline(x=a, color='gray', linestyle='--', label=f'Initial Bounds [{a}, {b}]')
    ax.axvline(x=b, color='gray', linestyle='--')

    # Style the plot
    ax.set_title('Golden Section Search Visualization', fontsize=16)
    ax.set_xlabel('x', fontsize=12)
    ax.set_ylabel('f(x)', fontsize=12)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.legend()
    plt.tight_layout()

    # Save plot to a memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Encode image to base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return image_base64