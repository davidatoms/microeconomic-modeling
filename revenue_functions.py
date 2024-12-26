#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REVENUE FUNCTIONS
Created on Thu Dec 26 13:34:42 2024

@author: deowulf
"""

def revenue(x, price_function):
    """
    Calculate revenue given quantity x and a price function P(x)
    
    Args:
        x: quantity of units
        price_function: function that returns unit price for given quantity
        
    Returns:
        Total revenue R(x) = P(x) * x
    """
    return price_function(x) * x

# Example usage with a simple linear price function
def price(x):
    return 100 - 0.5*x  # Example: Price decreases linearly with quantity

# Calculate revenue for 10 units
x = 10
R = revenue(x, price)