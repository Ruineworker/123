"""
Add Transaction Screen - Form to add income or expense
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.clock import Clock
from datetime import datetime


class AddTransactionScreen(MDScreen):
    def __init__(self, name="add_transaction", db=None, app=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.db = db
        self.app = app
        self.md_bg_color = (0.96, 0.98, 1.0, 1)
        
        self.transaction_type = "expense"
        self.selected_category = None
        self.selected_account = None
        
        self.build_ui()
    
    def build_ui(self):
        """Build add transaction form"""
        from kivymd.uix.scrollview import MDScrollView
        
        scroll = MDScrollView(size_hint=(1, 1))
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical", padding=dp(20), spacing=dp(16), 
                                  size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Header
        header = MDLabel(
            text="Add Transaction",
            font_style="Headline",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(40),
        )
        main_layout.add_widget(header)
        
        # Type selector (Income/Expense)
        type_card = self.create_type_selector()
        main_layout.add_widget(type_card)
        
        # Amount input
        amount_card = self.create_amount_input()
        main_layout.add_widget(amount_card)
        
        # Category selector
        category_card = self.create_category_selector()
        main_layout.add_widget(category_card)
        
        # Account selector
        account_card = self.create_account_selector()
        main_layout.add_widget(account_card)
        
        # Date input
        date_card = self.create_date_input()
        main_layout.add_widget(date_card)
        
        # Note input
        note_card = self.create_note_input()
        main_layout.add_widget(note_card)
        
        # Save button
        save_btn = MDButton(
            MDButtonText(text="Save Transaction", font_size=dp(16)),
            size_hint_y=None,
            height=dp(56),
            style="filled",
            on_release=lambda x: self.save_transaction(),
        )
        main_layout.add_widget(save_btn)
        
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
    
    def create_type_selector(self):
        """Create income/expense type selector"""
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(100),
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        title = MDLabel(
            text="Transaction Type",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title)
        
        # Buttons layout
        buttons_layout = MDBoxLayout(orientation="horizontal", spacing=dp(12))
        
        # Income button
        self.income_btn = MDButton(
            MDButtonText(text="Income"),
            size_hint_x=0.5,
            style="filled" if self.transaction_type == 'income' else "outlined",
            on_release=lambda x: self.set_type('income'),
        )
        buttons_layout.add_widget(self.income_btn)
        
        # Expense button
        self.expense_btn = MDButton(
            MDButtonText(text="Expense"),
            size_hint_x=0.5,
            style="filled" if self.transaction_type == 'expense' else "outlined",
            on_release=lambda x: self.set_type('expense'),
        )
        buttons_layout.add_widget(self.expense_btn)
        
        card.add_widget(buttons_layout)
        
        return card
    
    def create_amount_input(self):
        """Create amount input field"""
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(110),
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        title = MDLabel(
            text="Amount",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title)
        
        self.amount_field = MDTextField(
            hint_text="0.00",
            mode="rectangle",
            keyboard_type="number",
            size_hint_y=None,
            height=dp(56),
            radius=[dp(12)],
            font_size=dp(24),
        )
        card.add_widget(self.amount_field)
        
        return card
    
    def create_category_selector(self):
        """Create category selector dropdown"""
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(110),
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        title = MDLabel(
            text="Category",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title)
        
        self.category_btn = MDButton(
            MDButtonText(text="Select Category"),
            size_hint_y=None,
            height=dp(56),
            style="outlined",
            on_release=lambda x: self.show_category_menu(),
        )
        card.add_widget(self.category_btn)
        
        return card
    
    def create_account_selector(self):
        """Create account selector dropdown"""
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(110),
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        title = MDLabel(
            text="Account",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title)
        
        self.account_btn = MDButton(
            MDButtonText(text="Select Account"),
            size_hint_y=None,
            height=dp(56),
            style="outlined",
            on_release=lambda x: self.show_account_menu(),
        )
        card.add_widget(self.account_btn)
        
        return card
    
    def create_date_input(self):
        """Create date input"""
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(110),
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        title = MDLabel(
            text="Date",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title)
        
        self.date_field = MDTextField(
            text=datetime.now().strftime('%Y-%m-%d'),
            hint_text="YYYY-MM-DD",
            mode="rectangle",
            size_hint_y=None,
            height=dp(56),
            radius=[dp(12)],
        )
        card.add_widget(self.date_field)
        
        return card
    
    def create_note_input(self):
        """Create note/description input"""
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
            text="Note (Optional)",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title)
        
        self.note_field = MDTextField(
            hint_text="Add a note...",
            mode="rectangle",
            multiline=True,
            size_hint_y=None,
            height=dp(70),
            radius=[dp(12)],
        )
        card.add_widget(self.note_field)
        
        return card
    
    def set_transaction_type(self, trans_type):
        """Set transaction type from outside"""
        self.transaction_type = trans_type
        self.update_type_buttons()
        self.update_category_menu()
    
    def set_type(self, trans_type):
        """Set transaction type"""
        self.transaction_type = trans_type
        self.update_type_buttons()
        self.update_category_menu()
    
    def update_type_buttons(self):
        """Update type button styles"""
        if self.transaction_type == 'income':
            self.income_btn.style = "filled"
            self.expense_btn.style = "outlined"
        else:
            self.income_btn.style = "outlined"
            self.expense_btn.style = "filled"
    
    def update_category_menu(self):
        """Update category menu based on type"""
        self.selected_category = None
        self.category_btn.children[0].text = "Select Category"
    
    def show_category_menu(self):
        """Show category selection menu"""
        if not self.db:
            return
        
        categories = self.db.get_categories(category_type=self.transaction_type)
        
        menu_items = []
        for cat in categories:
            cat_id, cat_name, cat_type, cat_icon, cat_color = cat
            menu_items.append({
                "text": cat_name,
                "on_release": lambda x, cid=cat_id, cname=cat_name: self.select_category(cid, cname),
            })
        
        self.category_menu = MDDropdownMenu(items=menu_items, width_mult=4)
        self.category_menu.open()
    
    def select_category(self, category_id, category_name):
        """Select a category"""
        self.selected_category = category_id
        self.category_btn.children[0].text = category_name
        self.category_menu.dismiss()
    
    def show_account_menu(self):
        """Show account selection menu"""
        if not self.db:
            return
        
        accounts = self.db.get_accounts()
        
        menu_items = []
        for acc in accounts:
            acc_id, acc_name, acc_type, acc_balance, acc_color, acc_icon = acc
            menu_items.append({
                "text": f"{acc_name} ({self.app.format_currency(acc_balance)})",
                "on_release": lambda x, aid=acc_id, aname=acc_name: self.select_account(aid, aname),
            })
        
        self.account_menu = MDDropdownMenu(items=menu_items, width_mult=4)
        self.account_menu.open()
    
    def select_account(self, account_id, account_name):
        """Select an account"""
        self.selected_account = account_id
        self.account_btn.children[0].text = account_name
        self.account_menu.dismiss()
    
    def save_transaction(self):
        """Save the transaction"""
        # Validate inputs
        try:
            amount = float(self.amount_field.text)
            if amount <= 0:
                self.app.show_snackbar("Amount must be greater than 0")
                return
        except ValueError:
            self.app.show_snackbar("Please enter a valid amount")
            return
        
        if not self.selected_category:
            self.app.show_snackbar("Please select a category")
            return
        
        if not self.selected_account:
            self.app.show_snackbar("Please select an account")
            return
        
        # Get date
        date_str = self.date_field.text
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError:
            self.app.show_snackbar("Invalid date format (use YYYY-MM-DD)")
            return
        
        # Get note
        note = self.note_field.text
        
        # Save to database
        try:
            self.db.add_transaction(
                transaction_type=self.transaction_type,
                amount=amount,
                category_id=self.selected_category,
                account_id=self.selected_account,
                note=note,
                date_created=date_str
            )
            
            self.app.show_snackbar("Transaction saved successfully!")
            
            # Clear form
            self.amount_field.text = ""
            self.note_field.text = ""
            self.selected_category = None
            self.category_btn.children[0].text = "Select Category"
            
            # Go back to dashboard
            Clock.schedule_once(lambda dt: self.go_to_dashboard(), 0.5)
            
        except Exception as e:
            self.app.show_snackbar(f"Error: {str(e)}")
    
    def go_to_dashboard(self):
        """Navigate to dashboard"""
        if self.app.root:
            self.app.root.current = "dashboard"
    
    def on_enter(self):
        """Called when screen is displayed"""
        # Reset form
        self.amount_field.text = ""
        self.note_field.text = ""
        self.date_field.text = datetime.now().strftime('%Y-%m-%d')
        self.selected_category = None
        self.selected_account = None
        self.category_btn.children[0].text = "Select Category"
        self.account_btn.children[0].text = "Select Account"
