"""
FinWise - Personal Finance Tracker
Main Application Entry Point
"""

from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.utils import platform
from kivy.metrics import dp
from libs.database import Database
from screens.manager import ScreenManager
import os

# Set window size for desktop testing
if platform not in ('android', 'ios'):
    Window.size = (412, 915)  # Pixel-like dimensions
    Window.minimum_width = 360
    Window.minimum_height = 640

KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition
#:import SlideTransition kivy.uix.screenmanager.SlideTransition
#:import SwapTransition kivy.uix.screenmanager.SwapTransition

MDScreen:
    md_bg_color: app.theme_cls.bg_darkest
    
    ScreenManager:
        id: screen_manager
        transition: FadeTransition()
        
        MDScreen:
            name: "splash"
            md_bg_color: app.theme_cls.bg_darkest
            
            MDFloatLayout:
                MDBoxLayout:
                    orientation: "vertical"
                    size_hint: None, None
                    size: dp(200), dp(200)
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    
                    MDIcon:
                        icon: "wallet-outline"
                        halign: "center"
                        font_size: dp(80)
                        theme_text_color: "Custom"
                        text_color: app.primary_color
                        size_hint: None, None
                        size: dp(100), dp(100)
                        pos_hint: {"center_x": 0.5}
                    
                    MDLabel:
                        text: "FinWise"
                        halign: "center"
                        font_style: "H4"
                        theme_text_color: "Custom"
                        text_color: 1, 1, 1, 1
                        size_hint_y: None
                        height: self.texture_size[1]
'''

class FinWiseApp(MDApp):
    primary_color = (0.0, 0.75, 0.6, 1)  # Bright turquoise-green
    secondary_color = (0.2, 0.6, 0.9, 1)  # Soft blue
    accent_color = (1.0, 0.4, 0.3, 1)  # Coral for expenses
    success_color = (0.2, 0.8, 0.4, 1)  # Green for income
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = None
        self.title = "FinWise"
        
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette = "LightBlue"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.material_style = "M3"
        
        # Load main KV
        Builder.load_string(KV)
        
        # Initialize database
        self.db = Database()
        self.db.initialize()
        
        # Create screen manager with all screens
        self.root = ScreenManager(db=self.db, app=self)
        
        return self.root
    
    def on_start(self):
        # Navigate to dashboard after splash
        from kivy.clock import Clock
        Clock.schedule_once(self.go_to_dashboard, 2.0)
    
    def go_to_dashboard(self, dt):
        self.root.go_to_screen("dashboard")
    
    def format_currency(self, amount):
        """Format amount as currency"""
        try:
            amount = float(amount)
            currency = self.db.get_currency()
            if currency == "USD":
                return f"${amount:,.2f}"
            elif currency == "EUR":
                return f"€{amount:,.2f}"
            elif currency == "GBP":
                return f"£{amount:,.2f}"
            elif currency == "JPY":
                return f"¥{amount:,.0f}"
            elif currency == "RUB":
                return f"₽{amount:,.2f}"
            else:
                return f"{amount:,.2f} {currency}"
        except:
            return f"{amount}"
    
    def show_snackbar(self, text, is_error=False):
        """Show snackbar notification"""
        from kivymd.toast import toast
        toast(text)


if __name__ == "__main__":
    FinWiseApp().run()
