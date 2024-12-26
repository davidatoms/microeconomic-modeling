#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRODUCTION FUNCTIONS
Created on Thu Dec 26 13:18:03 2024

@author: deowulf
"""
from sympy import *
import sympy as sp

# Define our variables and constants
t, x, m, hbar = symbols('t x m ħ')
omega = Symbol('ω')
psi = Function('ψ')(x, t)
i = I

# Set up Schrödinger equation
V = (1/2) * m * omega**2 * x**2
schrodinger = Eq(
    i * hbar * diff(psi, t),
    -((hbar**2)/(2*m)) * diff(psi, x, 2) + V*psi
)

# Print in LaTeX format
print("LaTeX format:")
print(latex(schrodinger))

# For inline LaTeX
print("\nInline LaTeX format:")
print("$" + latex(schrodinger) + "$")

# For display LaTeX (centered equation)
print("\nDisplay LaTeX format:")
print("\\[ " + latex(schrodinger) + " \\]")

