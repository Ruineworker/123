"""
Accounts Screen - Manage accounts/wallets
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.icon import MDIcon
from kivy.metrics import dp
from kivy.clock import Clock


class AccountsScreen(MDScreen):
    def __init__(self, name="accounts", db=None, app=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.db = db
        self.app = app
        self.md_bg_color = (0.96, 0.98, 1.0, 1)
        
        self.build_ui()
        Clock.schedule_once(lambda dt: self.refresh_data(), 0.1)
    
    def build_ui(self):
        """Build accounts UI"""
        from kivymd.uix.scrollview import MDScrollView
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        
        # Header
        header = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50))
        
        title = MDLabel(
            text="Accounts",
            font_style="Headline",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
        )
        header.add_widget(title)
        
        # Add button
        add_btn = MDButton(
            MDButtonText(text="Add"),
            style="filled",
            size_hint_x=None,
            width=dp(80),
            on_release=lambda x: self.show_add_account_dialog(),
        )
        header.add_widget(add_btn)
        
        main_layout.add_widget(header)
        
        # Total balance card
        total_card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(130),
            radius=[dp(20)],
            md_bg_color=(0.0, 0.75, 0.6, 1),
        )
        
        total_label = MDLabel(
            text="Total Balance",
            font_style="Body",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        total_card.add_widget(total_label)
        
        self.total_balance_label = MDLabel(
            text="$0.00",
            font_style="Headline",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(50),
        )
        total_card.add_widget(self.total_balance_label)
        
        main_layout.add_widget(total_card)
        
        # Accounts list
        scroll = MDScrollView(size_hint=(1, 1))
        self.accounts_layout = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(4),
            size_hint_y=None,
        )
        self.accounts_layout.bind(minimum_height=self.accounts_layout.setter('height'))
        scroll.add_widget(self.accounts_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def refresh_data(self):
        """Refresh accounts list"""
        if not self.db:
            return
        
        self.accounts_layout.clear_widgets()
        
        # Update total balance
        total = self.db.get_total_balance()
        self.total_balance_label.text = self.app.format_currency(total)
        
        # Get all accounts
        accounts = self.db.get_accounts()
        
        for acc in accounts:
            card = self.create_account_card(acc)
            self.accounts_layout.add_widget(card)
    
    def create_account_card(self, account):
        """Create an account card"""
        acc_id, acc_name, acc_type, acc_balance, acc_color, acc_icon = account
        
        card = MDCard(
            orientation="horizontal",
            padding=dp(16),
            spacing=dp(16),
            size_hint_y=None,
            height=dp(100),
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        # Icon container
        icon_container = MDBoxLayout(
            size_hint_x=None,
            width=dp(60),
            md_bg_color=tuple(int(acc_color[i:i+2], 16)/255.0 for i in (1, 3, 5)) + (0.15,),
            radius=[dp(12)],
        )
        
        icon = MDIcon(
            icon=acc_icon,
            font_size=dp(32),
            theme_text_color="Custom",
            text_color=tuple(int(acc_color[i:i+2], 16)/255.0 for i in (1, 3, 5)) + (1,),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        icon_container.add_widget(icon)
        card.add_widget(icon_container)
        
        # Account info
        info_layout = MDBoxLayout(orientation="vertical", spacing=dp(4))
        
        name_label = MDLabel(
            text=acc_name,
            font_style="Title",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.9),
            size_hint_y=None,
            height=dp(30),
        )
        info_layout.add_widget(name_label)
        
        type_label = MDLabel(
            text=acc_type.capitalize(),
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.5),
            size_hint_y=None,
            height=dp(20),
        )
        info_layout.add_widget(type_label)
        
        card.add_widget(info_layout)
        
        # Balance
        balance_label = MDLabel(
            text=self.app.format_currency(acc_balance),
            font_style="Title",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            halign="right",
            size_hint_x=None,
            width=dp(120),
        )
        card.add_widget(balance_label)
        
        return card
    
    def show_add_account_dialog(self):
        """Show dialog to add new account"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.menu import MDDropdownMenu
        
        # Name field
        self.name_field = MDTextField(
            hint_text="Account Name",
            mode="rectangle",
            size_hint_x=1,
        )
        
        # Type selector
        self.selected_type = "cash"
        self.type_btn = MDButton(
            MDButtonText(text="Select Type"),
            style="outlined",
            size_hint_x=1,
            on_release=lambda x: self.show_type_menu(),
        )
        
        # Initial balance
        self.balance_field = MDTextField(
            hint_text="Initial Balance (optional)",
            mode="rectangle",
            keyboard_type="number",
            size_hint_x=1,
        )
        
        content_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(200),
        )
        content_layout.add_widget(self.name_field)
        content_layout.add_widget(self.type_btn)
        content_layout.add_widget(self.balance_field)
        
        self.add_dialog = MDDialog(
            title="Add Account",
            type="custom",
            content_cls=content_layout,
            buttons=[
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                    on_release=lambda x: self.add_dialog.dismiss(),
                ),
                MDButton(
                    MDButtonText(text="Add"),
                    style="filled",
                    on_release=lambda x: self.add_account(),
                ),
            ],
        )
        self.add_dialog.open()
    
    def show_type_menu(self):
        """Show account type menu"""
        types = [
            ("cash", "Cash"),
            ("bank", "Bank Account"),
            ("savings", "Savings"),
            ("electronic", "E-Wallet"),
            ("credit", "Credit Card"),
            ("investment", "Investment"),
        ]
        
        menu_items = []
        for type_val, type_name in types:
            menu_items.append({
                "text": type_name,
                "on_release": lambda x, t=type_val: self.select_type(t),
            })
        
        self.type_menu = MDDropdownMenu(items=menu_items, width_mult=4)
        self.type_menu.open()
    
    def select_type(self, acc_type):
        """Select account type"""
        self.selected_type = acc_type
        self.type_btn.children[0].text = acc_type.capitalize()
        self.type_menu.dismiss()
    
    def add_account(self):
        """Add new account"""
        name = self.name_field.text.strip()
        
        if not name:
            self.app.show_snackbar("Please enter an account name")
            return
        
        try:
            balance = float(self.balance_field.text) if self.balance_field.text else 0.0
        except ValueError:
            self.app.show_snackbar("Invalid balance amount")
            return
        
        # Generate color based on type
        colors = {
            'cash': '#00C49A',
            'bank': '#4A90E2',
            'savings': '#9B59B6',
            'electronic': '#F39C12',
            'credit': '#E74C3C',
            'investment': '#27AE60',
        }
        
        icons = {
            'cash': 'cash-multiple',
            'bank': 'credit-card',
            'savings': 'piggy-bank-outline',
            'electronic': 'cellphone-link',
            'credit': 'credit-card-clock',
            'investment': 'trending-up',
        }
        
        try:
            self.db.add_account(
                name=name,
                acc_type=self.selected_type,
                balance=balance,
                color=colors.get(self.selected_type, '#00C49A'),
                icon=icons.get(self.selected_type, 'wallet-outline')
            )
            
            self.app.show_snackbar("Account added!")
            self.add_dialog.dismiss()
            self.refresh_data()
            
        except Exception as e:
            self.app.show_snackbar(f"Error: {str(e)}")
    
    def on_enter(self):
        """Called when screen is displayed"""
        self.refresh_data()
