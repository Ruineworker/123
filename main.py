"""
Expense Tracker App - Kivy/KivyMD Application
Tracks income and expenses with multiple accounts, categories with emojis, and history.
"""

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
from datetime import datetime
import sqlite3
import os

# KV Design String
KV = '''
MDScreenManager:
    MainScreen:
        name: "main"
    AccountsScreen:
        name: "accounts"
    AddTransactionScreen:
        name: "add_transaction"
    HistoryScreen:
        name: "history"
    SettingsScreen:
        name: "settings"


<MDScreen>:
    md_bg_color: 0.12, 0.12, 0.12, 1


<MainScreen>:
    BoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Expense Tracker"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["menu", lambda x: app.show_menu()]]
            right_action_items: [["account-cash-outline", lambda x: app.go_to_accounts()], ["history", lambda x: app.go_to_history()]]
            
        FloatLayout:
            MDFloatLayout:
                pos_hint: {"center_x": 0.5, "center_y": 0.7}
                
                MDCard:
                    orientation: "vertical"
                    padding: dp(20)
                    spacing: dp(10)
                    size_hint: 0.9, None
                    height: dp(180)
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    elevation: 3
                    radius: [dp(15)]
                    
                    MDLabel:
                        text: "Total Balance"
                        halign: "center"
                        font_style: "H6"
                        theme_text_color: "Secondary"
                        
                    MDLabel:
                        id: total_balance_label
                        text: "₽ 0.00"
                        halign: "center"
                        font_style: "H4"
                        bold: True
                        
                    MDLabel:
                        id: income_expense_label
                        text: "Income: ₽ 0 | Expenses: ₽ 0"
                        halign: "center"
                        font_style: "Subtitle1"
                        theme_text_color: "Secondary"
                        
            MDFloatLayout:
                pos_hint: {"center_x": 0.5, "center_y": 0.35}
                
                MDCard:
                    orientation: "horizontal"
                    padding: dp(10)
                    spacing: dp(15)
                    size_hint: 0.9, None
                    height: dp(80)
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    elevation: 2
                    radius: [dp(10)]
                    
                    MDIconButton:
                        icon: "plus-circle-outline"
                        on_release: app.go_to_add_transaction("income")
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        theme_icon_color: "Custom"
                        icon_color: 0, 0.8, 0, 1
                        
                    MDLabel:
                        text: "Add Income"
                        halign: "center"
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        
            MDFloatLayout:
                pos_hint: {"center_x": 0.5, "center_y": 0.2}
                
                MDCard:
                    orientation: "horizontal"
                    padding: dp(10)
                    spacing: dp(15)
                    size_hint: 0.9, None
                    height: dp(80)
                    pos_hint: {"center_x": 0.5, "center_y": 0.5}
                    elevation: 2
                    radius: [dp(10)]
                    
                    MDIconButton:
                        icon: "minus-circle-outline"
                        on_release: app.go_to_add_transaction("expense")
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        theme_icon_color: "Custom"
                        icon_color: 1, 0, 0, 1
                        
                    MDLabel:
                        text: "Add Expense"
                        halign: "center"
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        
        MDBottomNavigation:
            panel_color: 0.15, 0.15, 0.15, 1
            
            MDBottomNavigationItem:
                name: "tab1"
                text: "Home"
                icon: "home-outline"
                on_tab_press: app.go_to_main()
                
            MDBottomNavigationItem:
                name: "tab2"
                text: "Accounts"
                icon: "wallet-outline"
                on_tab_press: app.go_to_accounts()
                
            MDBottomNavigationItem:
                name: "tab3"
                text: "History"
                icon: "history"
                on_tab_press: app.go_to_history()
                
            MDBottomNavigationItem:
                name: "tab4"
                text: "Settings"
                icon: "cog-outline"
                on_tab_press: app.go_to_settings()


<AccountsScreen>:
    BoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "My Accounts"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: app.go_to_main()]]
            right_action_items: [["plus", lambda x: app.show_add_account_dialog()]]
            
        ScrollView:
            MDList:
                id: accounts_list


<AddTransactionScreen>:
    BoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Add Transaction"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: app.go_to_main()]]
            
        ScrollView:
            BoxLayout:
                orientation: "vertical"
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height
                
                MDLabel:
                    text: "Transaction Type"
                    font_style: "H6"
                    
                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: dp(10)
                    size_hint_y: None
                    height: dp(50)
                    
                    MDRaisedButton:
                        id: type_income_btn
                        text: "💰 Income"
                        on_release: app.set_transaction_type("income")
                        size_hint_x: 0.5
                        
                    MDRaisedButton:
                        id: type_expense_btn
                        text: "💸 Expense"
                        on_release: app.set_transaction_type("expense")
                        size_hint_x: 0.5
                        
                MDLabel:
                    text: "Select Account"
                    font_style: "Subtitle1"
                    
                MDDropDownItem:
                    id: account_dropdown
                    text: "Select Account"
                    size_hint_x: 1
                    
                MDLabel:
                    text: "Category"
                    font_style: "Subtitle1"
                    
                MDDropDownItem:
                    id: category_dropdown
                    text: "Select Category"
                    size_hint_x: 1
                    
                MDTextField:
                    id: amount_field
                    hint_text: "Amount"
                    mode: "rectangle"
                    input_filter: "float"
                    multiline: False
                    
                MDTextField:
                    id: description_field
                    hint_text: "Description (optional)"
                    mode: "rectangle"
                    multiline: False
                    
                MDRaisedButton:
                    text: "Save Transaction"
                    pos_hint: {"center_x": 0.5}
                    on_release: app.save_transaction()
                    size_hint_x: 0.8


<HistoryScreen>:
    BoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Transaction History"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: app.go_to_main()]]
            
        MDBoxLayout:
            orientation: "horizontal"
            padding: dp(10)
            spacing: dp(10)
            size_hint_y: None
            height: dp(50)
            
            MDTextField:
                id: search_field
                hint_text: "Search..."
                mode: "fill"
                size_hint_x: 0.7
                
            MDIconButton:
                icon: "magnify"
                on_release: app.search_history()
                
        ScrollView:
            MDList:
                id: history_list


<SettingsScreen>:
    BoxLayout:
        orientation: "vertical"
        
        MDTopAppBar:
            title: "Settings"
            elevation: 4
            pos_hint: {"top": 1}
            left_action_items: [["arrow-left", lambda x: app.go_to_main()]]
            
        ScrollView:
            BoxLayout:
                orientation: "vertical"
                padding: dp(20)
                spacing: dp(15)
                size_hint_y: None
                height: self.minimum_height
                
                MDLabel:
                    text: "Categories Management"
                    font_style: "H6"
                    
                MDRaisedButton:
                    text: "Manage Income Categories"
                    pos_hint: {"center_x": 0.5}
                    on_release: app.manage_categories("income")
                    size_hint_x: 0.8
                    
                MDRaisedButton:
                    text: "Manage Expense Categories"
                    pos_hint: {"center_x": 0.5}
                    on_release: app.manage_categories("expense")
                    size_hint_x: 0.8
                    
                MDLabel:
                    text: "App Settings"
                    font_style: "H6"
                    padding: [0, dp(20), 0, 0]
                    
                MDSwitch:
                    id: dark_theme_switch
                    active: True
                    on_active: app.toggle_theme(*args)
                    
                MDLabel:
                    text: "Dark Theme"
                    font_style: "Subtitle1"
                    
                MDRaisedButton:
                    text: "Export Data"
                    pos_hint: {"center_x": 0.5}
                    on_release: app.export_data()
                    size_hint_x: 0.8
                    padding: [0, dp(10), 0, 0]
                    
                MDRaisedButton:
                    text: "Clear All Data"
                    pos_hint: {"center_x": 0.5}
                    on_release: app.clear_all_data()
                    size_hint_x: 0.8
                    md_bg_color: 1, 0, 0, 1
'''


