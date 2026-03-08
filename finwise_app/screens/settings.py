"""
Settings Screen - App settings and preferences
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.clock import Clock


class SettingsScreen(MDScreen):
    def __init__(self, name="settings", db=None, app=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.db = db
        self.app = app
        self.md_bg_color = (0.96, 0.98, 1.0, 1)
        
        self.build_ui()
        Clock.schedule_once(lambda dt: self.refresh_data(), 0.1)
    
    def build_ui(self):
        """Build settings UI"""
        from kivymd.uix.scrollview import MDScrollView
        
        scroll = MDScrollView(size_hint=(1, 1))
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12), 
                                  size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Header
        header = MDLabel(
            text="Settings",
            font_style="Headline",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(40),
        )
        main_layout.add_widget(header)
        
        # Currency setting
        currency_card = self.create_currency_setting()
        main_layout.add_widget(currency_card)
        
        # Data management
        data_card = self.create_data_management()
        main_layout.add_widget(data_card)
        
        # About section
        about_card = self.create_about_section()
        main_layout.add_widget(about_card)
        
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
    
    def create_currency_setting(self):
        """Create currency setting card"""
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(130),
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        title = MDLabel(
            text="Currency",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title)
        
        self.currency_btn = MDButton(
            MDButtonText(text="USD"),
            style="outlined",
            size_hint_y=None,
            height=dp(56),
            on_release=lambda x: self.show_currency_menu(),
        )
        card.add_widget(self.currency_btn)
        
        return card
    
    def create_data_management(self):
        """Create data management card"""
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(180),
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        title = MDLabel(
            text="Data Management",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title)
        
        # Buttons layout
        buttons_layout = MDBoxLayout(orientation="vertical", spacing=dp(8))
        
        # Backup button
        backup_btn = MDButton(
            MDButtonText(text="Backup Database"),
            style="outlined",
            size_hint_y=None,
            height=dp(48),
            on_release=lambda x: self.backup_database(),
        )
        buttons_layout.add_widget(backup_btn)
        
        # Reset button
        reset_btn = MDButton(
            MDButtonText(text="Reset to Demo Data"),
            style="filled",
            size_hint_y=None,
            height=dp(48),
            on_release=lambda x: self.show_reset_confirmation(),
        )
        buttons_layout.add_widget(reset_btn)
        
        card.add_widget(buttons_layout)
        
        return card
    
    def create_about_section(self):
        """Create about section card"""
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(150),
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        title = MDLabel(
            text="About FinWise",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title)
        
        version_label = MDLabel(
            text="Version 1.0.0",
            font_style="Body",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.6),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(version_label)
        
        desc_label = MDLabel(
            text="A personal finance tracker built with Python and KivyMD",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.5),
            size_hint_y=None,
            height=dp(40),
        )
        card.add_widget(desc_label)
        
        return card
    
    def refresh_data(self):
        """Refresh settings data"""
        if not self.db:
            return
        
        # Get current currency
        currency = self.db.get_currency()
        self.currency_btn.children[0].text = currency
    
    def show_currency_menu(self):
        """Show currency selection menu"""
        currencies = ["USD", "EUR", "GBP", "JPY", "RUB", "CNY", "INR", "BRL"]
        
        menu_items = []
        for curr in currencies:
            menu_items.append({
                "text": curr,
                "on_release": lambda x, c=curr: self.select_currency(c),
            })
        
        self.currency_menu = MDDropdownMenu(items=menu_items, width_mult=3)
        self.currency_menu.open()
    
    def select_currency(self, currency):
        """Select a currency"""
        if self.db:
            self.db.update_settings(currency=currency)
            self.currency_btn.children[0].text = currency
            self.currency_menu.dismiss()
            self.app.show_snackbar(f"Currency set to {currency}")
    
    def backup_database(self):
        """Backup database"""
        try:
            import os
            from datetime import datetime
            
            backup_dir = os.path.expanduser("~")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"finwise_backup_{timestamp}.db")
            
            self.db.backup_database(backup_path)
            self.app.show_snackbar(f"Backup saved to {backup_path}")
            
        except Exception as e:
            self.app.show_snackbar(f"Backup failed: {str(e)}")
    
    def show_reset_confirmation(self):
        """Show reset confirmation dialog"""
        from kivymd.uix.dialog import MDDialog
        
        self.reset_dialog = MDDialog(
            title="Reset Data?",
            text="This will delete all your data and restore demo data. This action cannot be undone!",
            buttons=[
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                    on_release=lambda x: self.reset_dialog.dismiss(),
                ),
                MDButton(
                    MDButtonText(text="Reset"),
                    style="filled",
                    on_release=lambda x: self.reset_database(),
                ),
            ],
        )
        self.reset_dialog.open()
    
    def reset_database(self):
        """Reset database to demo state"""
        try:
            self.db.reset_database()
            self.reset_dialog.dismiss()
            self.app.show_snackbar("Database reset successfully!")
            self.refresh_data()
            
            # Refresh current screen if needed
            Clock.schedule_once(lambda dt: self.go_to_dashboard(), 0.5)
            
        except Exception as e:
            self.app.show_snackbar(f"Reset failed: {str(e)}")
    
    def go_to_dashboard(self):
        """Navigate to dashboard"""
        if self.app.root:
            self.app.root.current = "dashboard"
    
    def on_enter(self):
        """Called when screen is displayed"""
        self.refresh_data()
