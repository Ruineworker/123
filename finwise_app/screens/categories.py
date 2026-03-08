"""
Categories Screen - Manage income and expense categories
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


class CategoriesScreen(MDScreen):
    def __init__(self, name="categories", db=None, app=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.db = db
        self.app = app
        self.md_bg_color = (0.96, 0.98, 1.0, 1)
        
        self.build_ui()
        Clock.schedule_once(lambda dt: self.refresh_data(), 0.1)
    
    def build_ui(self):
        """Build categories UI"""
        from kivymd.uix.scrollview import MDScrollView
        
        # Main layout
        main_layout = MDBoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        
        # Header
        header = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=dp(50))
        
        title = MDLabel(
            text="Categories",
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
            on_release=lambda x: self.show_add_category_dialog(),
        )
        header.add_widget(add_btn)
        
        main_layout.add_widget(header)
        
        # Segment control for Income/Expense
        segment_layout = MDBoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(45))
        
        self.expense_seg_btn = MDButton(
            MDButtonText(text="Expenses"),
            style="filled",
            size_hint_x=0.5,
            on_release=lambda x: self.show_categories('expense'),
        )
        segment_layout.add_widget(self.expense_seg_btn)
        
        self.income_seg_btn = MDButton(
            MDButtonText(text="Income"),
            style="outlined",
            size_hint_x=0.5,
            on_release=lambda x: self.show_categories('income'),
        )
        segment_layout.add_widget(self.income_seg_btn)
        
        main_layout.add_widget(segment_layout)
        
        # Categories grid
        scroll = MDScrollView(size_hint=(1, 1))
        self.categories_grid = MDBoxLayout(
            orientation="lr-tb",
            spacing=dp(12),
            padding=dp(4),
            size_hint_y=None,
        )
        self.categories_grid.bind(minimum_height=self.categories_grid.setter('height'))
        scroll.add_widget(self.categories_grid)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
        
        # Current filter
        self.current_type = 'expense'
    
    def show_categories(self, category_type):
        """Show categories by type"""
        self.current_type = category_type
        
        # Update segment buttons
        if category_type == 'expense':
            self.expense_seg_btn.style = "filled"
            self.income_seg_btn.style = "outlined"
        else:
            self.expense_seg_btn.style = "outlined"
            self.income_seg_btn.style = "filled"
        
        self.refresh_data()
    
    def refresh_data(self):
        """Refresh categories list"""
        if not self.db:
            return
        
        self.categories_grid.clear_widgets()
        
        categories = self.db.get_categories(category_type=self.current_type)
        
        for cat in categories:
            card = self.create_category_card(cat)
            self.categories_grid.add_widget(card)
    
    def create_category_card(self, category):
        """Create a category card"""
        cat_id, cat_name, cat_type, cat_icon, cat_color = category
        
        card = MDCard(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(8),
            size_hint_x=None,
            width=dp(110),
            height=dp(130),
            radius=[dp(16)],
            md_bg_color=(1, 1, 1, 1),
        )
        
        # Icon with background
        icon_container = MDBoxLayout(
            size_hint_y=None,
            height=dp(50),
            md_bg_color=tuple(int(cat_color[i:i+2], 16)/255.0 for i in (1, 3, 5)) + (0.15,),
            radius=[dp(12)],
        )
        
        icon = MDIcon(
            icon=cat_icon,
            font_size=dp(28),
            theme_text_color="Custom",
            text_color=tuple(int(cat_color[i:i+2], 16)/255.0 for i in (1, 3, 5)) + (1,),
            pos_hint={"center_x": 0.5},
        )
        icon_container.add_widget(icon)
        card.add_widget(icon_container)
        
        # Category name
        name_label = MDLabel(
            text=cat_name[:15] + "..." if len(cat_name) > 15 else cat_name,
            font_style="Subtitle",
            theme_text_color="Custom",
            text_color=(0, 0, 0, 0.9),
            halign="center",
            size_hint_y=None,
            height=dp(30),
        )
        card.add_widget(name_label)
        
        return card
    
    def show_add_category_dialog(self):
        """Show dialog to add new category"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.textfield import MDTextField
        from kivymd.uix.menu import MDDropdownMenu
        
        # Create input fields
        self.name_field = MDTextField(
            hint_text="Category Name",
            mode="rectangle",
            size_hint_x=1,
        )
        
        # Icon selector
        self.selected_icon = "tag-outline"
        self.icon_btn = MDButton(
            MDButtonText(text="Select Icon"),
            style="outlined",
            size_hint_x=1,
            on_release=lambda x: self.show_icon_menu(),
        )
        
        # Color selector (simplified - using preset colors)
        self.selected_color = "#00C49A"
        self.color_btn = MDButton(
            MDButtonText(text="Select Color"),
            style="outlined",
            size_hint_x=1,
            on_release=lambda x: self.show_color_menu(),
        )
        
        content_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12),
            size_hint_y=None,
            height=dp(220),
        )
        content_layout.add_widget(self.name_field)
        content_layout.add_widget(self.icon_btn)
        content_layout.add_widget(self.color_btn)
        
        self.add_dialog = MDDialog(
            title="Add Category",
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
                    on_release=lambda x: self.add_category(),
                ),
            ],
        )
        self.add_dialog.open()
    
    def show_icon_menu(self):
        """Show icon selection menu"""
        icons = [
            "food-variant", "car", "home-outline", "movie-outline", 
            "heart-pulse", "shopping-bag", "repeat", "lightning-bolt",
            "school", "cash", "laptop", "gift-outline", "trending-up",
            "tag-outline", "star", "coffee", "bus", "train", "plane",
        ]
        
        menu_items = []
        for icon in icons:
            menu_items.append({
                "text": icon,
                "on_release": lambda x, i=icon: self.select_icon(i),
            })
        
        self.icon_menu = MDDropdownMenu(items=menu_items, width_mult=4)
        self.icon_menu.open()
    
    def select_icon(self, icon):
        """Select an icon"""
        self.selected_icon = icon
        self.icon_btn.children[0].text = icon
        self.icon_menu.dismiss()
    
    def show_color_menu(self):
        """Show color selection menu"""
        colors = [
            ("#FF6B6B", "Red"),
            ("#4ECDC4", "Teal"),
            ("#45B7D1", "Blue"),
            ("#96CEB4", "Green"),
            ("#FFEAA7", "Yellow"),
            ("#DDA0DD", "Purple"),
            ("#74B9FF", "Light Blue"),
            ("#FAB1A0", "Orange"),
            ("#00C49A", "Turquoise"),
            ("#FD79A8", "Pink"),
        ]
        
        menu_items = []
        for color, name in colors:
            menu_items.append({
                "text": f"{name} ({color})",
                "on_release": lambda x, c=color: self.select_color(c),
            })
        
        self.color_menu = MDDropdownMenu(items=menu_items, width_mult=4)
        self.color_menu.open()
    
    def select_color(self, color):
        """Select a color"""
        self.selected_color = color
        self.color_btn.children[0].text = color
        self.color_menu.dismiss()
    
    def add_category(self):
        """Add new category"""
        name = self.name_field.text.strip()
        
        if not name:
            self.app.show_snackbar("Please enter a category name")
            return
        
        try:
            self.db.add_category(
                name=name,
                category_type=self.current_type,
                icon=self.selected_icon,
                color=self.selected_color
            )
            
            self.app.show_snackbar("Category added!")
            self.add_dialog.dismiss()
            self.refresh_data()
            
        except Exception as e:
            self.app.show_snackbar(f"Error: {str(e)}")
    
    def on_enter(self):
        """Called when screen is displayed"""
        self.refresh_data()
