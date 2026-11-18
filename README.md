# Smart Equation Visualizer & Solver

[![CI Build & Tests](https://github.com/Jaspreet-93/Equation-Visualization/actions/workflows/ci.yml/badge.svg)](https://github.com/Jaspreet-93/Equation-Visualization/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests: Unittest](https://img.shields.io/badge/tests-26%20passed-brightgreen.svg)](tests/)

An interactive desktop application built with Python using **Tkinter**, **SymPy**, and **Matplotlib**. The application serves as an educational and mathematical suite to safely parse, plot, analyze, and solve algebraic equations step-by-step.

---

## 🌟 Key Features

- **Safe & Smart Parser**:
  - Restricts execution to safe mathematical symbols and functions (`sin`, `cos`, `tan`, `sinh`, `cosh`, `exp`, `log`, `ln`, `sqrt`, `Abs`, `pi`, `e`).
  - Supports user-friendly syntax such as **implicit multiplication** (e.g., `2x`, `3(x - 1)`), **caret powers** (e.g., `x^2`), and **equation notation** (e.g., `x^2 = 4` or `x^2 - 5x + 6 = 0`).

- **Interactive Canvas & Navigation Toolbar**:
  - Embedded Matplotlib figure within Tkinter utilizing `FigureCanvasTkAgg` and `NavigationToolbar2Tk`.
  - Full pan, zoom, reset, and high-resolution export capabilities.
  - Asymptote and domain boundary protection (handles singularities like $1/x$ gracefully without crashes).

- **Root Solver**:
  - Finds algebraic solutions and numerical approximations for $f(x) = 0$.
  - Distinguishes real roots from complex roots.
  - Automatically places coordinate markers and labels on the graph.

- **Calculus Engine**:
  - **Derivatives**: Computes first and higher-order symbolic derivatives $f'(x)$, $f''(x)$.
  - **Tangent & Normal Lines**: Computes slope $m = f'(x_0)$ and plots tangent lines at any user-defined point $x_0$.
  - **Integrals**: Computes both indefinite antiderivatives $\int f(x) dx + C$ and definite integrals $\int_{x_{\min}}^{x_{\max}} f(x) dx$.
  - **Limits**: Evaluates directional and two-sided limits $\lim_{x \to x_0} f(x)$.

- **Optimization & Extrema Classification**:
  - Solves for critical points where $f'(x) = 0$.
  - Employs the **Second Derivative Test** ($f''(x)$) to classify points into **Local Minimum**, **Local Maximum**, or **Inflection Points**.
  - Computes global extrema over the selected interval $[x_{\min}, x_{\max}]$.
  - Color-coded extrema overlay markers directly on the graph.

- **Step-by-Step Solver Dialog**:
  - Dedicated multi-tabbed explanation window detailing:
    - Quadratic formula discriminant derivation ($\Delta = b^2 - 4ac$) and linear isolation.
    - Differentiation step-by-step applying power, product, and chain rules.
    - Antiderivative integration formulas.
    - First and second derivative optimization tests.

- **Preset Library**:
  - Instant dropdown menu with classic equations:
    - Polynomials: $x^2 - 5x + 6$, $x^3 - 3x$, $x^4 - 4x^2 + 2$
    - Oscillatory & Damped: $\sin(x) \cdot x$, $\cos(2x) - \sin(x)$
    - Gaussian / Rational: $e^{-x^2}$, $\frac{x}{x^2 + 1}$

---

## 🗺️ Execution Flowchart

```mermaid
flowchart TD
    Start([Launch Application]) --> GUI[Tkinter GUI Initialized]
    GUI --> Input[User Enters Equation or Selects Preset]
    
    Input --> Parse[Safe Parser with SymPy Transformations\n• Implicit Multiplication 2x -> 2*x\n• Caret Power x^2 -> x**2\n• Equation Parsing lhs = rhs]
    
    Parse --> Action{User Action}

    Action -->|Plot Graph| Plot[Generate NumPy Array with NaN Singularity Handling]
    Plot --> Canvas[Render on Matplotlib Canvas + Navigation Toolbar]
    Canvas --> Overlays{Toggles Active?}
    Overlays -->|Roots| PlotRoots[Plot Roots Coordinates & Dots]
    Overlays -->|Extrema| PlotExtrema[Plot Min / Max Labeled Markers]
    Overlays -->|Tangent| PlotTangent[Compute & Plot Tangent Line at x0]
    
    Action -->|Solve Roots| Roots[Symbolic Root Extraction via solveset/solve]
    Roots --> ShowRoots[Display Real & Complex Roots Dialog]

    Action -->|Derivative & Tangent| Deriv[Compute f'\(x\) & Tangent Line at x0]
    Deriv --> ShowDeriv[Display Derivative & Slope Summary]

    Action -->|Integral| Integ[Compute Indefinite & Definite Integrals]
    Integ --> ShowInteg[Display Antiderivative & Area]

    Action -->|Max / Min| Opt[Calculate Critical Points & Second Derivative Test]
    Opt --> ShowOpt[Classify Local Min/Max and Global Extrema]

    Action -->|Step-by-Step Solver| Steps[Generate Step-by-Step Mathematical Explanation]
    Steps --> ShowSteps[Open Multi-Tabbed Dialog: Roots, Derivative, Integral, Optimization]

    PlotRoots --> Idle([Wait for User Event])
    PlotExtrema --> Idle
    PlotTangent --> Idle
    ShowRoots --> Idle
    ShowDeriv --> Idle
    ShowInteg --> Idle
    ShowOpt --> Idle
    ShowSteps --> Idle
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
| :--- | :--- |
| **Python 3.8+** | Core runtime environment |
| **Tkinter / ttk** | Native desktop graphical user interface with themed widgets |
| **SymPy** | Computer Algebra System (CAS) for symbolic parsing, differentiation, and solving |
| **Matplotlib** | 2D mathematical plotting engine with `FigureCanvasTkAgg` and toolbar integration |
| **NumPy** | High-performance vectorized numerical evaluations over custom intervals |
| **Unittest** | Built-in automated unit testing framework |
| **GitHub Actions** | Automated Continuous Integration (CI) matrix across Python 3.9 - 3.12 |

---

## 📂 Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI matrix workflow
├── app/
│   ├── __init__.py              # Package exports
│   ├── math_engine.py           # Safe parser, symbol allowlist & root solver
│   ├── plotter.py               # Curve evaluation, canvas rendering & overlays
│   ├── calculus.py              # Derivatives, integrals, tangent & normal lines
│   ├── optimization.py          # Critical points, 2nd derivative test & extrema
│   ├── step_explainer.py        # Step-by-step math explanations generator
│   ├── smart_eq_app.py          # Modern Tkinter GUI application
│   ├── m1_math_engine.py        # Legacy compatibility wrapper
│   ├── m2_plot.py               # Legacy compatibility wrapper
│   └── app/
│       ├── m3_calculus.py       # Legacy compatibility wrapper
│       └── app/
│           ├── m4_optimization.py # Legacy compatibility wrapper
│           └── app/
│               ├── m5_steps.py    # Legacy compatibility wrapper
│               └── smart_eq_app.py # Legacy compatibility wrapper
├── tests/
│   ├── __init__.py
│   ├── test_math_engine.py      # Tests for parsing, syntax & roots
│   ├── test_calculus.py         # Tests for derivatives, integrals & tangents
│   ├── test_optimization.py     # Tests for local/global extrema classification
│   ├── test_step_explainer.py   # Tests for step generation
│   └── test_plotter.py          # Tests for array generation & singularity safety
├── .gitignore                   # Ignore caches, virtual environments, bytecode
├── main.py                      # Primary application launcher
├── pyproject.toml               # Modern Python package configuration
├── README.md                    # Project documentation
└── requirements.txt             # Direct project dependencies
```

---

## 💻 Installation & Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/Jaspreet-93/Equation-Visualization.git
cd Equation-Visualization
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Launch the graphical user interface with either:
```bash
python main.py
```
or
```bash
python -m app.smart_eq_app
```

---

## 🧪 Running Unit Tests

Run the complete test suite locally:
```bash
python -m unittest discover -v tests
```

Expected output:
```text
Ran 26 tests in ~0.5s
OK
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
