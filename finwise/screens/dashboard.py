"""
Dashboard Screen Module
"""

from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.screen import MDScreen


class DashboardScreen(MDScreen):
    """Main Dashboard Screen"""
    
    total_balance = StringProperty("$0.00")
    monthly_income = StringProperty("$0.00")
    monthly_expenses = StringProperty("$0.00")
    
    def on_enter(self):
        """Called when screen is entered"""
        Clock.schedule_once(self.update_data)
    
    def update_data(self, dt=None):
        """Update dashboard data"""
        app = self.manager.get_running_app()
        if app and app.db:
            # Get total balance
            balance = app.db.get_total_balance()
            self.total_balance = app.format_currency(balance)
            
            # Get monthly summary
            summary = app.db.get_monthly_summary()
            self.monthly_income = app.format_currency(summary['income'])
            self.monthly_expenses = app.format_currency(summary['expenses'])
            
            # Refresh recent transactions list
            self.refresh_transactions()
    
    def refresh_transactions(self):
        """Refresh recent transactions list"""
        # This will be handled by the KV file's RecycleView
    
    def add_income(self):
        """Navigate to add transaction screen with income type"""
        app = self.manager.get_running_app()
        add_screen = self.manager.get_screen("add_transaction")
        if add_screen:
            add_screen.set_transaction_type("income")
        self.manager.current = "add_transaction"
    
    def add_expense(self):
        """Navigate to add transaction screen with expense type"""
        app = self.manager.get_running_app()
        add_screen = self.manager.get_screen("add_transaction")
        if add_screen:
            add_screen.set_transaction_type("expense")
        self.manager.current = "add_transaction"
    
    def go_to_transactions(self):
        """Navigate to transactions screen"""
        self.manager.current = "transactions"
    
    def go_to_analytics(self):
        """Navigate to analytics screen"""
        self.manager.current = "analytics"
