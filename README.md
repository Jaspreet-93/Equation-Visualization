# Equation Visualizer & Solver

A GUI application built with Python using **SymPy**, **Matplotlib**, and **Tkinter** to parse, visualize, and solve mathematical equations interactively.

## Features

- **Safe Parser**: Uses SymPy's local context to parse only valid mathematical functions and variables safely.
- **Plot Graph**: Generates and embeds interactive plots using Matplotlib within the Tkinter GUI.
- **Solve Roots**: Finds algebraic roots for $f(x) = 0$ in the real/complex domains.
- **Derivative Calculation**: Automatically calculates the symbolic derivative $f'(x)$.
- **Turning Points**: Identifies critical points and determines maximum/minimum values of functions.

## Project Structure

```text
.
├── .gitignore
├── README.md
└── app/
    ├── m1_math_engine.py      # Core parser and solver engine
    ├── m2_plot.py             # Plotting utilities
    └── app/
        ├── m3_calculus.py     # Calculus utilities (derivatives, integration)
        └── app/
            ├── m4_optimization.py  # Local extrema / turning points
            └── app/
                ├── m5_steps.py     # Step-by-step resolution representation
                └── smart_eq_app.py # Tkinter GUI main entry point
```

## Requirements

Ensure you have Python 3.8+ installed, then install the dependencies:

```bash
pip install sympy matplotlib numpy
```

## How to Run

To start the interactive GUI application, execute:

```bash
python app/app/app/app/smart_eq_app.py
```
