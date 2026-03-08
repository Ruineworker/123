"""
FinWise - Personal Finance Tracker
Main Application Entry Point
Updated for KivyMD 2.0.0 and Kivy 2.3.1
"""

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.utils import platform
from kivy.metrics import dp
from libs.database import Database
from libs.models import init_db

# Set window size for desktop testing
if platform not in ('android', 'ios'):
    Window.size = (414, 896)  # iPhone-like dimensions
    Window.top = 100
    Window.left = 100


class FinWiseApp(MDApp):
    """Main Application Class"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "FinWise"
        
        # Configure theme for Material Design 3
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        
        # Custom colors matching the design
        self.theme_cls.colors = {
            "primary": "#14B8A6",  # Bright teal-green
            "on-primary": "#FFFFFF",
            "primary-container": "#CCFBF1",
            "on-primary-container": "#0F766E",
            "secondary": "#2DD4BF",  # Soft cyan
            "on-secondary": "#FFFFFF",
            "secondary-container": "#F0FDFA",
            "on-secondary-container": "#115E59",
            "background": "#F0FDFA",  # Very light mint
            "on-background": "#1F2937",
            "surface": "#FFFFFF",  # White cards
            "on-surface": "#1F2937",
            "error": "#EF4444",
            "on-error": "#FFFFFF",
        }
        
        self.db = None
        self.current_screen = None

    def build(self):
        """Build the application"""
        self.icon = "assets/icon.png" if hasattr(self, 'icon') else ""
        
        # Load all KV files
        Builder.load_file("screens/splash.kv")
        Builder.load_file("screens/dashboard.kv")
        Builder.load_file("screens/transactions.kv")
        Builder.load_file("screens/add_transaction.kv")
        Builder.load_file("screens/categories.kv")
        Builder.load_file("screens/accounts.kv")
        Builder.load_file("screens/analytics.kv")
        Builder.load_file("screens/settings.kv")
        Builder.load_file("main.kv")
        
        # Initialize database
        self.db = Database()
        init_db(self.db)
        
        return Builder.load_string("""
#:import FadeTransition kivy.uix.screenmanager.FadeTransition

ScreenManager:
    transition: FadeTransition()
    duration: 0.3
    
    SplashScreen:
    DashboardScreen:
    TransactionsScreen:
    AddTransactionScreen:
    CategoriesScreen:
    AccountsScreen:
    AnalyticsScreen:
    SettingsScreen:
""")

    def on_start(self):
        """Called when app starts"""
        # Populate demo data if first run
        if self.db.is_first_run():
            self.db.populate_demo_data()
        
        # Navigate to splash screen first
        self.root.current = "splash"

    def navigate_to(self, screen_name):
        """Navigate to a specific screen"""
        self.root.current = screen_name

    def get_balance(self):
        """Get total balance across all accounts"""
        if self.db:
            return self.db.get_total_balance()
        return 0.0

    def format_currency(self, amount):
        """Format amount as currency"""
        currency = self.db.get_currency() if self.db else "$"
        return f"{currency}{amount:,.2f}"


if __name__ == "__main__":
    FinWiseApp().run()
