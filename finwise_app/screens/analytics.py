"""
Analytics Screen - Charts and analytics for income/expenses
"""

from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from kivy.clock import Clock
from datetime import datetime


class AnalyticsScreen(MDScreen):
    def __init__(self, name="analytics", db=None, app=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.db = db
        self.app = app
        self.md_bg_color = (0.96, 0.98, 1.0, 1)
        
        self.build_ui()
        Clock.schedule_once(lambda dt: self.refresh_data(), 0.1)
    
    def build_ui(self):
        """Build analytics UI"""
        from kivymd.uix.scrollview import MDScrollView
        
        scroll = MDScrollView(size_hint=(1, 1))
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12), 
                                  size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # Header
        header = MDLabel(
            text="Analytics",
            font_style="Headline",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=dp(40),
        )
        main_layout.add_widget(header)
        
        # Monthly summary
        summary_card = self.create_monthly_summary()
        main_layout.add_widget(summary_card)
        
        # Expenses by category
        expenses_card = self.create_expenses_by_category()
        main_layout.add_widget(expenses_card)
        
        # Income by category
        income_card = self.create_income_by_category()
        main_layout.add_widget(income_card)
        
        scroll.add_widget(main_layout)
        self.add_widget(scroll)
    
    def create_monthly_summary(self):
        """Create monthly summary card"""
        card = MDCard(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(16),
            size_hint_y=None,
            height=dp(180),
            radius=[dp(20)],
            md_bg_color=(0.0, 0.75, 0.6, 1),
        )
        
        # Title
        title = MDLabel(
            text="This Month",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.9),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title)
        
        # Summary layout
        summary_layout = MDBoxLayout(orientation="horizontal", spacing=dp(16))
        
        # Income
        income_layout = MDBoxLayout(orientation="vertical", spacing=dp(4), size_hint_x=0.5)
        
        income_label = MDLabel(
            text="Income",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.7),
            size_hint_y=None,
            height=dp(20),
        )
        income_layout.add_widget(income_label)
        
        self.monthly_income_label = MDLabel(
            text="$0.00",
            font_style="Title",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(35),
        )
        income_layout.add_widget(self.monthly_income_label)
        
        summary_layout.add_widget(income_layout)
        
        # Divider
        divider = MDLabel(
            text="|",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.3),
            halign="center",
            size_hint_x=None,
            width=dp(20),
        )
        summary_layout.add_widget(divider)
        
        # Expenses
        expense_layout = MDBoxLayout(orientation="vertical", spacing=dp(4), size_hint_x=0.5)
        
        expense_label = MDLabel(
            text="Expenses",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.7),
            size_hint_y=None,
            height=dp(20),
        )
        expense_layout.add_widget(expense_label)
        
        self.monthly_expense_label = MDLabel(
            text="$0.00",
            font_style="Title",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(35),
        )
        expense_layout.add_widget(expense_label)
        expense_layout.add_widget(self.monthly_expense_label)
        
        summary_layout.add_widget(expense_layout)
        
        card.add_widget(summary_layout)
        
        # Savings
        savings_layout = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30))
        
        savings_label = MDLabel(
            text="Savings:",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.8),
        )
        savings_layout.add_widget(savings_label)
        
        self.savings_label = MDLabel(
            text="$0.00",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            bold=True,
        )
        savings_layout.add_widget(self.savings_label)
        
        card.add_widget(savings_layout)
        
        return card
    
    def create_expenses_by_category(self):
        """Create expenses by category card"""
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(300),
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        title = MDLabel(
            text="Expenses by Category",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title)
        
        # Categories list
        from kivymd.uix.list import MDList
        self.expenses_list = MDList()
        card.add_widget(self.expenses_list)
        
        return card
    
    def create_income_by_category(self):
        """Create income by category card"""
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(250),
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        title = MDLabel(
            text="Income by Category",
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.8),
            size_hint_y=None,
            height=dp(24),
        )
        card.add_widget(title)
        
        from kivymd.uix.list import MDList
        self.income_list = MDList()
        card.add_widget(self.income_list)
        
        return card
    
    def refresh_data(self):
        """Refresh analytics data"""
        if not self.db:
            return
        
        # Get monthly summary
        now = datetime.now()
        monthly = self.db.get_monthly_summary(year=now.year, month=now.month)
        
        self.monthly_income_label.text = self.app.format_currency(monthly['income'])
        self.monthly_expense_label.text = self.app.format_currency(monthly['expenses'])
        self.savings_label.text = self.app.format_currency(monthly['savings'])
        
        # Get expenses by category
        self.expenses_list.clear_widgets()
        expenses = self.db.get_expenses_by_category()
        
        total_expenses = sum(cat[4] for cat in expenses) if expenses else 0
        
        for cat in expenses[:5]:  # Top 5 categories
            cat_id, cat_name, cat_icon, cat_color, cat_total = cat
            
            # Calculate percentage
            percentage = (cat_total / total_expenses * 100) if total_expenses > 0 else 0
            
            item = self.create_category_item(
                name=cat_name,
                icon=cat_icon,
                color=cat_color,
                amount=cat_total,
                percentage=percentage,
                is_income=False
            )
            self.expenses_list.add_widget(item)
        
        # Get income by category
        self.income_list.clear_widgets()
        incomes = self.db.get_income_by_category()
        
        total_income = sum(cat[4] for cat in incomes) if incomes else 0
        
        for cat in incomes[:5]:  # Top 5 categories
            cat_id, cat_name, cat_icon, cat_color, cat_total = cat
            
            percentage = (cat_total / total_income * 100) if total_income > 0 else 0
            
            item = self.create_category_item(
                name=cat_name,
                icon=cat_icon,
                color=cat_color,
                amount=cat_total,
                percentage=percentage,
                is_income=True
            )
            self.income_list.add_widget(item)
    
    def create_category_item(self, name, icon, color, amount, percentage, is_income=False):
        """Create a category list item with progress bar"""
        from kivymd.uix.list import OneLineListItem, IconLeftWidget
        from kivymd.uix.progressindicator import MDLinearProgressIndicator
        
        # Convert hex color to RGB
        rgb = tuple(int(color[i:i+2], 16)/255.0 for i in (1, 3, 5))
        
        item = OneLineListItem(
            text=name,
            secondary_text=f"{percentage:.1f}% • {self.app.format_currency(amount)}",
            height=dp(70),
        )
        
        # Add icon
        icon_widget = IconLeftWidget(
            icon=icon,
            theme_text_color="Custom",
            text_color=rgb + (1,),
        )
        item.add_widget(icon_widget)
        
        # Add amount on right
        amount_label = MDLabel(
            text=self.app.format_currency(amount),
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=rgb + (1,) if is_income else (1.0, 0.4, 0.3, 1),
            halign="right",
            size_hint_x=None,
            width=dp(100),
        )
        item.add_widget(amount_label)
        
        return item
    
    def on_enter(self):
        """Called when screen is displayed"""
        self.refresh_data()
