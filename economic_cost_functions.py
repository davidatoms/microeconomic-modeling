#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ECONOMIC COST FUNCTIONS
Created on Thu Dec 26 13:43:32 2024

@author: deowulf
"""
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, diff, lambdify

# Global Parameters
FIXED_COST = 100  # Fixed cost component
VARIABLE_COST_PARAMS = {
    'linear_term': 2,    # Coefficient for linear term (ax)
    'quadratic_term': 1  # Coefficient for quadratic term (bx^2)
}
PLOTTING_PARAMS = {
    'x_min': 1,         # Minimum quantity for plotting
    'x_max': 10,        # Maximum quantity for plotting
    'num_points': 100,  # Number of points to plot
    'figure_size': (12, 8)
}
NUMERICAL_PARAMS = {
    'h': 0.0001,  # Step size for numerical differentiation
    'epsilon': 0.01  # Threshold for numerical comparisons
}
ANALYSIS_PARAMS = {
    'test_points': [2, 4, 6, 8],  # Points to analyze MC-AC relationship
}
DISPLAY_PARAMS = {
    'test_quantities': [1, 2, 5, 10],  # Quantities to test in example
    'colors': {
        'tc': 'green',
        'ac': 'blue',
        'mc': 'red'
    }
}

class EconomicCosts:
    def __init__(self, fixed_cost=FIXED_COST):
        """
        Initialize with fixed costs and create variable cost function using global parameters
        """
        self.fixed_cost = fixed_cost
        # Define variable cost function using parameters
        self.variable_cost_fn = lambda x: (VARIABLE_COST_PARAMS['linear_term'] * x + 
                                         VARIABLE_COST_PARAMS['quadratic_term'] * x**2)
    
    def total_cost(self, x):
        """Calculate total cost TC(x) = FC + VC(x)"""
        if x < 0:
            raise ValueError("Quantity must be non-negative")
        return self.fixed_cost + self.variable_cost_fn(x)
    
    def average_cost(self, x):
        """Calculate average cost AC(x) = TC(x)/x"""
        if x <= 0:
            raise ValueError("Quantity must be positive")
        return self.total_cost(x) / x
    
    def marginal_cost_numerical(self, x, h=NUMERICAL_PARAMS['h']):
        """Calculate marginal cost using numerical differentiation"""
        if x < 0:
            raise ValueError("Quantity must be non-negative")
        return (self.total_cost(x + h) - self.total_cost(x)) / h
    
    def create_marginal_cost_symbolic(self):
        """Create symbolic marginal cost function"""
        x = symbols('x')
        # Define symbolic total cost function using parameters
        total_cost_expr = (self.fixed_cost + 
                          VARIABLE_COST_PARAMS['linear_term'] * x + 
                          VARIABLE_COST_PARAMS['quadratic_term'] * x**2)
        return lambdify(x, diff(total_cost_expr, x))
    
    def average_cost_derivative_numerical(self, x, h=NUMERICAL_PARAMS['h']):
        """
        Calculate the first derivative of average cost using numerical differentiation
        d(AC)/dx = d(TC/x)/dx = (MC - AC)/x
        """
        if x < 0:
            raise ValueError("Quantity must be non-negative")
            
        # We can calculate this two ways:
        # 1. Using numerical differentiation directly on AC
        ac_derivative_numerical = (self.average_cost(x + h) - self.average_cost(x)) / h
        
        # 2. Using the formula (MC - AC)/x
        mc = self.marginal_cost_numerical(x)
        ac = self.average_cost(x)
        ac_derivative_formula = (mc - ac) / x
        
        return {
            'numerical': ac_derivative_numerical,
            'formula': ac_derivative_formula
        }
    
    def analyze_ac_derivative(self, x):
        """Analyze the derivative of AC at a given point"""
        derivatives = self.average_cost_derivative_numerical(x)
        
        print(f"\nAt quantity {x}:")
        print(f"AC derivative (numerical): {derivatives['numerical']:.4f}")
        print(f"AC derivative (formula): {derivatives['formula']:.4f}")
        
        if abs(derivatives['numerical']) < NUMERICAL_PARAMS['epsilon']:
            print("AC is at a critical point (minimum or maximum)")
        elif derivatives['numerical'] > 0:
            print("AC is increasing")
        else:
            print("AC is decreasing")
            
        return derivatives

    def plot_all_costs(self):
        """Plot TC, AC, and MC curves using plotting parameters"""
        x = np.linspace(PLOTTING_PARAMS['x_min'], 
                       PLOTTING_PARAMS['x_max'], 
                       PLOTTING_PARAMS['num_points'])
        
        # Calculate costs
        tc = [self.total_cost(xi) for xi in x]
        ac = [self.average_cost(xi) for xi in x]
        mc = [self.marginal_cost_numerical(xi) for xi in x]
        
        # Create plot
        plt.figure(figsize=PLOTTING_PARAMS['figure_size'])
        
        # Plot total cost
        plt.subplot(2, 1, 1)
        plt.plot(x, tc, label='Total Cost (TC)', color=DISPLAY_PARAMS['colors']['tc'])
        plt.title('Total Cost Curve')
        plt.xlabel('Quantity (x)')
        plt.ylabel('Cost')
        plt.grid(True)
        plt.legend()
        
        # Plot AC and MC
        plt.subplot(2, 1, 2)
        plt.plot(x, ac, label='Average Cost (AC)', color=DISPLAY_PARAMS['colors']['ac'])
        plt.plot(x, mc, label='Marginal Cost (MC)', color=DISPLAY_PARAMS['colors']['mc'])
        plt.title('Average and Marginal Cost Curves')
        plt.xlabel('Quantity (x)')
        plt.ylabel('Cost')
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        plt.show()
    
    def find_minimum_ac(self):
        """Find quantity that minimizes average cost"""
        x = np.linspace(PLOTTING_PARAMS['x_min'], 
                       PLOTTING_PARAMS['x_max'], 
                       PLOTTING_PARAMS['num_points'] * 10)  # Using more points for accuracy
        ac = [self.average_cost(xi) for xi in x]
        min_idx = np.argmin(ac)
        return x[min_idx], ac[min_idx]

def analyze_ac_mc_relationship(x, econ):
    """Analyze the relationship between AC and MC at a given quantity"""
    ac = econ.average_cost(x)
    mc = econ.marginal_cost_numerical(x)
    
    # Compare MC and AC using global epsilon
    if abs(mc - ac) < NUMERICAL_PARAMS['epsilon']:
        print(f"\nAt quantity {x}:")
        print("MC ≈ AC: This is the minimum point of average cost")
    elif mc > ac:
        print(f"\nAt quantity {x}:")
        print("MC > AC: Average cost is increasing")
    else:
        print(f"\nAt quantity {x}:")
        print("MC < AC: Average cost is decreasing")
    
    return {'AC': ac, 'MC': mc}

def main():
    # Create instance
    econ = EconomicCosts()
    
    # Print current parameters
    print("Current Parameters:")
    print(f"Fixed Cost: {FIXED_COST}")
    print(f"Variable Cost Parameters: {VARIABLE_COST_PARAMS}")
    print("\nCost calculations for different quantities:")
    
    # Calculate costs for test quantities
    for q in DISPLAY_PARAMS['test_quantities']:
        tc = econ.total_cost(q)
        ac = econ.average_cost(q)
        mc = econ.marginal_cost_numerical(q)
        print(f"\nAt quantity {q}:")
        print(f"Total Cost: {tc:.2f}")
        print(f"Average Cost: {ac:.2f}")
        print(f"Marginal Cost: {mc:.2f}")
    
    # Find minimum average cost
    min_q, min_ac = econ.find_minimum_ac()
    print(f"\nMinimum Average Cost:")
    print(f"Quantity: {min_q:.2f}")
    print(f"Average Cost: {min_ac:.2f}")
    
    # Analyze derivatives of AC at test points
    print("\nAnalyzing AC Derivatives:")
    for x in ANALYSIS_PARAMS['test_points']:
        derivatives = econ.analyze_ac_derivative(x)
    
    # Analyze MC-AC relationship at different points
    print("\nAnalyzing MC-AC Relationship:")
    relationships = []
    for x in ANALYSIS_PARAMS['test_points']:
        result = analyze_ac_mc_relationship(x, econ)
        relationships.append(result)
    
    # Find where MC = AC (minimum average cost point)
    min_q, min_ac = econ.find_minimum_ac()
    print(f"\nAt minimum average cost point (x ≈ {min_q:.2f}):")
    mc_at_min = econ.marginal_cost_numerical(min_q)
    print(f"AC = {min_ac:.2f}")
    print(f"MC = {mc_at_min:.2f}")
    
    # Plot all cost curves
    econ.plot_all_costs()

if __name__ == "__main__":
    main()