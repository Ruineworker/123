"""
Categories Screen Module
"""

from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineAvatarListItem, IconLeftWidget


class CategoriesScreen(MDScreen):
    """Categories Management Screen"""
    
    category_type = StringProperty("expense")
    
    def on_enter(self):
        """Called when screen is entered"""
        Clock.schedule_once(self.load_categories)
    
    def load_categories(self, dt=None):
        """Load categories into the list"""
        app = self.manager.get_running_app()
        if not app or not app.db:
            return
        
        container = self.ids.get("categories_container")
        if not container:
            return
        
        # Clear existing items
        container.clear_widgets()
        
        # Get categories
        categories = app.db.get_categories(self.category_type)
        
        for cat in categories:
            item = self.create_category_item(cat, app)
            container.add_widget(item)
    
    def create_category_item(self, cat, app):
        """Create a category list item"""
        name = cat['name']
        icon = cat['icon'] or 'tag'
        color = cat['color'] or '#6B7280'
        
        # Parse color
        r, g, b = self.hex_to_rgb(color)
        
        # Create item
        item = OneLineAvatarListItem(text=name)
        
        # Add icon with color
        icon_widget = IconLeftWidget(icon=icon)
        icon_widget.theme_text_color = "Custom"
        icon_widget.text_color = r, g, b, 1
        item.add_widget(icon_widget)
        
        return item
    
    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    
    def set_type(self, ctype):
        """Set category type"""
        self.category_type = ctype
        Clock.schedule_once(self.load_categories)
    
    def show_add_dialog(self):
        """Show dialog to add new category"""
        self.dialog = MDDialog(
            title="Add Category",
            type="custom",
            content_cls=None,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=(0.08, 0.72, 0.65, 1),
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDFlatButton(
                    text="ADD",
                    theme_text_color="Custom",
                    text_color=(0.08, 0.72, 0.65, 1),
                    on_release=self.add_category
                ),
            ],
        )
        self.dialog.open()
    
    def add_category(self, obj):
        """Add new category"""
        # This would need input fields in the dialog
        self.dialog.dismiss()
