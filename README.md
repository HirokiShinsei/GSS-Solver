# Golden Section Search Solver (GSS-Solver)

## Overview

Golden Section Search Solver (GSS-Solver) is a web-based tool and API for finding the minimum (or maximum) of single-variable functions using the Golden Section Search algorithm. It features a modern, interactive frontend and a robust FastAPI backend, with support for mathematical input, visualization, and session history. The project is containerized with Docker for easy deployment.

---

## Features

- **Modern UI**: Responsive, glassmorphism-styled frontend with Tailwind CSS and Plotly.js for interactive plots.
- **Math Input**: Live math rendering with MathQuill and quick-insert function buttons.
- **Golden Section Search**: Accurate, step-by-step minimization/maximization of user-defined functions.
- **Visualization**: Dynamic plotting of the function and search process.
- **Session History**: View and clear previous calculations in the current session.
- **REST API**: FastAPI backend with endpoints for solving, history, and clearing history.
- **Dockerized**: Easily run the entire stack in a container.

---

## Project Structure

```
├── about-us.html         # About page (frontend)
├── Dockerfile            # Docker container definition
├── gss_solver.py         # Core Golden Section Search logic
├── index.html            # Landing page (frontend)
├── main.py               # FastAPI backend
├── README.md             # Project documentation
├── requirements.txt      # Python dependencies
├── solver.html           # Main solver UI (frontend)
├── assets/               # Static assets (logo, images, etc.)
├── backup-rollbacks/     # HTML backups
└── __pycache__/          # Python bytecode (ignored)
```

---

## Quick Start

### 1. Prerequisites

- Python 3.11+
- pip
- (Optional) Docker

### 2. Local Development

#### Install dependencies

```bash
pip install -r requirements.txt
```

#### Run the FastAPI backend

```bash
uvicorn main:app --reload
# The API will be available at http://127.0.0.1:8000
# Interactive docs: http://127.0.0.1:8000/docs
```

#### Open the Frontend

Open `solver.html` in your browser (double-click or use a local web server for best results).

#### (Optional) Run with Gunicorn (for production)

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:7860
```

---

## Docker Usage

### Build the Docker image

```bash
docker build -t gss-solver .
```

### Run the container

```bash
docker run -p 7860:7860 gss-solver
# The API will be available at http://localhost:7860
```

---

## API Endpoints

### `POST /api/solve`

Solve a function using Golden Section Search.

**Request Body:**

```
{
	"func_str": "x**2 + 3*x + 2",   // Function as a string (use 'x' as variable)
	"a": -5,                        // Left bound
	"b": 5,                         // Right bound
	"tol": 0.0001,                  // Tolerance (optional, default 1e-4)
	"mode": "minimize"             // 'minimize' or 'maximize' (optional)
}
```

**Response:**

```
{
	"x_min": -1.4999,
	"f_min": -0.2500,
	"iterations": [ ... ],
	"num_iterations": 20,
	"plot_data": {
		"x": [...],
		"y": [...]
	}
}
```

### `GET /api/history`

Returns the session's calculation history.

### `DELETE /api/history`

Clears the session's calculation history.

---

## Frontend Usage

Open `solver.html` in your browser. Enter a function (e.g., `x**2 + 3*x + 2`), set bounds and tolerance, and click **Solve**. The result, plot, and iteration table will appear. Use the mode toggle to switch between minimization and maximization.

**Supported Math Syntax:**
- Use `x` as the variable.
- Standard Python math syntax: `x**2`, `sin(x)`, `exp(x)`, etc.
- See the in-app guide for more examples.

---

## Technologies Used

- **Backend:** FastAPI, Uvicorn, Gunicorn, NumPy, SymPy, Matplotlib
- **Frontend:** HTML, Tailwind CSS, Plotly.js, MathQuill, JavaScript
- **Containerization:** Docker

---

## Customization & Extending

- To add new features, edit `main.py` (API/backend) or `solver.html` (frontend UI/logic).
- The core algorithm is in `gss_solver.py`.
- For branding, update assets in the `assets/` folder and favicon links in HTML files.

---

## Credits

- Developed by [Your Name/Team].
- Uses open-source libraries: FastAPI, Uvicorn, Gunicorn, NumPy, SymPy, Matplotlib, Plotly.js, MathQuill, Tailwind CSS.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.