# market.py
from demand import Demand
import matplotlib.pyplot as plt

class Market:
    def __init__(self, params):
        demand_params = params['demand']
        self.demand = Demand(
            base_price=demand_params['base_price'],
            price_elasticity=demand_params['price_elasticity'],
            min_price=demand_params['min_price'],
            seasonal_factors=demand_params.get('seasonal_factors')
        )
        self.firms = []
        self.market_type = params['market_type']
        self.max_periods = params['max_periods']
        self.current_period = 0
        self.total_market_value = 0
        self.price_history = []
        self.periods = []
        self.firm_metrics = {}  # Store metrics for each firm

    def add_firm(self, firm):
        """Add a firm to the market and initialize its metrics"""
        self.firms.append(firm)
        self.firm_metrics[firm.name] = {
            'revenue': [],
            'costs': [],
            'profits': [],
            'market_price': []
        }

    def calculate_market_share(self):
        """Calculate market share for each firm"""
        total_sales = sum(firm.inventory.current_stock for firm in self.firms)
        if total_sales == 0:
            return {firm.name: 0 for firm in self.firms}
        return {
            firm.name: firm.inventory.current_stock / total_sales 
            for firm in self.firms
        }

    def calculate_market_concentration(self):
        """Calculate Herfindahl-Hirschman Index (HHI) for market concentration"""
        market_shares = self.calculate_market_share()
        return sum(share * share * 10000 for share in market_shares.values())

    def get_market_stats(self):
        """Get current market statistics"""
        total_supply = sum(firm.inventory.current_stock for firm in self.firms)
        market_price = self.demand.get_market_price(total_supply)
        return {
            'total_supply': total_supply,
            'market_price': market_price,
            'total_market_value': self.total_market_value,
            'market_concentration': self.calculate_market_concentration(),
            'market_shares': self.calculate_market_share()
        }

    def simulate_period(self):
        """Simulate one period of market activity"""
        # Get current market conditions
        total_supply = sum(firm.inventory.current_stock for firm in self.firms)
        market_price = self.demand.get_market_price(total_supply)
        
        # Track this period
        self.periods.append(self.current_period)
        self.price_history.append(market_price)
        
        market_data = {
            'price': market_price,
            'total_supply': total_supply,
            'period': self.current_period
        }

        # Production phase
        for firm in self.firms:
            # Make production decisions
            production_qty = firm.make_production_decision(market_data)
            
            # Calculate production costs
            production_cost = (
                (firm.costs.variable_cost_per_unit / firm.production.efficiency) * production_qty +
                firm.costs.fixed_costs +
                firm.production.calculate_maintenance_cost()
            )
            
            if production_cost <= firm.capital:
                firm.inventory.add_stock(production_qty)
                firm.capital -= production_cost
                self.firm_metrics[firm.name]['costs'].append(production_cost)
            else:
                self.firm_metrics[firm.name]['costs'].append(0)

        # Market clearing and sales phase
        total_supply = sum(firm.inventory.current_stock for firm in self.firms)
        market_value = 0
        
        if total_supply > 0:
            market_price = self.demand.get_market_price(total_supply)
            
            for firm in self.firms:
                # Calculate market share and sales
                market_share = firm.inventory.current_stock / total_supply
                sales_qty = min(firm.inventory.current_stock, market_share * total_supply)
                revenue = sales_qty * market_price
                
                # Update firm state
                firm.inventory.remove_stock(sales_qty)
                firm.capital += revenue
                market_value += revenue
                
                # Apply inventory holding costs
                holding_cost = firm.inventory.current_stock * firm.inventory.holding_cost
                firm.capital -= holding_cost
                
                # Track metrics
                self.firm_metrics[firm.name]['revenue'].append(revenue)
                self.firm_metrics[firm.name]['profits'].append(
                    revenue - self.firm_metrics[firm.name]['costs'][-1]
                )
                self.firm_metrics[firm.name]['market_price'].append(market_price)
                
                # Investment phase
                firm.make_investment_decisions(market_price)
        else:
            # No supply - record zeros
            for firm in self.firms:
                self.firm_metrics[firm.name]['revenue'].append(0)
                self.firm_metrics[firm.name]['profits'].append(
                    -self.firm_metrics[firm.name]['costs'][-1]
                )
                self.firm_metrics[firm.name]['market_price'].append(market_price)

        # Update market state
        self.total_market_value = market_value
        self.current_period += 1
        self.demand.advance_period()

    def plot_metrics(self):
        """Plot all firms' metrics"""
        plt.figure(figsize=(15, 10))
        
        # Plot revenues
        plt.subplot(3, 1, 1)
        for firm_name, metrics in self.firm_metrics.items():
            plt.plot(self.periods, metrics['revenue'], label=f'{firm_name} Revenue')
        plt.title('Firm Revenues Over Time')
        plt.xlabel('Period')
        plt.ylabel('Revenue')
        plt.grid(True)
        plt.legend()
        
        # Plot costs
        plt.subplot(3, 1, 2)
        for firm_name, metrics in self.firm_metrics.items():
            plt.plot(self.periods, metrics['costs'], label=f'{firm_name} Costs')
        plt.title('Firm Costs Over Time')
        plt.xlabel('Period')
        plt.ylabel('Costs')
        plt.grid(True)
        plt.legend()
        
        # Plot profits
        plt.subplot(3, 1, 3)
        for firm_name, metrics in self.firm_metrics.items():
            plt.plot(self.periods, metrics['profits'], label=f'{firm_name} Profits')
        plt.title('Firm Profits Over Time')
        plt.xlabel('Period')
        plt.ylabel('Profits')
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        plt.show()

    def get_price_trend(self, periods=5):
        """Calculate price trend over the last n periods"""
        if len(self.price_history) < 2:
            return 0
        recent_prices = self.price_history[-periods:]
        if len(recent_prices) < 2:
            return 0
        price_changes = [
            (recent_prices[i] - recent_prices[i-1]) / recent_prices[i-1]
            for i in range(1, len(recent_prices))
        ]
        return sum(price_changes) / len(price_changes)

    def get_market_phase(self):
        """Determine current market phase based on price trends and concentration"""
        price_trend = self.get_price_trend()
        concentration = self.calculate_market_concentration()
        
        if concentration > 2500:  # High concentration
            if price_trend > 0.05:
                return "Monopolistic Growth"
            elif price_trend < -0.05:
                return "Market Correction"
            else:
                return "Stable Oligopoly"
        else:  # Competitive market
            if price_trend > 0.05:
                return "Competitive Growth"
            elif price_trend < -0.05:
                return "Price War"
            else:
                return "Stable Competition"

    def get_performance_report(self):
        """Generate a performance report for all firms"""
        report = {
            'market_phase': self.get_market_phase(),
            'total_market_value': self.total_market_value,
            'average_price': sum(self.price_history) / len(self.price_history) if self.price_history else 0,
            'price_volatility': self.get_price_trend(),
            'firms': {}
        }
        
        for firm in self.firms:
            report['firms'][firm.name] = {
                'capital': firm.capital,
                'market_share': self.calculate_market_share()[firm.name],
                'production_capacity': firm.production.capacity,
                'efficiency': firm.production.efficiency,
                'inventory_level': firm.inventory.current_stock
            }
            
        return report