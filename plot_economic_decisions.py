#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 12:52:25 2024

@author: deowulf
"""

import numpy as np
import matplotlib.pyplot as plt

def plot_economic_scenarios():
    fig, axes = plt.subplots(2, 2, figsize=(15, 15))
    
    # Scenario 1: Strong preference for good 1 (Cobb-Douglas)
    ax = axes[0,0]
    x1 = np.linspace(0.1, 10, 100)
    utility_levels = [2, 4, 6, 8, 10]
    
    # Strong preference for good 1
    alpha, beta = 0.8, 0.2
    for u in utility_levels:
        x2 = np.exp((np.log(u) - alpha * np.log(x1)) / beta)
        ax.plot(x1, x2, '--', label=f'U={u}')
    
    # Add budget constraint
    budget_x1 = np.linspace(0, 10, 100)
    budget_x2 = (100 - 2*budget_x1)/3
    ax.plot(budget_x1, budget_x2, 'r-', label='Budget')
    
    ax.set_title('Strong Preference for Good 1\nα=0.8, β=0.2')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.grid(True)
    
    # Scenario 2: Nearly Perfect Complements (CES)
    ax = axes[0,1]
    rho = -5  # Very negative rho for strong complementarity
    for u in utility_levels:
        try:
            x2 = (u**rho - x1**rho)**(1/rho)
            ax.plot(x1, x2, '--', label=f'U={u}')
        except:
            continue
    
    ax.plot(budget_x1, budget_x2, 'r-', label='Budget')
    ax.set_title('Nearly Perfect Complements\nρ=-5')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.grid(True)
    
    # Scenario 3: Perfect Substitutes
    ax = axes[1,0]
    # Perfect substitutes: straight line indifference curves
    for u in utility_levels:
        x2 = (u - x1)  # U = x₁ + x₂
        ax.plot(x1, x2, '--', label=f'U={u}')
    
    ax.plot(budget_x1, budget_x2, 'r-', label='Budget')
    ax.set_title('Perfect Substitutes\nU = x₁ + x₂')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.grid(True)
    
    # Scenario 4: Stone-Geary (subsistence levels)
    ax = axes[1,1]
    # Stone-Geary with subsistence levels
    a, b = 2, 1  # Subsistence levels
    alpha, beta = 0.5, 0.5
    for u in utility_levels:
        # U = (x₁ - a)^α * (x₂ - b)^β
        try:
            x2 = b + (u/((x1-a)**alpha))**(1/beta)
            ax.plot(x1[x1>a], x2[x1>a], '--', label=f'U={u}')
        except:
            continue
    
    ax.plot(budget_x1, budget_x2, 'r-', label='Budget')
    ax.axvline(x=a, color='g', linestyle=':', label='x₁ subsistence')
    ax.axhline(y=b, color='g', linestyle=':', label='x₂ subsistence')
    ax.set_title('Stone-Geary Utility\nSubsistence Levels')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.grid(True)
    
    # Common settings for all plots
    for ax in axes.flat:
        ax.set_xlabel('x₁')
        ax.set_ylabel('x₂')
        ax.legend()
    
    plt.tight_layout()
    return fig

plot_economic_scenarios()