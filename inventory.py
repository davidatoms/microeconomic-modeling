# inventory.py
class Inventory:
    def __init__(self, holding_cost, max_capacity, spoilage_rate, min_stock_level, storage_cost_factor):
        self.holding_cost = holding_cost
        self.max_capacity = max_capacity
        self.spoilage_rate = spoilage_rate
        self.min_stock_level = min_stock_level
        self.storage_cost_factor = storage_cost_factor
        self.current_stock = 0

    def add_stock(self, quantity):
        """Add stock to inventory"""
        self.current_stock = min(self.current_stock + quantity, self.max_capacity)

    def remove_stock(self, quantity):
        """Remove stock from inventory"""
        self.current_stock = max(0, self.current_stock - quantity)