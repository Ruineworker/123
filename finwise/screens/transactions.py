"""
Transactions Screen Module
"""

from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarIconicListItem, IconLeftWidget


class TransactionsScreen(MDScreen):
    """Transactions List Screen"""
    
    search_text = StringProperty("")
    filter_type = StringProperty("all")
    
    def on_enter(self):
        """Called when screen is entered"""
        Clock.schedule_once(self.load_transactions)
    
    def load_transactions(self, dt=None):
        """Load transactions into the list"""
        app = self.manager.get_running_app()
        if not app or not app.db:
            return
        
        container = self.ids.get("transactions_container")
        if not container:
            return
        
        # Clear existing items
        container.clear_widgets()
        
        # Build filters
        filters = {}
        if self.filter_type != "all":
            filters['type'] = self.filter_type
        
        if self.search_text:
            filters['search'] = self.search_text
        
        # Get transactions
        transactions = app.db.get_transactions(limit=50, filters=filters)
        
        for trans in transactions:
            item = self.create_transaction_item(trans, app)
            container.add_widget(item)
    
    def create_transaction_item(self, trans, app):
        """Create a transaction list item"""
        amount = trans['amount']
        trans_type = trans['type']
        category_name = trans['category_name'] or 'Uncategorized'
        date = trans['date_created'].split(' ')[0]
        note = trans['note'] or ''
        color = trans['category_color'] or '#6B7280'
        icon = trans['category_icon'] or 'tag'
        
        # Parse color
        r, g, b = self.hex_to_rgb(color)
        
        # Create item
        item = TransactionListItem(
            text=category_name,
            secondary_text=f"{date} | {note}" if note else date,
        )
        
        # Add icon with color
        icon_widget = IconLeftWidget(icon=icon)
        icon_widget.theme_text_color = "Custom"
        icon_widget.text_color = r, g, b, 1
        item.add_widget(icon_widget)
        
        # Add amount label
        amount_label = TransactionAmountLabel(
            text=f"{'+' if trans_type == 'income' else '-'}{app.format_currency(amount)}",
            trans_type=trans_type
        )
        item.add_widget(amount_label)
        
        return item
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    
    def on_search_text(self, instance, value):
        """Handle search text change"""
        Clock.schedule_once(self.load_transactions, 0.3)
    
    def set_filter(self, filter_type):
        """Set transaction filter"""
        self.filter_type = filter_type
        Clock.schedule_once(self.load_transactions)
    
    def refresh_transactions(self):
        """Refresh transactions list"""
        self.load_transactions()


class TransactionListItem(OneLineAvatarIconicListItem):
    """Custom list item for transactions"""
    
    def __init__(self, secondary_text="", **kwargs):
        super().__init__(**kwargs)
        self.secondary_text = secondary_text


class TransactionAmountLabel(MDScreen):
    """Amount label widget"""
    
    def __init__(self, text="", trans_type="expense", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.trans_type = trans_type
