from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

# Import your solver logic
from gss_solver import golden_section_search, create_plot

app = FastAPI(
    title="Golden Section Search API",
    description="An API to find function minima using the Golden Section Search algorithm.",
    version="1.0.0",
)

# --- CORS Configuration ---------------------------------------------------
# This allows your frontend (running on a different port) to talk to this backend.
origins = [
    "*" # Allow all origins for development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-Memory Storage ----------------------------------------------------
# A simple list to store the history of calculations for the current session.
session_history: List[Dict[str, Any]] = []


# --- Pydantic Models ------------------------------------------------------
# These models define the expected structure of the request and response data.
class SolverInput(BaseModel):
    func_str: str
    a: float
    b: float
    tol: float = 1e-4
    mode: str = 'minimize'

class SolverResult(BaseModel):
    x_min: float
    f_min: float
    iterations: list
    num_iterations: int
    plot_data: str | None

# --- API Endpoints --------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to the GSS Solver API. Visit /docs for details."}

@app.post("/api/solve", response_model=SolverResult)
def solve_function(data: SolverInput):
    """
    Receives function details, performs the Golden Section Search,
    and returns the result including a plot.
    """
    try:
        # If maximizing, we minimize the negative of the function
        func_to_solve = f"-({data.func_str})" if data.mode == 'maximize' else data.func_str

        # Perform the calculation using your existing solver function
        result = golden_section_search(
            func_str=func_to_solve,
            a=data.a,
            b=data.b,
            tol=data.tol
        )

        # Adjust f_min back if we were maximizing
        if data.mode == 'maximize':
            result['f_min'] = -result['f_min']
            for it in result['iterations']:
                it['f_x1'] = -it['f_x1']
                it['f_x2'] = -it['f_x2']

        # Generate the plot using your existing plot function
        plot_base64 = create_plot(
            func_str=data.func_str, # Use original function for plot
            bounds=(data.a, data.b),
            iterations=result['iterations'],
            x_min=result['x_min'],
            f_min=result['f_min']
        )
        
        # Prepare the response
        response_data = {
            "x_min": result['x_min'],
            "f_min": result['f_min'],
            "iterations": result['iterations'],
            "num_iterations": result['num_iterations'],
            "plot_data": plot_base64
        }

        # Add to session history
        history_entry = {**response_data, "function": data.func_str, "bounds": {"a": data.a, "b": data.b}, "mode": data.mode}
        session_history.insert(0, history_entry)

        return response_data

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Catch any other unexpected errors during computation
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/api/history", response_model=List[Dict[str, Any]])
def get_history():
    """
    Returns the list of all calculations performed in the current session.
    """
    return session_history

@app.delete("/api/history")
def clear_history():
    """
    Clears the session history.
    """
    session_history.clear()
    return {"message": "History cleared successfully."}

# --- Server Execution -----------------------------------------------------
# To run this server, execute the following command in your terminal:
# uvicorn main:app --reload
#
# Then, open your solver.html file in a browser.
if __name__ == "__main__":
    import uvicorn
    print("Starting FastAPI server...")
    print("Run with: uvicorn main:app --reload")
    print("Access the API docs at http://localhost:8000/docs")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


