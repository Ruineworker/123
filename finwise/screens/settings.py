"""
Settings Screen Module
"""

from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import shutil
import os


class SettingsScreen(MDScreen):
    """Settings Screen"""
    
    def on_enter(self):
        """Called when screen is entered"""
        Clock.schedule_once(self.load_settings)
    
    def load_settings(self, dt=None):
        """Load current settings"""
        app = self.manager.get_running_app()
        if not app or not app.db:
            return
        
        # Load currency
        currency = app.db.get_currency()
        currency_spinner = self.ids.get("currency_spinner")
        if currency_spinner:
            currency_spinner.text = currency
        
        # Load theme
        theme = app.db.get_theme()
        theme_spinner = self.ids.get("theme_spinner")
        if theme_spinner:
            theme_spinner.text = theme.capitalize()
    
    def set_currency(self, currency):
        """Set currency"""
        app = self.manager.get_running_app()
        if app and app.db:
            app.db.set_currency(currency)
    
    def set_theme(self, theme):
        """Set theme"""
        app = self.manager.get_running_app()
        if app and app.db:
            app.db.set_theme(theme.lower())
    
    def backup_database(self):
        """Backup database to file"""
        app = self.manager.get_running_app()
        if not app or not app.db:
            return
        
        db_path = app.db.db_name
        backup_path = "finwise_backup.db"
        
        try:
            shutil.copy2(db_path, backup_path)
            self.show_dialog("Success", f"Database backed up to {backup_path}")
        except Exception as e:
            self.show_dialog("Error", f"Backup failed: {str(e)}")
    
    def reset_demo_data(self):
        """Reset demo data"""
        self.confirm_dialog = MDDialog(
            title="Reset Data",
            text="This will delete all your data and restore demo data. Continue?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=0.08, 0.72, 0.65, 1,
                    on_release=lambda x: self.confirm_dialog.dismiss()
                ),
                MDFlatButton(
                    text="RESET",
                    theme_text_color="Custom",
                    text_color=0.94, 0.27, 0.27, 1,
                    on_release=self.perform_reset
                ),
            ],
        )
        self.confirm_dialog.open()
    
    def perform_reset(self, obj):
        """Perform data reset"""
        self.confirm_dialog.dismiss()
        
        app = self.manager.get_running_app()
        if not app or not app.db:
            return
        
        try:
            # Close existing connection
            app.db.close()
            
            # Remove database file
            if os.path.exists(app.db.db_name):
                os.remove(app.db.db_name)
            
            # Reinitialize
            app.db = None
            from libs.database import Database
            from libs.models import init_db
            
            app.db = Database()
            init_db(app.db)
            app.db.populate_demo_data()
            
            self.show_dialog("Success", "Data has been reset to demo data")
        except Exception as e:
            self.show_dialog("Error", f"Reset failed: {str(e)}")
    
    def show_dialog(self, title, message):
        """Show info dialog"""
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=0.08, 0.72, 0.65, 1,
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def go_to_categories(self):
        """Navigate to categories screen"""
        self.manager.current = "categories"
    
    def go_to_accounts(self):
        """Navigate to accounts screen"""
        self.manager.current = "accounts"
