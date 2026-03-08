"""
Screen Manager - Handles navigation between screens
"""

from kivy.uix.screenmanager import ScreenManager, SlideTransition, FadeTransition
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineAvatarIconLeftWidget, IconLeftWidget
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock
from datetime import datetime

# Import all screens
from screens.dashboard import DashboardScreen
from screens.transactions import TransactionsScreen
from screens.add_transaction import AddTransactionScreen
from screens.categories import CategoriesScreen
from screens.accounts import AccountsScreen
from screens.analytics import AnalyticsScreen
from screens.settings import SettingsScreen


class CustomScreenManager(ScreenManager):
    """Custom screen manager with bottom navigation"""
    
    def __init__(self, db=None, app=None, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.app = app
        self.transition = FadeTransition()
        
        # Add all screens
        self.add_widget(DashboardScreen(name="dashboard", db=db, app=app))
        self.add_widget(TransactionsScreen(name="transactions", db=db, app=app))
        self.add_widget(AddTransactionScreen(name="add_transaction", db=db, app=app))
        self.add_widget(CategoriesScreen(name="categories", db=db, app=app))
        self.add_widget(AccountsScreen(name="accounts", db=db, app=app))
        self.add_widget(AnalyticsScreen(name="analytics", db=db, app=app))
        self.add_widget(SettingsScreen(name="settings", db=db, app=app))
    
    def go_to_screen(self, screen_name):
        """Navigate to a specific screen"""
        if self.has_screen(screen_name):
            self.current = screen_name
    
    def has_screen(self, name):
        """Check if screen exists"""
        return any(screen.name == name for screen in self.screens)


# Alias for compatibility
ScreenManager = CustomScreenManager
