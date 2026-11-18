"""
Smart Equation Visualizer + Solver GUI Application
Modern Tkinter/ttk desktop interface with interactive Matplotlib plotting,
pan/zoom navigation toolbar, calculus solver, optimization analyzer, and step explainer.
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from app.math_engine import parse_math_expression, find_roots
from app.calculus import compute_derivative, compute_integral, compute_tangent_line
from app.optimization import find_critical_points, find_global_extrema
from app.step_explainer import (
    explain_roots,
    explain_derivative,
    explain_integration,
    explain_optimization,
)
from app.plotter import render_plot_on_axes


class EquationVisualizerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Smart Equation Visualizer + Solver")
        self.root.geometry("1000x750")
        self.root.minsize(800, 600)

        # Apply ttk theme
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        self.current_expr = None

        self._setup_ui()
        self._set_default_equation("x^2 - 5x + 6")

    def _setup_ui(self):
        # Top Header Frame
        header_frame = ttk.Frame(self.root, padding="8 6 8 6")
        header_frame.pack(fill=tk.X)

        title_label = ttk.Label(
            header_frame,
            text="Smart Equation Visualizer & Solver",
            font=("Segoe UI", 15, "bold"),
        )
        title_label.pack(side=tk.LEFT)

        # Presets dropdown
        preset_frame = ttk.Frame(header_frame)
        preset_frame.pack(side=tk.RIGHT)
        ttk.Label(preset_frame, text="Preset Examples:").pack(side=tk.LEFT, padx=(0, 4))
        self.preset_var = tk.StringVar(value="Select an example...")
        self.presets = [
            "x^2 - 5x + 6",
            "x^3 - 3x",
            "sin(x) * x",
            "2x^2 - 4x + 1",
            "exp(-x^2)",
            "x / (x^2 + 1)",
            "cos(2x) - sin(x)",
            "x^4 - 4x^2 + 2",
        ]
        preset_combo = ttk.Combobox(
            preset_frame,
            textvariable=self.preset_var,
            values=self.presets,
            state="readonly",
            width=18,
        )
        preset_combo.pack(side=tk.LEFT)
        preset_combo.bind("<<ComboboxSelected>>", self._on_preset_selected)

        # Control Panel Frame
        control_frame = ttk.LabelFrame(self.root, text=" Equation & Parameters ", padding="8")
        control_frame.pack(fill=tk.X, padx=10, pady=4)

        # Input Row
        input_row = ttk.Frame(control_frame)
        input_row.pack(fill=tk.X, pady=2)

        ttk.Label(input_row, text="Equation f(x):", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(0, 6))
        self.eq_entry = ttk.Entry(input_row, font=("Consolas", 11))
        self.eq_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.eq_entry.bind("<Return>", lambda event: self.plot_graph())

        ttk.Label(input_row, text="x_min:").pack(side=tk.LEFT, padx=(0, 2))
        self.xmin_entry = ttk.Entry(input_row, width=6)
        self.xmin_entry.insert(0, "-10")
        self.xmin_entry.pack(side=tk.LEFT, padx=(0, 8))

        ttk.Label(input_row, text="x_max:").pack(side=tk.LEFT, padx=(0, 2))
        self.xmax_entry = ttk.Entry(input_row, width=6)
        self.xmax_entry.insert(0, "10")
        self.xmax_entry.pack(side=tk.LEFT, padx=(0, 8))

        ttk.Label(input_row, text="Tangent x0:").pack(side=tk.LEFT, padx=(0, 2))
        self.x0_entry = ttk.Entry(input_row, width=6)
        self.x0_entry.insert(0, "1.0")
        self.x0_entry.pack(side=tk.LEFT)

        # Toggles Row
        toggles_row = ttk.Frame(control_frame)
        toggles_row.pack(fill=tk.X, pady=(6, 2))

        self.show_roots_var = tk.BooleanVar(value=True)
        self.show_extrema_var = tk.BooleanVar(value=True)
        self.show_tangent_var = tk.BooleanVar(value=False)
        self.grid_var = tk.BooleanVar(value=True)

        ttk.Checkbutton(toggles_row, text="Show Roots", variable=self.show_roots_var, command=self.plot_graph).pack(side=tk.LEFT, padx=6)
        ttk.Checkbutton(toggles_row, text="Show Extrema (Min/Max)", variable=self.show_extrema_var, command=self.plot_graph).pack(side=tk.LEFT, padx=6)
        ttk.Checkbutton(toggles_row, text="Show Tangent at x0", variable=self.show_tangent_var, command=self.plot_graph).pack(side=tk.LEFT, padx=6)
        ttk.Checkbutton(toggles_row, text="Show Grid", variable=self.grid_var, command=self.plot_graph).pack(side=tk.LEFT, padx=6)

        # Action Buttons Row
        buttons_row = ttk.Frame(control_frame)
        buttons_row.pack(fill=tk.X, pady=(6, 2))

        btn_plot = ttk.Button(buttons_row, text="📈 Plot Graph", command=self.plot_graph)
        btn_plot.pack(side=tk.LEFT, padx=4)

        btn_roots = ttk.Button(buttons_row, text="🎯 Solve Roots", command=self.solve_roots)
        btn_roots.pack(side=tk.LEFT, padx=4)

        btn_deriv = ttk.Button(buttons_row, text="📐 Derivative & Tangent", command=self.show_derivative)
        btn_deriv.pack(side=tk.LEFT, padx=4)

        btn_integral = ttk.Button(buttons_row, text="∫ Integral", command=self.show_integral)
        btn_integral.pack(side=tk.LEFT, padx=4)

        btn_extrema = ttk.Button(buttons_row, text="⚡ Max / Min", command=self.show_extrema)
        btn_extrema.pack(side=tk.LEFT, padx=4)

        btn_steps = ttk.Button(buttons_row, text="📝 Step-by-Step Explanation", command=self.show_steps_window)
        btn_steps.pack(side=tk.LEFT, padx=4)

        btn_clear = ttk.Button(buttons_row, text="↺ Clear", command=self.clear_all)
        btn_clear.pack(side=tk.RIGHT, padx=4)

        # Center Matplotlib Canvas Frame
        plot_frame = ttk.Frame(self.root)
        plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        self.fig, self.ax = plt.subplots(figsize=(8, 4.5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        self.toolbar.update()

        # Bottom Status Bar
        self.status_var = tk.StringVar(value="Ready. Enter an equation and click 'Plot Graph'.")
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding="4 2 4 2",
            font=("Segoe UI", 9),
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _on_preset_selected(self, event=None):
        selected = self.preset_var.get()
        if selected and selected in self.presets:
            self._set_default_equation(selected)
            self.plot_graph()

    def _set_default_equation(self, eq: str):
        self.eq_entry.delete(0, tk.END)
        self.eq_entry.insert(0, eq)

    def _get_parameters(self):
        raw_eq = self.eq_entry.get().strip()
        if not raw_eq:
            raise ValueError("Please enter an equation in x.")

        try:
            xmin = float(self.xmin_entry.get().strip())
            xmax = float(self.xmax_entry.get().strip())
        except ValueError:
            raise ValueError("x_min and x_max must be valid numbers.")

        if xmin >= xmax:
            raise ValueError("x_min must be strictly less than x_max.")

        try:
            x0 = float(self.x0_entry.get().strip())
        except ValueError:
            x0 = None

        return raw_eq, xmin, xmax, x0

    def plot_graph(self):
        try:
            raw_eq, xmin, xmax, x0 = self._get_parameters()
            self.current_expr = parse_math_expression(raw_eq)

            render_plot_on_axes(
                self.ax,
                self.current_expr,
                xmin=xmin,
                xmax=xmax,
                show_roots=self.show_roots_var.get(),
                show_extrema=self.show_extrema_var.get(),
                show_tangent=self.show_tangent_var.get(),
                x0=x0,
                grid=self.grid_var.get(),
            )
            self.fig.tight_layout()
            self.canvas.draw()
            self.status_var.set(f"Rendered: f(x) = {self.current_expr} on [{xmin}, {xmax}]")

        except Exception as exc:
            messagebox.showerror("Plot Error", str(exc))
            self.status_var.set(f"Error: {exc}")

    def solve_roots(self):
        try:
            raw_eq, _, _, _ = self._get_parameters()
            expr = parse_math_expression(raw_eq)
            roots = find_roots(expr, domain="reals")

            if not roots:
                msg = f"No real roots found for f(x) = {expr}."
            else:
                lines = [f"Roots of f(x) = 0 ({len(roots)} real):"]
                for i, (sym_root, num_val) in enumerate(roots, 1):
                    val_str = f"~ {num_val:.4f}" if num_val is not None else ""
                    lines.append(f"  Root {i}:  x = {sym_root}  {val_str}")
                msg = "\n".join(lines)

            messagebox.showinfo("Roots Result", msg)
            self.status_var.set(f"Solved roots: {len(roots)} real roots found.")

        except Exception as exc:
            messagebox.showerror("Roots Error", str(exc))

    def show_derivative(self):
        try:
            raw_eq, _, _, x0 = self._get_parameters()
            expr = parse_math_expression(raw_eq)
            d1 = compute_derivative(expr, 1)

            lines = [f"Function:       f(x)  = {expr}"]
            lines.append(f"1st Derivative: f'(x) = {d1}")

            if x0 is not None:
                try:
                    tinfo = compute_tangent_line(expr, x0)
                    lines.append(f"\nTangent at x0 = {x0}:")
                    lines.append(f"  Slope m = f'({x0}) = {tinfo['slope']:.4f}")
                    lines.append(f"  Point (x0, y0)   = ({x0}, {tinfo['y0']:.4f})")
                    lines.append(f"  Equation: {tinfo['equation_str']}")
                except Exception as t_err:
                    lines.append(f"\n(Could not evaluate tangent at x0={x0}: {t_err})")

            messagebox.showinfo("Calculus: Derivative", "\n".join(lines))
            self.status_var.set(f"Derivative: f'(x) = {d1}")

        except Exception as exc:
            messagebox.showerror("Derivative Error", str(exc))

    def show_integral(self):
        try:
            raw_eq, xmin, xmax, _ = self._get_parameters()
            expr = parse_math_expression(raw_eq)
            indef = compute_integral(expr, definite=False)

            lines = [f"Function: f(x) = {expr}"]
            lines.append(f"Indefinite Integral: ∫ f(x) dx = {indef} + C")

            try:
                definite_val = compute_integral(expr, definite=True, a=xmin, b=xmax)
                lines.append(f"Definite Integral on [{xmin}, {xmax}]: {definite_val} (~ {float(definite_val):.4f})")
            except Exception:
                pass

            messagebox.showinfo("Calculus: Integral", "\n".join(lines))
            self.status_var.set(f"Indefinite Integral: {indef} + C")

        except Exception as exc:
            messagebox.showerror("Integral Error", str(exc))

    def show_extrema(self):
        try:
            raw_eq, xmin, xmax, _ = self._get_parameters()
            expr = parse_math_expression(raw_eq)
            cps = find_critical_points(expr)

            lines = [f"Optimization analysis for f(x) = {expr}:"]
            if not cps:
                lines.append("No interior critical points found where f'(x) = 0.")
            else:
                lines.append(f"Found {len(cps)} critical point(s):")
                for cp in cps:
                    lines.append(
                        f"  • {cp['nature']}: x = {cp['x']:.4f}, y = {cp['y']:.4f} (f''={cp['d2']:.4f})"
                    )

            extrema = find_global_extrema(expr, xmin, xmax)
            lines.append(f"\nGlobal Extrema on [{xmin}, {xmax}]:")
            if extrema["global_min"]:
                lines.append(f"  Global Minimum: x = {extrema['global_min']['x']:.4f}, y = {extrema['global_min']['y']:.4f}")
            if extrema["global_max"]:
                lines.append(f"  Global Maximum: x = {extrema['global_max']['x']:.4f}, y = {extrema['global_max']['y']:.4f}")

            messagebox.showinfo("Extrema & Optimization", "\n".join(lines))
            self.status_var.set(f"Critical Points: {len(cps)} found.")

        except Exception as exc:
            messagebox.showerror("Extrema Error", str(exc))

    def show_steps_window(self):
        try:
            raw_eq, _, _, _ = self._get_parameters()
            expr = parse_math_expression(raw_eq)

            steps_win = tk.Toplevel(self.root)
            steps_win.title(f"Step-by-Step Solver: f(x) = {expr}")
            steps_win.geometry("700x550")

            notebook = ttk.Notebook(steps_win)
            notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

            # Tab 1: Roots
            tab_roots = ttk.Frame(notebook)
            notebook.add(tab_roots, text="Roots Steps")
            txt_roots = scrolledtext.ScrolledText(tab_roots, font=("Consolas", 10), wrap=tk.WORD)
            txt_roots.pack(fill=tk.BOTH, expand=True)
            txt_roots.insert(tk.END, explain_roots(expr))
            txt_roots.configure(state="disabled")

            # Tab 2: Derivative
            tab_deriv = ttk.Frame(notebook)
            notebook.add(tab_deriv, text="Derivative Steps")
            txt_deriv = scrolledtext.ScrolledText(tab_deriv, font=("Consolas", 10), wrap=tk.WORD)
            txt_deriv.pack(fill=tk.BOTH, expand=True)
            txt_deriv.insert(tk.END, explain_derivative(expr))
            txt_deriv.configure(state="disabled")

            # Tab 3: Integration
            tab_int = ttk.Frame(notebook)
            notebook.add(tab_int, text="Integration Steps")
            txt_int = scrolledtext.ScrolledText(tab_int, font=("Consolas", 10), wrap=tk.WORD)
            txt_int.pack(fill=tk.BOTH, expand=True)
            txt_int.insert(tk.END, explain_integration(expr))
            txt_int.configure(state="disabled")

            # Tab 4: Optimization
            tab_opt = ttk.Frame(notebook)
            notebook.add(tab_opt, text="Optimization Steps")
            txt_opt = scrolledtext.ScrolledText(tab_opt, font=("Consolas", 10), wrap=tk.WORD)
            txt_opt.pack(fill=tk.BOTH, expand=True)
            txt_opt.insert(tk.END, explain_optimization(expr))
            txt_opt.configure(state="disabled")

        except Exception as exc:
            messagebox.showerror("Explanation Error", str(exc))

    def clear_all(self):
        self.eq_entry.delete(0, tk.END)
        self.ax.clear()
        self.ax.set_title("Enter an equation above to plot", fontsize=11)
        self.ax.grid(True, linestyle=":", alpha=0.6)
        self.canvas.draw()
        self.status_var.set("Cleared.")


def main():
    root = tk.Tk()
    app = EquationVisualizerApp(root)
    # Automatically plot default preset on startup
    root.after(100, app.plot_graph)
    root.mainloop()


if __name__ == '__main__':
    main()
