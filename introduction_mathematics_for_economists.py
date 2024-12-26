import numpy as np
import matplotlib.pyplot as plt

def plot_utility_comparisons():
    # MODIFY: Change figure size and number of subplots
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # MODIFY: Change the range and number of points for x₁
    x1 = np.linspace(0.1, 10, 100)  # start value, end value, number of points
    
    # MODIFY: Change utility levels to plot different indifference curves
    utility_levels = [2, 4, 6, 8]  # Add or remove values to show more/fewer curves
    
    # 1. Cobb-Douglas
    ax = axes[0]
    # MODIFY: Change preference parameters alpha and beta
    # alpha = beta = 0.5 means equal preferences
    # alpha > beta means stronger preference for good 1
    # alpha < beta means stronger preference for good 2
    alpha, beta = 0.5, 0.5
    for u in utility_levels:
        x2 = np.exp((np.log(u) - alpha * np.log(x1)) / beta)
        ax.plot(x1, x2, '--', label=f'U={u}')
    ax.set_title('Cobb-Douglas\nU = x₁ᵅ × x₂ᵝ')
    
    # MODIFY: Change axis limits for Cobb-Douglas plot
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.grid(True)
    
    # 2. CES
    ax = axes[1]
    # MODIFY: Change rho to see different elasticities of substitution
    # rho → 1: goods become perfect substitutes (straight lines)
    # rho → -∞: goods become perfect complements (L-shaped)
    # rho = 0: Cobb-Douglas case
    rho = 0.5
    for u in utility_levels:
        x2 = (u**rho - x1**rho)**(1/rho)
        ax.plot(x1, x2, '--', label=f'U={u}')
    ax.set_title('CES\nU = (x₁ᵖ + x₂ᵖ)^(1/ρ)')
    
    # MODIFY: Change axis limits for CES plot
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.grid(True)
    
    # 3. Quasilinear
    ax = axes[2]
    # MODIFY: Change utility function form
    # Current: U = x₁ + ln(x₂)
    # Could modify to: U = x₁ + x₂^0.5 or other forms
    for u in utility_levels:
        # MODIFY: Change function here for different quasilinear forms
        x2 = np.exp(u - x1)
        ax.plot(x1, x2, '--', label=f'U={u}')
    ax.set_title('Quasilinear\nU = x₁ + ln(x₂)')
    
    # MODIFY: Change axis limits for Quasilinear plot
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.grid(True)
    
    # MODIFY: Change plot aesthetics
    for ax in axes:
        ax.set_xlabel('x₁')
        ax.set_ylabel('x₂')
        ax.legend()
        # Could modify grid style, line colors, etc.
    
    # MODIFY: Change spacing between subplots
    plt.tight_layout()
    return fig

# Example modifications you could make:
# 1. Add budget constraint:
# ax.plot(x1, (100 - 2*x1)/3, 'r-', label='Budget')

# 2. Add optimal point:
# ax.plot(x1_opt, x2_opt, 'bo', markersize=10, label='Optimal')

# 3. Change utility function types:
# - Perfect substitutes: U = x₁ + x₂
# - Perfect complements: U = min(x₁, x₂)
# - Stone-Geary: U = (x₁ - a)^α * (x₂ - b)^β

plot_utility_comparisons()