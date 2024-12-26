# main.py
from market import Market
from firm import Firm

def create_market_params():
    """Create and return market parameters"""
    return {
        'market_type': 'oligopoly',
        'max_periods': 10,
        'demand': {
            'base_price': 100,
            'price_elasticity': 0.5,
            'min_price': 20,
            'seasonal_factors': [1.0, 1.1, 1.2, 0.9, 0.8, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.0]
        }
    }

def create_base_firm_params():
    """Create and return base firm parameters"""
    return {
        'initial_capital': 10000,
        'strategy': 'balanced',
        'production': {
            'initial_capacity': 100,
            'initial_efficiency': 1.0,
            'max_efficiency': 2.0,
            'upgrade_cost_factor': 100,
            'maintenance_cost_factor': 0.1
        },
        'costs': {
            'fixed_costs': 1000,
            'variable_cost_per_unit': 20,
            'overhead_ratio': 0.1,
            'labor_cost_factor': 15,
            'material_cost_factor': 10
        },
        'inventory': {
            'holding_cost': 5,
            'max_capacity': 200,
            'spoilage_rate': 0.02,
            'min_stock_level': 10,
            'storage_cost_factor': 2
        },
        'risk_tolerance': 0.5,
        'min_profit_margin': 0.1,
        'max_inventory_ratio': 0.8
    }

def create_firms_config(base_params):
    """Create and return firm configurations"""
    return [
        {
            'name': "Acme Corp",
            'params': {
                **base_params,
                'strategy': 'aggressive',
                'risk_tolerance': 0.8
            }
        },
        {
            'name': "Beta Industries",
            'params': {
                **base_params,
                'strategy': 'conservative',
                'risk_tolerance': 0.3,
                'production': {
                    **base_params['production'],
                    'initial_capacity': 120
                }
            }
        },
        {
            'name': "Gamma Ltd",
            'params': {
                **base_params,
                'strategy': 'balanced',
                'risk_tolerance': 0.5,
                'costs': {
                    **base_params['costs'],
                    'fixed_costs': 800
                }
            }
        }
    ]

def print_market_status(market, period):
    """Print detailed market status"""
    stats = market.get_market_stats()
    print(f"\n=== Period {period + 1} ===")
    print(f"Market Phase: {market.get_market_phase()}")
    print(f"Market Price: ${stats['market_price']:.2f}")
    print(f"Total Supply: {stats['total_supply']:.0f}")
    print(f"Market Value: ${stats['total_market_value']:.2f}")
    
    print("\nFirm Status:")
    for firm in market.firms:
        metrics = firm.get_performance_metrics()
        print(f"\n{firm.name}:")
        print(f"  Capital: ${metrics['capital']:.2f}")
        print(f"  Inventory: {metrics['inventory_level']}")
        print(f"  Production Capacity: {metrics['production_capacity']:.1f}")
        print(f"  Efficiency: {metrics['efficiency']:.2f}")
        print(f"  Profit Margin: {metrics['profit_margin']:.1%}")
        print(f"  Capacity Utilization: {metrics['capacity_utilization']:.1%}")
        if metrics['revenue_growth'] != 0:
            print(f"  Revenue Growth: {metrics['revenue_growth']:.1%}")

def main():
    # Create market with parameters
    market_params = create_market_params()
    market = Market(market_params)
    
    # Create base parameters for firms
    base_firm_params = create_base_firm_params()
    
    # Create firm configurations
    firms_config = create_firms_config(base_firm_params)
    
    # Create and add firms to market
    for firm_config in firms_config:
        try:
            firm = Firm(firm_config['name'], firm_config['params'])
            market.add_firm(firm)
        except ValueError as e:
            print(f"Error creating firm {firm_config['name']}: {e}")
            continue
    
    # Run simulation
    try:
        for period in range(market_params['max_periods']):
            print(f"\nPeriod {period + 1}")
            market.simulate_period()
            
            # Print status of each firm
            for firm in market.firms:
                print(f"{firm.name}:")
                print(f"  Capital: ${firm.capital:.2f}")
                print(f"  Inventory: {firm.inventory.current_stock}")
                print(f"  Production capacity: {firm.production.capacity}")
                
        # After simulation, plot the metrics
        market.plot_metrics()  # Changed from plot_market_metrics to plot_metrics
            
    except Exception as e:
        print(f"Error during simulation: {e}")

if __name__ == "__main__":
    main()