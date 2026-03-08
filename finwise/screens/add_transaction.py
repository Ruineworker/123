"""
Add Transaction Screen Module
"""

from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from datetime import datetime


class AddTransactionScreen(MDScreen):
    """Add/Edit Transaction Screen"""
    
    transaction_type = StringProperty("expense")
    categories_list = ListProperty([])
    accounts_list = ListProperty([])
    selected_category_id = None
    selected_account_id = None
    editing_transaction_id = None
    
    def on_enter(self):
        """Called when screen is entered"""
        Clock.schedule_once(self.load_data)
    
    def load_data(self, dt=None):
        """Load categories and accounts"""
        app = self.manager.get_running_app()
        if not app or not app.db:
            return
        
        # Load categories based on type
        categories = app.db.get_categories(self.transaction_type)
        self.categories_list = [
            {"id": cat['id'], "name": cat['name'], "icon": cat['icon'], "color": cat['color']}
            for cat in categories
        ]
        
        # Select first category by default
        if self.categories_list and self.selected_category_id is None:
            self.selected_category_id = self.categories_list[0]['id']
        
        # Load accounts
        accounts = app.db.get_accounts()
        self.accounts_list = [
            {"id": acc['id'], "name": acc['name'], "balance": acc['balance']}
            for acc in accounts
        ]
        
        # Select first account by default
        if self.accounts_list and self.selected_account_id is None:
            self.selected_account_id = self.accounts_list[0]['id']
        
        # Update UI
        self.update_category_buttons()
        self.update_account_spinner()
    
    def set_transaction_type(self, trans_type):
        """Set transaction type (income/expense)"""
        self.transaction_type = trans_type
        self.selected_category_id = None
        self.selected_account_id = None
        # Reset form fields
        self.ids.amount_input.text = ""
        self.ids.note_input.text = ""
        self.ids.date_input.text = datetime.now().strftime("%Y-%m-%d")
        # Reload data for new type
        Clock.schedule_once(self.load_data)
    
    def update_category_buttons(self):
        """Update category selection buttons"""
        container = self.ids.get("categories_container")
        if not container:
            return
        
        container.clear_widgets()
        
        for cat in self.categories_list:
            btn = MDCategoryButton(
                text=cat['name'],
                icon=cat['icon'],
                color=cat['color'],
                category_id=cat['id'],
                selected=(cat['id'] == self.selected_category_id)
            )
            btn.bind(on_release=lambda x, cid=cat['id']: self.select_category(cid))
            container.add_widget(btn)
    
    def update_account_spinner(self):
        """Update account spinner"""
        spinner = self.ids.get("account_spinner")
        if not spinner:
            return
        
        account_names = [acc['name'] for acc in self.accounts_list]
        spinner.values = account_names
        
        if self.selected_account_id and self.accounts_list:
            for i, acc in enumerate(self.accounts_list):
                if acc['id'] == self.selected_account_id:
                    spinner.text = acc['name']
                    break
    
    def select_category(self, category_id):
        """Select a category"""
        self.selected_category_id = category_id
        self.update_category_buttons()
    
    def on_account_spinner(self, instance, value):
        """Handle account selection"""
        for acc in self.accounts_list:
            if acc['name'] == value:
                self.selected_account_id = acc['id']
                break
    
    def save_transaction(self):
        """Save the transaction"""
        app = self.manager.get_running_app()
        if not app or not app.db:
            return
        
        # Validate inputs
        amount_text = self.ids.amount_input.text.strip()
        if not amount_text:
            self.show_error("Please enter an amount")
            return
        
        try:
            amount = float(amount_text)
            if amount <= 0:
                self.show_error("Amount must be greater than 0")
                return
        except ValueError:
            self.show_error("Invalid amount format")
            return
        
        if not self.selected_category_id:
            self.show_error("Please select a category")
            return
        
        if not self.selected_account_id:
            self.show_error("Please select an account")
            return
        
        note = self.ids.note_input.text.strip()
        date = self.ids.date_input.text.strip()
        
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        # Save transaction
        if self.editing_transaction_id:
            # Update existing
            app.db.update_transaction(
                self.editing_transaction_id,
                self.transaction_type,
                amount,
                self.selected_category_id,
                self.selected_account_id,
                note,
                date
            )
        else:
            # Create new
            app.db.create_transaction(
                self.transaction_type,
                amount,
                self.selected_category_id,
                self.selected_account_id,
                note,
                date
            )
        
        # Navigate back
        self.manager.current = "dashboard"
    
    def show_error(self, message):
        """Show error dialog"""
        dialog = MDDialog(
            title="Error",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=(0.08, 0.72, 0.65, 1),
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
    
    def clear_form(self):
        """Clear the form"""
        self.ids.amount_input.text = ""
        self.ids.note_input.text = ""
        self.ids.date_input.text = datetime.now().strftime("%Y-%m-%d")
        self.selected_category_id = None
        self.selected_account_id = None
        self.editing_transaction_id = None
        self.load_data()


class MDCategoryButton(MDScreen):
    """Category selection button widget"""
    
    def __init__(self, text="", icon="", color="#14B8A6", category_id=None, selected=False, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.icon = icon
        self.color = color
        self.category_id = category_id
        self.selected = selected