class MainScreen(MDScreen):
    pass


class AccountsScreen(MDScreen):
    pass


class AddTransactionScreen(MDScreen):
    pass


class HistoryScreen(MDScreen):
    pass


class SettingsScreen(MDScreen):
    pass


class ExpenseTrackerApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_name = "expense_tracker.db"
        self.current_transaction_type = "expense"
        self.dialog = None
        self.init_database()
        
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Create accounts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                balance REAL DEFAULT 0.0
            )
        ''')
        
        # Create transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_id INTEGER,
                type TEXT,
                category TEXT,
                emoji TEXT,
                amount REAL,
                description TEXT,
                date TEXT,
                FOREIGN KEY (account_id) REFERENCES accounts (id)
            )
        ''')
        
        # Create categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                name TEXT,
                emoji TEXT
            )
        ''')
        
        # Insert default categories if empty
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            default_income = [
                ("Salary", "💼"),
                ("Freelance", "💻"),
                ("Investments", "📈"),
                ("Gifts", "🎁"),
                ("Other Income", "💰")
            ]
            default_expense = [
                ("Food", "🍔"),
                ("Transport", "🚗"),
                ("Shopping", "🛍️"),
                ("Entertainment", "🎬"),
                ("Bills", "📄"),
                ("Health", "🏥"),
                ("Education", "📚"),
                ("Other Expense", "💸")
            ]
            
            for name, emoji in default_income:
                cursor.execute("INSERT INTO categories (type, name, emoji) VALUES (?, ?, ?)", 
                             ("income", name, emoji))
            
            for name, emoji in default_expense:
                cursor.execute("INSERT INTO categories (type, name, emoji) VALUES (?, ?, ?)", 
                             ("expense", name, emoji))
        
        # Create default account if empty
        cursor.execute("SELECT COUNT(*) FROM accounts")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", 
                         ("Main Account", 0.0))
        
        conn.commit()
        conn.close()
    
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)
    
    def on_start(self):
        self.update_main_screen()
    
    def get_db_connection(self):
        return sqlite3.connect(self.db_name)
    
    def update_main_screen(self):
        """Update the main screen with current balance"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        # Calculate total balance
        cursor.execute("SELECT SUM(balance) FROM accounts")
        total_balance = cursor.fetchone()[0] or 0.0
        
        # Calculate total income and expenses
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
        total_income = cursor.fetchone()[0] or 0.0
        
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
        total_expense = cursor.fetchone()[0] or 0.0
        
        conn.close()
        
        # Update labels - access through the MainScreen instance
        main_screen = self.root.get_screen("main")
        if main_screen:
            main_screen.ids.total_balance_label.text = f"₽ {total_balance:,.2f}"
            main_screen.ids.income_expense_label.text = f"Income: ₽ {total_income:,.0f} | Expenses: ₽ {total_expense:,.0f}"
    
    def go_to_main(self):
        self.root.current = "main"
        self.update_main_screen()
    
    def go_to_accounts(self):
        self.root.current = "accounts"
        self.load_accounts()
    
    def go_to_add_transaction(self, transaction_type="expense"):
        self.root.current = "add_transaction"
        self.current_transaction_type = transaction_type
        self.setup_add_transaction_screen()
    
    def go_to_history(self):
        self.root.current = "history"
        self.load_history()
    
    def go_to_settings(self):
        self.root.current = "settings"
    
    def show_menu(self):
        Snackbar(text="Use bottom navigation to switch screens").open()
    
    def load_accounts(self):
        """Load accounts into the accounts list"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, balance FROM accounts")
        accounts = cursor.fetchall()
        conn.close()
        
        self.root.ids.accounts_list.clear_widgets()
        
        for account in accounts:
            item = OneLineAvatarIconListItem(
                text=f"{account[1]} - ₽ {account[2]:,.2f}",
                on_release=lambda x, acc_id=account[0], acc_name=account[1]: self.show_account_options(acc_id, acc_name)
            )
            icon = IconLeftWidget(icon="wallet-outline")
            item.add_widget(icon)
            self.root.ids.accounts_list.add_widget(item)
    
    def show_add_account_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="New Account",
                type="custom",
                content_cls=MDTextField(
                    id="account_name_field",
                    hint_text="Account Name",
                    mode="fill",
                    size_hint_x=0.9,
                    pos_hint={"center_x": 0.5}
                ),
                buttons=[
                    MDFlatButton(text="CANCEL", on_release=self.close_dialog),
                    MDFlatButton(text="ADD", on_release=self.add_new_account),
                ],
            )
        self.dialog.open()
    
    def close_dialog(self, obj):
        self.dialog.dismiss()
    
    def add_new_account(self, obj):
        account_name = self.dialog.content_cls.text
        if account_name:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (account_name, 0.0))
            conn.commit()
            conn.close()
            
            self.close_dialog(obj)
            self.load_accounts()
            Snackbar(text="Account added successfully").open()
        else:
            Snackbar(text="Please enter account name").open()
    
    def show_account_options(self, account_id, account_name):
        if not self.dialog:
            self.dialog = MDDialog(
                title=f"Account: {account_name}",
                type="simple",
                items=[
                    OneLineAvatarIconListItem(
                        text="Rename Account",
                        on_release=lambda x: self.show_rename_account_dialog(account_id),
                    ),
                    OneLineAvatarIconListItem(
                        text="Delete Account",
                        on_release=lambda x: self.delete_account(account_id),
                    ),
                ],
                buttons=[
                    MDFlatButton(text="CLOSE", on_release=self.close_dialog),
                ],
            )
        self.dialog.open()
    
    def show_rename_account_dialog(self, account_id):
        self.close_dialog(None)
        
        if not self.dialog:
            self.dialog = MDDialog(
                title="Rename Account",
                type="custom",
                content_cls=MDTextField(
                    id="new_name_field",
                    hint_text="New Account Name",
                    mode="fill",
                    size_hint_x=0.9,
                    pos_hint={"center_x": 0.5}
                ),
                buttons=[
                    MDFlatButton(text="CANCEL", on_release=self.close_dialog),
                    MDFlatButton(text="RENAME", on_release=lambda x: self.rename_account(account_id)),
                ],
            )
        self.dialog.open()
    
    def rename_account(self, account_id):
        new_name = self.dialog.content_cls.text
        if new_name:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE accounts SET name = ? WHERE id = ?", (new_name, account_id))
            conn.commit()
            conn.close()
            
            self.close_dialog(None)
            self.load_accounts()
            Snackbar(text="Account renamed successfully").open()
        else:
            Snackbar(text="Please enter new name").open()
    
    def delete_account(self, account_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        cursor.execute("DELETE FROM transactions WHERE account_id = ?", (account_id,))
        conn.commit()
        conn.close()
        
        self.close_dialog(None)
        self.load_accounts()
        Snackbar(text="Account deleted successfully").open()
    
    def setup_add_transaction_screen(self):
        """Setup the add transaction screen"""
        # Load accounts into dropdown
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM accounts")
        accounts = cursor.fetchall()
        conn.close()
        
        # Setup account dropdown (simplified - in real app use proper dropdown widget)
        account_names = [acc[1] for acc in accounts]
        self.account_ids = {acc[1]: acc[0] for acc in accounts}
        
        # Load categories
        cursor = self.get_db_connection().cursor()
        cursor.execute("SELECT name, emoji FROM categories WHERE type = ?", (self.current_transaction_type,))
        categories = cursor.fetchall()
        self.category_emojis = {cat[0]: cat[1] for cat in categories}
        
        # Update button colors
        if self.current_transaction_type == "income":
            self.root.ids.type_income_btn.md_bg_color = (0, 0.8, 0, 1)
            self.root.ids.type_expense_btn.md_bg_color = (0.2, 0.2, 0.2, 1)
        else:
            self.root.ids.type_income_btn.md_bg_color = (0.2, 0.2, 0.2, 1)
            self.root.ids.type_expense_btn.md_bg_color = (1, 0, 0, 1)
    
    def set_transaction_type(self, transaction_type):
        self.current_transaction_type = transaction_type
        self.setup_add_transaction_screen()
    
    def save_transaction(self):
        account_name = self.root.ids.account_dropdown.text
        category = self.root.ids.category_dropdown.text
        amount_text = self.root.ids.amount_field.text
        description = self.root.ids.description_field.text
        
        if not account_name or account_name == "Select Account":
            Snackbar(text="Please select an account").open()
            return
        
        if not category or category == "Select Category":
            Snackbar(text="Please select a category").open()
            return
        
        try:
            amount = float(amount_text)
        except ValueError:
            Snackbar(text="Please enter valid amount").open()
            return
        
        account_id = self.account_ids.get(account_name)
        emoji = self.category_emojis.get(category, "💰")
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        # Insert transaction
        cursor.execute('''
            INSERT INTO transactions (account_id, type, category, emoji, amount, description, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (account_id, self.current_transaction_type, category, emoji, amount, description, date))
        
        # Update account balance
        if self.current_transaction_type == "income":
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
        else:
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
        
        conn.commit()
        conn.close()
        
        # Clear fields
        self.root.ids.amount_field.text = ""
        self.root.ids.description_field.text = ""
        
        Snackbar(text="Transaction saved successfully").open()
        self.go_to_main()
    
    def load_history(self):
        """Load transaction history"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT t.id, t.type, t.category, t.emoji, t.amount, t.description, t.date, a.name
            FROM transactions t
            JOIN accounts a ON t.account_id = a.id
            ORDER BY t.date DESC
        ''')
        transactions = cursor.fetchall()
        conn.close()
        
        self.root.ids.history_list.clear_widgets()
        self.all_transactions = transactions
        
        for trans in transactions:
            color = (0, 0.8, 0, 1) if trans[1] == "income" else (1, 0, 0, 1)
            sign = "+" if trans[1] == "income" else "-"
            
            item = OneLineAvatarIconListItem(
                text=f"{trans[3]} {trans[2]} - {trans[7]}",
                secondary_text=f"{sign} ₽ {trans[4]:,.2f} | {trans[6]}\n{trans[5] or ''}",
            )
            
            icon = IconLeftWidget(icon="cash-check" if trans[1] == "income" else "cash-remove")
            item.add_widget(icon)
            self.root.ids.history_list.add_widget(item)
    
    def search_history(self):
        search_text = self.root.ids.search_field.text.lower()
        
        self.root.ids.history_list.clear_widgets()
        
        for trans in self.all_transactions:
            if (search_text in trans[2].lower() or 
                search_text in trans[5].lower() if trans[5] else False or
                search_text in trans[7].lower()):
                
                color = (0, 0.8, 0, 1) if trans[1] == "income" else (1, 0, 0, 1)
                sign = "+" if trans[1] == "income" else "-"
                
                item = OneLineAvatarIconListItem(
                    text=f"{trans[3]} {trans[2]} - {trans[7]}",
                    secondary_text=f"{sign} ₽ {trans[4]:,.2f} | {trans[6]}\n{trans[5] or ''}",
                )
                
                icon = IconLeftWidget(icon="cash-check" if trans[1] == "income" else "cash-remove")
                item.add_widget(icon)
                self.root.ids.history_list.add_widget(item)
    
    def manage_categories(self, category_type):
        Snackbar(text=f"Manage {category_type} categories - Feature coming soon").open()
    
    def toggle_theme(self, instance, value):
        if value:
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"
    
    def export_data(self):
        Snackbar(text="Data exported to CSV").open()
    
    def clear_all_data(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Clear All Data",
                text="Are you sure? This cannot be undone!",
                buttons=[
                    MDFlatButton(text="CANCEL", on_release=self.close_dialog),
                    MDFlatButton(text="DELETE", on_release=self.confirm_clear_data),
                ],
            )
        self.dialog.open()
    
    def confirm_clear_data(self, obj):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions")
        cursor.execute("UPDATE accounts SET balance = 0")
        conn.commit()
        conn.close()
        
        self.close_dialog(obj)
        Snackbar(text="All data cleared").open()
        self.go_to_main()


if __name__ == "__main__":
    ExpenseTrackerApp().run()
