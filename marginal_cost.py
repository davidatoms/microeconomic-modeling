#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 13:33:55 2024

@author: deowulf
"""

import numpy as np
from sympy import symbols, diff, lambdify

def marginal_cost_numerical(x, fixed_cost=0, variable_cost_fn=None, h=0.0001):
    """
    Calculate marginal cost using numerical differentiation
    MC(x) = dC/dx ≈ [C(x+h) - C(x)]/h
    
    Parameters:
    x (float): Quantity
    fixed_cost (float): Fixed costs
    variable_cost_fn (function): Variable cost function
    h (float): Small increment for numerical differentiation
    """
    if variable_cost_fn is None:
        variable_cost_fn = lambda x: x
        
    # Calculate total cost at x and x+h
    c_x = fixed_cost + variable_cost_fn(x)
    c_xh = fixed_cost + variable_cost_fn(x + h)
    
    # Numerical derivative
    mc = (c_xh - c_x) / h
    return mc

# Analytical approach using SymPy
def create_marginal_cost_function():
    """
    Create an analytical marginal cost function using symbolic differentiation
    """
    # Define symbolic variable
    x = symbols('x')
    
    # Example total cost function: TC = 100 + 2x + x^2
    fixed_cost = 100
    total_cost = fixed_cost + 2*x + x**2
    
    # Calculate derivative
    marginal_cost = diff(total_cost, x)
    
    # Convert to numerical function
    mc_function = lambdify(x, marginal_cost)
    
    return mc_function

import matplotlib.pyplot as plt

def plot_cost_curves(x_range):
    """
    Plot AC and MC curves
    """
    # Create cost functions
    fixed_cost = 100
    variable_cost = lambda x: 2*x + x**2
    
    # Calculate costs
    x = np.linspace(x_range[0], x_range[1], 100)
    ac = [average_cost(xi, fixed_cost, variable_cost) for xi in x]
    mc = [marginal_cost_numerical(xi, fixed_cost, variable_cost) for xi in x]
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(x, ac, label='Average Cost (AC)', color='blue')
    plt.plot(x, mc, label='Marginal Cost (MC)', color='red')
    plt.title('Average and Marginal Cost Curves')
    plt.xlabel('Quantity (x)')
    plt.ylabel('Cost')
    plt.grid(True)
    plt.legend()
    plt.show()

# Plot the curves
plot_cost_curves([1, 10])

# Example usage:
if __name__ == "__main__":
    # Example with quadratic variable costs
    quad_cost = lambda x: x**2
    
    # Test numerical approach
    quantities = [1, 2, 5, 10]
    print("Numerical Marginal Costs:")
    for q in quantities:
        mc = marginal_cost_numerical(q, fixed_cost=100, variable_cost_fn=quad_cost)
        print(f"MC(x={q}) = {mc:.2f}")
    
    # Test analytical approach
    mc_function = create_marginal_cost_function()
    print("\nAnalytical Marginal Costs:")
    for q in quantities:
        mc = mc_function(q)
        print(f"MC(x={q}) = {mc:.2f}")