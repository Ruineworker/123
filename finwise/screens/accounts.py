"""
Accounts Screen Module
"""

from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarListItem, IconLeftWidget


class AccountsScreen(MDScreen):
    """Accounts Management Screen"""
    
    def on_enter(self):
        """Called when screen is entered"""
        Clock.schedule_once(self.load_accounts)
    
    def load_accounts(self, dt=None):
        """Load accounts into the list"""
        app = self.manager.get_running_app()
        if not app or not app.db:
            return
        
        container = self.ids.get("accounts_container")
        if not container:
            return
        
        # Clear existing items
        container.clear_widgets()
        
        # Get accounts
        accounts = app.db.get_accounts()
        total_balance = app.db.get_total_balance()
        
        # Update total balance label
        total_label = self.ids.get("total_balance_label")
        if total_label:
            total_label.text = f"Total: {app.format_currency(total_balance)}"
        
        for acc in accounts:
            item = self.create_account_item(acc, app)
            container.add_widget(item)
    
    def create_account_item(self, acc, app):
        """Create an account list item"""
        name = acc['name']
        balance = acc['balance']
        acc_type = acc['type']
        color = acc['color'] or '#14B8A6'
        icon = acc['icon'] or 'wallet'
        
        # Map account types to icons
        icon_map = {
            'cash': 'cash',
            'card': 'credit-card',
            'savings': 'piggy-bank',
            'electronic': 'wallet',
        }
        icon = icon_map.get(acc_type, icon)
        
        # Parse color
        r, g, b = self.hex_to_rgb(color)
        
        # Create item with secondary text for balance
        item = AccountListItem(
            text=name,
            secondary_text=app.format_currency(balance)
        )
        
        # Add icon with color
        icon_widget = IconLeftWidget(icon=icon)
        icon_widget.theme_text_color = "Custom"
        icon_widget.text_color = r, g, b, 1
        item.add_widget(icon_widget)
        
        return item
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    
    def show_add_dialog(self):
        """Show dialog to add new account"""
        self.dialog = MDDialog(
            title="Add Account",
            type="custom",
            content_cls=None,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=0.08, 0.72, 0.65, 1,
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="ADD",
                    theme_text_color="Custom",
                    text_color=0.08, 0.72, 0.65, 1,
                    on_release=self.add_account
                ),
            ],
        )
        self.dialog.open()
    
    def add_account(self, obj):
        """Add new account"""
        self.dialog.dismiss()


class AccountListItem(OneLineAvatarListItem):
    """Custom list item for accounts with balance"""
    
    def __init__(self, secondary_text="", **kwargs):
        super().__init__(**kwargs)
        self.secondary_text = secondary_text
