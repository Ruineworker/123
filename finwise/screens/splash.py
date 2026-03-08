"""
Splash Screen Module
"""

from kivy.clock import Clock
from kivy.animation import Animation
from kivymd.uix.screen import MDScreen


class SplashScreen(MDScreen):
    """Splash Screen with logo and app name"""
    
    def on_enter(self):
        """Called when screen is entered"""
        # Schedule navigation to dashboard after delay
        Clock.schedule_once(self.navigate_to_dashboard, 2.5)
    
    def navigate_to_dashboard(self, dt):
        """Navigate to dashboard screen"""
        self.manager.current = "dashboard"
