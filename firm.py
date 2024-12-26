import matplotlib.pyplot as plt

# firm.py
class Firm:
    @staticmethod
    def validate_firm_params(params):
        required = ['initial_capital', 'strategy', 'production', 'costs', 'inventory', 
                   'risk_tolerance', 'min_profit_margin', 'max_inventory_ratio']
        return all(key in params for key in required)
    
    @staticmethod
    def validate_strategy(strategy):
        return strategy in ['aggressive', 'conservative', 'balanced']

    def __init__(self, name, firm_params):
        if not self.validate_firm_params(firm_params):
            raise ValueError("Invalid firm parameters")
        
        if not self.validate_strategy(firm_params['strategy']):
            raise ValueError("Invalid strategy type")
            
        self.name = name
        self.capital = firm_params['initial_capital']
        self.strategy = firm_params['strategy']
        
        from production import Production
        from costs import Costs
        from inventory import Inventory
        
        self.production = Production(**firm_params['production'])
        self.costs = Costs(**firm_params['costs'])
        self.inventory = Inventory(**firm_params['inventory'])
        
        self.risk_tolerance = firm_params['risk_tolerance']
        self.min_profit_margin = firm_params['min_profit_margin']
        self.max_inventory_ratio = firm_params['max_inventory_ratio']
        
        # Add tracking metrics
        self.total_revenue = 0
        self.total_costs = 0
        self.production_history = []
        self.revenue_history = []
        self.cost_history = []
        self.profit_history = []
        self.periods = []

    def make_production_decision(self, market_data):
        """
        Decide how much to produce based on market conditions and firm strategy
        
        Args:
            market_data (dict): Dictionary containing market information including price
            
        Returns:
            float: Quantity to produce this period
        """
        # Extract market price from market data
        market_price = float(market_data['price']) if isinstance(market_data, dict) else float(market_data)

        # Calculate available production capacity
        max_production = self.production.capacity
        
        # Calculate current inventory space
        available_space = self.inventory.max_capacity - self.inventory.current_stock
        
        # Calculate unit cost including variable and overhead costs with efficiency
        unit_cost = (
            (self.costs.variable_cost_per_unit / self.production.efficiency) + 
            self.costs.overhead_ratio * self.costs.fixed_costs / max_production
        )
        
        # Calculate target profit margin based on strategy
        target_margin = {
            'aggressive': 1.5 * self.min_profit_margin,
            'balanced': 1.2 * self.min_profit_margin,
            'conservative': 1.0 * self.min_profit_margin
        }[self.strategy]
        
        # Calculate break-even price with target margin
        target_price = unit_cost * (1 + target_margin)
        
        # Determine production quantity based on strategy and market conditions
        if market_price >= target_price:
            # Price is good - produce based on strategy
            production_ratios = {
                'aggressive': 0.9,
                'balanced': 0.7,
                'conservative': 0.5
            }
            base_production = max_production * production_ratios[self.strategy]
            
            # Adjust for risk tolerance
            production = base_production * (1 + (self.risk_tolerance - 0.5))
        else:
            # Price is below target - reduce production
            price_ratio = market_price / target_price
            production = max_production * price_ratio * self.risk_tolerance
        
        # Ensure production doesn't exceed available inventory space
        production = min(production, available_space)
        
        # Ensure production is within capital constraints
        max_affordable = self.capital / unit_cost
        production = min(production, max_affordable)
        
        # Track production decision
        self.production_history.append(production)
        
        return max(0, production)  # Ensure non-negative production

    def make_investment_decisions(self, market_price):
        """
        Make strategic investments in capacity and efficiency
        
        Args:
            market_price (float): Current market price
        """
        # Only invest if we have sufficient capital buffer
        investment_budget = max(0, self.capital - self.costs.fixed_costs * 2)
        
        if investment_budget <= 0:
            return
        
        # Investment ratios based on strategy
        capacity_investment_ratio = {
            'aggressive': 0.3,
            'balanced': 0.2,
            'conservative': 0.1
        }[self.strategy]
        
        efficiency_investment_ratio = {
            'aggressive': 0.2,
            'balanced': 0.15,
            'conservative': 0.1
        }[self.strategy]
        
        # Calculate potential investments
        capacity_investment = investment_budget * capacity_investment_ratio
        efficiency_investment = investment_budget * efficiency_investment_ratio
        
        # Upgrade capacity
        if capacity_investment > self.production.upgrade_cost_factor:
            capacity_increase = capacity_investment / self.production.upgrade_cost_factor
            cost = self.production.upgrade_capacity(capacity_increase)
            self.capital -= cost
            self.total_costs += cost

        # Improve efficiency
        if efficiency_investment > self.production.upgrade_cost_factor * 2:
            efficiency_increase = efficiency_investment / (self.production.upgrade_cost_factor * 2)
            cost = self.production.improve_efficiency(efficiency_increase)
            self.capital -= cost
            self.total_costs += cost

    def plot_financial_metrics(self):
        """Plot firm's financial metrics"""
        plt.figure(figsize=(15, 10))
        
        # Revenue plot
        plt.subplot(3, 1, 1)
        plt.plot(self.periods, self.revenue_history, 'g-', label='Revenue')
        plt.title(f'{self.name} - Revenue Over Time')
        plt.xlabel('Period')
        plt.ylabel('Revenue')
        plt.grid(True)
        plt.legend()
        
        # Cost plot
        plt.subplot(3, 1, 2)
        plt.plot(self.periods, self.cost_history, 'r-', label='Costs')
        plt.title(f'{self.name} - Costs Over Time')
        plt.xlabel('Period')
        plt.ylabel('Costs')
        plt.grid(True)
        plt.legend()
        
        # Profit plot
        plt.subplot(3, 1, 3)
        profits = [r - c for r, c in zip(self.revenue_history, self.cost_history)]
        plt.plot(self.periods, profits, 'b-', label='Profit')
        plt.title(f'{self.name} - Profit Over Time')
        plt.xlabel('Period')
        plt.ylabel('Profit')
        plt.grid(True)
        plt.legend()
        
        plt.tight_layout()
        plt.show()
        
    def update_capital(self, revenue, costs):
        """
        Update firm's capital based on revenue and costs
        
        Args:
            revenue (float): Revenue from sales
            costs (float): Total costs incurred
        """
        self.capital += revenue - costs
        self.total_revenue += revenue
        self.total_costs += costs
        
        # History for graphs
        self.revenue_history.append(revenue)
        self.cost_history(costs)
        self.periods.append(len(self.periods))

    def get_performance_metrics(self):
        """
        Get firm's performance metrics
        
        Returns:
            dict: Dictionary containing various performance metrics
        """
        return {
            'name': self.name,
            'capital': self.capital,
            'production_capacity': self.production.capacity,
            'efficiency': self.production.efficiency,
            'inventory_level': self.inventory.current_stock,
            'total_revenue': self.total_revenue,
            'total_costs': self.total_costs,
            'profit_margin': (self.total_revenue - self.total_costs) / self.total_revenue if self.total_revenue > 0 else 0,
            'capacity_utilization': sum(self.production_history[-3:]) / (self.production.capacity * 3) if self.production_history else 0,
            'revenue_growth': ((self.revenue_history[-1] / self.revenue_history[-2]) - 1) if len(self.revenue_history) > 1 else 0
        }