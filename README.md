# Smart Equation Visualizer & Solver

A robust, interactive desktop application built with Python using **Tkinter**, **SymPy**, and **Matplotlib**. The project serves as an educational and mathematical utility to parse, visualize, analyze, and solve algebraic equations step-by-step.

---

## 🗺️ Project Execution Flowchart

The following diagram represents the core execution flow of the application:

```mermaid
flowchart TD
    A([Start Application]) --> B[Tkinter GUI Window Launched]
    B --> C{User Action}
    
    C -->|Input Equation & Click 'Plot Graph'| D[Parse Expr safely with SymPy local dict]
    D --> E[Convert Expr to NumPy function via lambdify]
    E --> F[Generate x-axis interval & evaluate points safely]
    F --> G[Render plot inside Tkinter embedded Matplotlib canvas]
    
    C -->|Input Equation & Click 'Solve Roots'| H[Parse Expr safely with SymPy]
    H --> I[Solve equation f\(x\) = 0 algebraically]
    I --> J[Display list of Roots in popup messagebox]
    
    C -->|Input Equation & Click 'Derivative'| K[Parse Expr safely with SymPy]
    K --> L[Calculate symbolic derivative f'\(x\) via diff]
    L --> M[Display f'\(x\) derivative expression in popup]
    
    C -->|Input Equation & Click 'Max/Min'| N[Parse Expr safely with SymPy]
    N --> O[Calculate derivative f'\(x\) & solve f'\(x\) = 0]
    O --> P[Substitute critical points back to f\(x\) to find turning coordinate pairs]
    P --> Q[Display Critical Points in popup messagebox]
    
    G --> R([Wait for Next Interaction])
    J --> R
    M --> R
    Q --> R
```

---

## 🚀 Working & Execution Flow

1. **Safety First (Expression Parsing)**:
   - To prevent execution of arbitrary/malicious code (e.g. `eval` exploits), the application processes user-input equations via custom local dictionaries.
   - SymPy's `sympify` is restricted to an allowlist containing variable `x` and standard math functions (`sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, `Abs`).

2. **Visualizing the Graph**:
   - The expression is converted to a fast-evaluating NumPy function using `lambdify`.
   - Domain errors (like dividing by zero or taking the square root of negative numbers at certain points) are handled gracefully on a point-by-point basis using try-catch blocks to prevent application crashes and display clean graphs.

3. **Symbolic Solving & Optimization**:
   - Roots are solved algebraically using SymPy’s exact solver.
   - Derivatives are calculated symbolically using the `diff` method.
   - Optimization points (turning points) are found by calculating $f'(x)$, solving for $f'(x) = 0$ to get critical inputs, and then substituting these values back into $f(x)$ to obtain coordinate pairs.

---

## 🛠️ Technology Stack

- **Python 3.8+**: Core programming language.
- **Tkinter**: Standard GUI library for modern-feeling widget layout.
- **SymPy**: Computer Algebra System (CAS) for symbolic math, differentiation, equation solving, and formula formatting.
- **Matplotlib**: Plotting and rendering engine, integrated directly into Tkinter frames using a `FigureCanvasTkAgg` canvas backend.
- **NumPy**: Fast vectorized numerical computations for smooth multi-point plotting.

---

## 📂 Codebase Modules & Architecture

The application is structured into modular layers that build upon each other:

| Module File | Relative Path | Purpose & Functionality |
| :--- | :--- | :--- |
| **Math Engine** | [`app/m1_math_engine.py`](file:///d:/PROJECTS/equation%20visulaization/app/m1_math_engine.py) | Safely parses strings and computes real roots algebraically. |
| **Plotter** | [`app/m2_plot.py`](file:///d:/PROJECTS/equation%20visulaization/app/m2_plot.py) | Renders standard, standalone Matplotlib graph windows of the expression. |
| **Calculus Engine** | [`app/app/m3_calculus.py`](file:///d:/PROJECTS/equation%20visulaization/app/app/m3_calculus.py) | Finds real roots and computes/plots tangent lines at a user-specified tangent point $x_0$. |
| **Optimizer** | [`app/app/app/m4_optimization.py`](file:///d:/PROJECTS/equation%20visulaization/app/app/app/m4_optimization.py) | Dedicated safe-plotting functionality for mathematical optimization. |
| **Step Explainer** | [`app/app/app/app/m5_steps.py`](file:///d:/PROJECTS/equation%20visulaization/app/app/app/app/m5_steps.py) | Generates step-by-step explanations for solving polynomial roots and derivatives. |
| **Main UI Entry** | [`app/app/app/app/smart_eq_app.py`](file:///d:/PROJECTS/equation%20visulaization/app/app/app/app/smart_eq_app.py) | Combines all features into an interactive Tkinter graphical interface. |

---

## 💻 Setup & Commands

Follow these steps to set up and run the application on your local system:

### 1. Prerequisites
Ensure you have Python 3.8 or above installed on your machine. You can verify your python version by running:
```bash
python --version
```

### 2. Install Dependencies
Run the following command to install the required libraries:
```bash
pip install sympy matplotlib numpy
```

### 3. Run the GUI Application
To run the primary Tkinter application:
```bash
python app/app/app/app/smart_eq_app.py
```

### 4. Run Individual Modules (Optional CLI Testing)
Each module contains a CLI testing harness when executed directly. For example:

- To test the **Math Parser & Solver** CLI:
  ```bash
  python app/m1_math_engine.py
  ```

- To test **Calculus & Tangent plotting** CLI:
  ```bash
  python app/app/m3_calculus.py
  ```

- To test the **Step Explainer** CLI:
  ```bash
  python app/app/app/app/m5_steps.py
  ```
