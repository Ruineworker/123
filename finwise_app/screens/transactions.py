"""
Transactions Screen - List of all transactions with filters
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.icon import MDIcon
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from kivy.clock import Clock
from datetime import datetime


class TransactionsScreen(MDScreen):
    def __init__(self, name="transactions", db=None, app=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.db = db
        self.app = app
        self.md_bg_color = (0.96, 0.98, 1.0, 1)
        self.current_filter = None
        self.search_text = ""
        
        self.build_ui()
        Clock.schedule_once(lambda dt: self.refresh_data(), 0.1)
    
    def build_ui(self):
        """Build transactions UI"""
        from kivymd.uix.scrollview import MDScrollView
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        
        # Header
        header = MDLabel(
            text="Transactions",
            font_style="Headline",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(40),
        )
        main_layout.add_widget(header)
        
        # Search bar
        self.search_field = MDTextField(
            hint_text="Search transactions...",
            mode="rectangle",
            size_hint_y=None,
            height=dp(50),
            radius=[dp(12)],
            on_text=lambda inst, text: self.on_search(text),
        )
        main_layout.add_widget(self.search_field)
        
        # Filter buttons
        filter_layout = MDBoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(40))
        
        # All filter
        all_btn = MDButton(
            MDButtonText(text="All"),
            style="filled" if not self.current_filter else "outlined",
            size_hint_x=0.33,
            on_release=lambda x: self.apply_filter(None),
        )
        filter_layout.add_widget(all_btn)
        
        # Income filter
        income_btn = MDButton(
            MDButtonText(text="Income"),
            style="filled" if self.current_filter == 'income' else "outlined",
            size_hint_x=0.33,
            on_release=lambda x: self.apply_filter('income'),
        )
        filter_layout.add_widget(income_btn)
        
        # Expense filter
        expense_btn = MDButton(
            MDButtonText(text="Expense"),
            style="filled" if self.current_filter == 'expense' else "outlined",
            size_hint_x=0.33,
            on_release=lambda x: self.apply_filter('expense'),
        )
        filter_layout.add_widget(expense_btn)
        
        main_layout.add_widget(filter_layout)
        
        # Scroll view for transactions
        scroll = MDScrollView(size_hint=(1, 1))
        self.transactions_list = MDList()
        scroll.add_widget(self.transactions_list)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def on_search(self, text):
        """Handle search input"""
        self.search_text = text
        self.refresh_data()
    
    def apply_filter(self, filter_type):
        """Apply transaction type filter"""
        self.current_filter = filter_type
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh transactions list"""
        if not self.db:
            return
        
        self.transactions_list.clear_widgets()
        
        transactions = self.db.get_transactions(
            transaction_type=self.current_filter,
            search=self.search_text if self.search_text else None
        )
        
        for trans in transactions:
            item = self.create_transaction_item(trans)
            self.transactions_list.add_widget(item)
    
    def create_transaction_item(self, transaction):
        """Create transaction list item"""
        from kivymd.uix.list import IconLeftWidget
        
        trans_id = transaction[0]
        trans_type = transaction[1]
        amount = transaction[2]
        note = transaction[5] or "No description"
        date_str = transaction[6]
        category_name = transaction[7] or "Uncategorized"
        category_icon = transaction[8] or 'tag-outline'
        
        # Format date
        try:
            date_obj = datetime.strptime(date_str.split()[0], '%Y-%m-%d')
            formatted_date = date_obj.strftime('%b %d, %Y')
        except:
            formatted_date = date_str[:10]
        
        # Truncate long text
        display_note = note[:35] + "..." if len(note) > 35 else note
        
        item = OneLineListItem(
            text=display_note,
            secondary_text=f"{category_name} • {formatted_date}",
            height=dp(65),
        )
        
        # Add icon
        icon = IconLeftWidget(
            icon=category_icon,
            theme_text_color="Custom",
        )
        
        if trans_type == 'income':
            icon.text_color = (0.2, 0.8, 0.4, 1)
        else:
            icon.text_color = (1.0, 0.4, 0.3, 1)
        
        item.add_widget(icon)
        
        # Add amount
        amount_label = MDLabel(
            text=self.app.format_currency(amount),
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.4, 1) if trans_type == 'income' else (1.0, 0.4, 0.3, 1),
            halign="right",
            size_hint_x=None,
            width=dp(110),
        )
        item.add_widget(amount_label)
        
        return item
    
    def on_enter(self):
        """Called when screen is displayed"""
        self.refresh_data()
