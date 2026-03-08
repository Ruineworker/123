"""
Analytics Screen Module
"""

from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.screen import MDScreen


class AnalyticsScreen(MDScreen):
    """Analytics and Statistics Screen"""
    
    def on_enter(self):
        """Called when screen is entered"""
        Clock.schedule_once(self.load_analytics)
    
    def load_analytics(self, dt=None):
        """Load analytics data"""
        app = self.manager.get_running_app()
        if not app or not app.db:
            return
        
        # Get monthly summary
        summary = app.db.get_monthly_summary()
        
        # Update summary labels
        income_label = self.ids.get("analytics_income")
        expenses_label = self.ids.get("analytics_expenses")
        balance_label = self.ids.get("analytics_balance")
        
        if income_label:
            income_label.text = app.format_currency(summary['income'])
        if expenses_label:
            expenses_label.text = app.format_currency(summary['expenses'])
        if balance_label:
            balance_label.text = app.format_currency(summary['balance'])
        
        # Load category breakdowns
        self.load_category_breakdown("expense")
        self.load_category_breakdown("income")
        
        # Load monthly trend
        self.load_monthly_trend()
    
    def load_category_breakdown(self, trans_type):
        """Load category breakdown for type"""
        app = self.manager.get_running_app()
        if not app or not app.db:
            return
        
        container_id = f"categories_{trans_type}"
        container = self.ids.get(container_id)
        if not container:
            return
        
        container.clear_widgets()
        
        categories = app.db.get_analytics_by_category(trans_type)
        
        # Get total for percentage calculation
        total = sum(cat['total'] for cat in categories)
        
        for cat in categories:
            if cat['total'] > 0:
                percentage = (cat['total'] / total * 100) if total > 0 else 0
                item = CategoryBreakdownItem(
                    name=cat['name'],
                    amount=app.format_currency(cat['total']),
                    percentage=percentage,
                    color=cat['color']
                )
                container.add_widget(item)
    
    def load_monthly_trend(self):
        """Load monthly trend chart data"""
        app = self.manager.get_running_app()
        if not app or not app.db:
            return
        
        container = self.ids.get("monthly_trend_container")
        if not container:
            return
        
        container.clear_widgets()
        
        trends = app.db.get_monthly_trend(months=6)
        
        for trend in trends:
            item = MonthlyTrendItem(
                month=trend['month'],
                income=app.format_currency(trend['income']),
                expenses=app.format_currency(trend['expenses'])
            )
            container.add_widget(item)


class CategoryBreakdownItem(MDScreen):
    """Category breakdown item widget"""
    
    def __init__(self, name="", amount="", percentage=0, color="#14B8A6", **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.amount = amount
        self.percentage = percentage
        self.color = color


class MonthlyTrendItem(MDScreen):
    """Monthly trend item widget"""
    
    def __init__(self, month="", income="", expenses="", **kwargs):
        super().__init__(**kwargs)
        self.month = month
        self.income = income
        self.expenses = expenses
