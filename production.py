# production.py
class Production:
    def __init__(self, initial_capacity, initial_efficiency, max_efficiency, 
                 upgrade_cost_factor, maintenance_cost_factor):
        self.capacity = initial_capacity
        self.efficiency = initial_efficiency
        self.max_efficiency = max_efficiency
        self.upgrade_cost_factor = upgrade_cost_factor
        self.maintenance_cost_factor = maintenance_cost_factor

    def upgrade_capacity(self, amount):
        """Upgrade production capacity"""
        self.capacity += amount
        return self.upgrade_cost_factor * amount

    def improve_efficiency(self, amount):
        """Improve production efficiency"""
        self.efficiency = min(self.max_efficiency, self.efficiency + amount)
        return self.upgrade_cost_factor * amount * 2  # Efficiency upgrades cost more

    def calculate_maintenance_cost(self):
        """Calculate periodic maintenance cost"""
        return self.capacity * self.maintenance_cost_factor