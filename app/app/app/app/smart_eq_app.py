import sympy as sp
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Tkinter GUI Setup
root = Tk()
root.title("Smart Equation Visualizer + Solver")
root.geometry("800x600")

# Input Box
Label(root, text="Enter equation in x (e.g. x**2 - 5*x + 6):").pack(pady=10)
eq_input = Entry(root, width=40, font=("Arial", 14))
eq_input.pack()

x = sp.symbols('x')

def plot_graph():
    try:
        expr = sp.sympify(eq_input.get())
        f = sp.lambdify(x, expr, 'numpy')

        fig, ax = plt.subplots()
        import numpy as np
        X = np.linspace(-10, 10, 400)
        Y = f(X)
        ax.plot(X, Y, label=f"f(x) = {expr}")
        ax.axhline(0, color="black", linewidth=0.8)
        ax.axvline(0, color="black", linewidth=0.8)
        ax.grid(True)
        ax.legend()

        # Embed into Tkinter
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack()
        canvas.draw()

    except Exception as e:
        messagebox.showerror("Error", f"Invalid equation!\n{e}")

def solve_roots():
    try:
        expr = sp.sympify(eq_input.get())
        roots = sp.solve(expr, x)
        messagebox.showinfo("Roots", f"Roots: {roots}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not solve roots!\n{e}")

def derivative():
    try:
        expr = sp.sympify(eq_input.get())
        d = sp.diff(expr, x)
        messagebox.showinfo("Derivative", f"f'(x) = {d}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not calculate derivative!\n{e}")

def find_turning_points():
    try:
        expr = sp.sympify(eq_input.get())
        d = sp.diff(expr, x)
        critical_points = sp.solve(d, x)
        values = [(cp, expr.subs(x, cp)) for cp in critical_points]
        messagebox.showinfo("Turning Points", f"Critical Points: {values}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not find turning points!\n{e}")

# Buttons
frame = Frame(root)
frame.pack(pady=20)

Button(frame, text="Plot Graph", command=plot_graph, width=15).grid(row=0, column=0, padx=5)
Button(frame, text="Solve Roots", command=solve_roots, width=15).grid(row=0, column=1, padx=5)
Button(frame, text="Derivative", command=derivative, width=15).grid(row=0, column=2, padx=5)
Button(frame, text="Max/Min", command=find_turning_points, width=15).grid(row=0, column=3, padx=5)

root.mainloop()
