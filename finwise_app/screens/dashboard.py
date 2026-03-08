"""
Dashboard Screen - Main screen with balance overview and quick actions
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.icon import MDIcon
from kivy.metrics import dp
from kivy.clock import Clock
from datetime import datetime


class DashboardScreen(MDScreen):
    def __init__(self, name="dashboard", db=None, app=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.db = db
        self.app = app
        self.md_bg_color = (0.96, 0.98, 1.0, 1)  # Very light mint/white
        
        # Build UI
        self.build_ui()
        
        # Schedule data refresh
        Clock.schedule_once(lambda dt: self.refresh_data(), 0.1)
    
    def build_ui(self):
        """Build the dashboard UI"""
        
        # Main scroll view
        from kivymd.uix.scrollview import MDScrollView
        scroll = MDScrollView(size_hint=(1, 1))
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical", padding=dp(16), spacing=dp(16), 
                                  size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Hero card with total balance
        hero_card = self.create_hero_card()
        main_layout.add_widget(hero_card)
        
        # Summary cards (Income/Expenses for month)
        summary_layout = self.create_summary_cards()
        main_layout.add_widget(summary_layout)
        
        # Quick actions
        quick_actions = self.create_quick_actions()
        main_layout.add_widget(quick_actions)
        
        # Recent transactions section
        recent_section = self.create_recent_transactions()
        main_layout.add_widget(recent_section)
        
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
    
    def create_hero_card(self):
        """Create hero card with total balance"""
        from kivymd.uix.card import MDCard
        
        card = MDCard(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(220),
            radius=[dp(24)],
            md_bg_color=(0.0, 0.75, 0.6, 1),  # Bright turquoise-green
        )
        
        # Title
        title_label = MDLabel(
            text="Total Balance",
            font_style="Body",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title_label)
        
        # Balance amount
        self.balance_label = MDLabel(
            text="$0.00",
            font_style="Headline",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            halign="center",
            size_hint_y=None,
            height=dp(60),
        )
        card.add_widget(self.balance_label)
        
        # Subtitle
        subtitle = MDLabel(
            text="All accounts combined",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.7),
            halign="center",
            size_hint_y=None,
            height=dp(20),
        )
        card.add_widget(subtitle)
        
        return card
    
    def create_summary_cards(self):
        """Create income and expense summary cards for the month"""
        from kivymd.uix.card import MDCard
        
        layout = MDBoxLayout(orientation="horizontal", spacing=dp(12), size_hint_y=None, height=dp(120))
        
        # Income card
        income_card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(8),
            size_hint_x=0.5,
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        income_icon = MDIcon(
            icon="arrow-down-left",
            font_size=dp(24),
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.4, 1),  # Green
            size_hint_y=None,
            height=dp(30),
        )
        income_card.add_widget(income_icon)
        
        self.income_label = MDLabel(
            text="$0.00",
            font_style="Title",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(35),
        )
        income_card.add_widget(self.income_label)
        
        income_desc = MDLabel(
            text="Income this month",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.6),
            size_hint_y=None,
            height=dp(20),
        )
        income_card.add_widget(income_desc)
        
        layout.add_widget(income_card)
        
        # Expense card
        expense_card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(8),
            size_hint_x=0.5,
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        expense_icon = MDIcon(
            icon="arrow-up-right",
            font_size=dp(24),
            theme_text_color="Custom",
            text_color=(1.0, 0.4, 0.3, 1),  # Coral red
            size_hint_y=None,
            height=dp(30),
        )
        expense_card.add_widget(expense_icon)
        
        self.expense_label = MDLabel(
            text="$0.00",
            font_style="Title",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(35),
        )
        expense_card.add_widget(expense_icon)
        expense_card.add_widget(self.expense_label)
        
        expense_desc = MDLabel(
            text="Expenses this month",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.6),
            size_hint_y=None,
            height=dp(20),
        )
        expense_card.add_widget(expense_desc)
        
        layout.add_widget(expense_card)
        
        return layout
    
    def create_quick_actions(self):
        """Create quick action buttons"""
        from kivymd.uix.card import MDCard
        
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
            text="Quick Actions",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title)
        
        # Buttons layout
        buttons_layout = MDBoxLayout(orientation="horizontal", spacing=dp(12))
        
        # Add Income button
        from kivymd.uix.button import MDButton, MDButtonText
        income_btn = MDButton(
            MDButtonText(text="Add Income"),
            size_hint_x=0.5,
            style="filled",
            on_release=lambda x: self.go_to_add_transaction("income"),
        )
        buttons_layout.add_widget(income_btn)
        
        # Add Expense button
        expense_btn = MDButton(
            MDButtonText(text="Add Expense"),
            size_hint_x=0.5,
            style="filled",
            on_release=lambda x: self.go_to_add_transaction("expense"),
        )
        buttons_layout.add_widget(expense_btn)
        
        card.add_widget(buttons_layout)
        
        return card
    
    def create_recent_transactions(self):
        """Create recent transactions list"""
        from kivymd.uix.card import MDCard
        
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(280),
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        # Header
        header_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30))
        
        title = MDLabel(
            text="Recent Transactions",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
        )
        header_layout.add_widget(title)
        
        # View all button
        from kivymd.uix.button import MDButton, MDButtonText
        view_all_btn = MDButton(
            MDButtonText(text="View All"),
            style="text",
            size_hint_x=None,
            width=dp(80),
            on_release=lambda x: self.go_to_transactions(),
        )
        header_layout.add_widget(view_all_btn)
        
        card.add_widget(header_layout)
        
        # Transactions list
        from kivymd.uix.list import MDList
        self.recent_list = MDList()
        card.add_widget(self.recent_list)
        
        return card
    
    def refresh_data(self):
        """Refresh all dashboard data"""
        if not self.db:
            return
        
        # Update total balance
        total_balance = self.db.get_total_balance()
        self.balance_label.text = self.app.format_currency(total_balance)
        
        # Update monthly summary
        monthly = self.db.get_monthly_summary()
        self.income_label.text = self.app.format_currency(monthly['income'])
        self.expense_label.text = self.app.format_currency(monthly['expenses'])
        
        # Update recent transactions
        self.update_recent_transactions()
    
    def update_recent_transactions(self):
        """Update recent transactions list"""
        self.recent_list.clear_widgets()
        
        transactions = self.db.get_transactions(limit=5)
        
        for trans in transactions:
            item = self.create_transaction_item(trans)
            self.recent_list.add_widget(item)
    
    def create_transaction_item(self, transaction):
        """Create a transaction list item"""
        from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
        
        # Transaction data: id, type, amount, category_id, account_id, note, date, category_name, category_icon, category_color, account_name
        trans_id = transaction[0]
        trans_type = transaction[1]
        amount = transaction[2]
        note = transaction[5] or "No description"
        date_str = transaction[6]
        category_name = transaction[7] or "Uncategorized"
        category_icon = transaction[8] or 'tag-outline'
        category_color = transaction[9] or '#00C49A'
        
        # Format date
        try:
            date_obj = datetime.strptime(date_str.split()[0], '%Y-%m-%d')
            formatted_date = date_obj.strftime('%b %d')
        except:
            formatted_date = date_str[:10]
        
        # Create item
        item = OneLineAvatarIconListItem(
            text=note[:40] + "..." if len(note) > 40 else note,
            secondary_text=f"{category_name} • {formatted_date}",
            height=dp(60),
        )
        
        # Add icon
        icon = IconLeftWidget(
            icon=category_icon,
            theme_text_color="Custom",
        )
        
        # Set icon color based on transaction type
        if trans_type == 'income':
            icon.text_color = (0.2, 0.8, 0.4, 1)
        else:
            icon.text_color = (1.0, 0.4, 0.3, 1)
        
        item.add_widget(icon)
        
        # Add amount label
        amount_label = MDLabel(
            text=self.app.format_currency(amount),
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0.2, 0.8, 0.4, 1) if trans_type == 'income' else (1.0, 0.4, 0.3, 1),
            halign="right",
            size_hint_x=None,
            width=dp(100),
        )
        item.add_widget(amount_label)
        
        return item
    
    def go_to_add_transaction(self, trans_type):
        """Navigate to add transaction screen"""
        if self.app.root:
            # Pass transaction type to the add screen
            add_screen = self.app.root.get_screen("add_transaction")
            if add_screen:
                add_screen.set_transaction_type(trans_type)
            self.app.root.current = "add_transaction"
    
    def go_to_transactions(self):
        """Navigate to transactions screen"""
        if self.app.root:
            self.app.root.current = "transactions"
