"""
Database Module - SQLite Operations
"""

import sqlite3
from datetime import datetime, timedelta
import os


class Database:
    """SQLite Database Handler"""
    
    def __init__(self, db_name="finwise.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
    
    def execute(self, query, params=None):
        """Execute a query"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()
        return self.cursor
    
    def fetchall(self):
        """Fetch all results"""
        return self.cursor.fetchall()
    
    def fetchone(self):
        """Fetch one result"""
        return self.cursor.fetchone()
    
    def close(self):
        """Close connection"""
        if self.conn:
            self.conn.close()
    
    def is_first_run(self):
        """Check if this is first run (no transactions exist)"""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM transactions")
            count = self.cursor.fetchone()[0]
            return count == 0
        except:
            return True
    
    def get_currency(self):
        """Get currency from settings"""
        try:
            self.cursor.execute("SELECT currency FROM settings WHERE id=1")
            result = self.cursor.fetchone()
            return result[0] if result else "$"
        except:
            return "$"
    
    def set_currency(self, currency):
        """Set currency in settings"""
        self.execute("UPDATE settings SET currency=? WHERE id=1", (currency,))
    
    def get_theme(self):
        """Get theme from settings"""
        try:
            self.cursor.execute("SELECT theme FROM settings WHERE id=1")
            result = self.cursor.fetchone()
            return result[0] if result else "light"
        except:
            return "light"
    
    def set_theme(self, theme):
        """Set theme in settings"""
        self.execute("UPDATE settings SET theme=? WHERE id=1", (theme,))
    
    # Account operations
    def create_account(self, name, account_type, balance=0.0, color="#14B8A6", icon="wallet"):
        """Create a new account"""
        self.execute(
            "INSERT INTO accounts (name, type, balance, color, icon) VALUES (?, ?, ?, ?, ?)",
            (name, account_type, balance, color, icon)
        )
        return self.cursor.lastrowid
    
    def get_accounts(self):
        """Get all accounts"""
        self.cursor.execute("SELECT * FROM accounts ORDER BY id")
        return self.fetchall()
    
    def get_account(self, account_id):
        """Get single account"""
        self.cursor.execute("SELECT * FROM accounts WHERE id=?", (account_id,))
        return self.fetchone()
    
    def update_account_balance(self, account_id, amount):
        """Update account balance"""
        self.execute("UPDATE accounts SET balance=balance+? WHERE id=?", (amount, account_id))
    
    def set_account_balance(self, account_id, balance):
        """Set account balance directly"""
        self.execute("UPDATE accounts SET balance=? WHERE id=?", (balance, account_id))
    
    def delete_account(self, account_id):
        """Delete account"""
        self.execute("DELETE FROM accounts WHERE id=?", (account_id,))
    
    def get_total_balance(self):
        """Get total balance across all accounts"""
        self.cursor.execute("SELECT SUM(balance) FROM accounts")
        result = self.cursor.fetchone()[0]
        return result if result else 0.0
    
    # Category operations
    def create_category(self, name, category_type, icon="tag", color="#14B8A6"):
        """Create a new category"""
        self.execute(
            "INSERT INTO categories (name, type, icon, color) VALUES (?, ?, ?, ?)",
            (name, category_type, icon, color)
        )
        return self.cursor.lastrowid
    
    def get_categories(self, category_type=None):
        """Get all categories or filtered by type"""
        if category_type:
            self.cursor.execute("SELECT * FROM categories WHERE type=? ORDER BY name", (category_type,))
        else:
            self.cursor.execute("SELECT * FROM categories ORDER BY name")
        return self.fetchall()
    
    def get_category(self, category_id):
        """Get single category"""
        self.cursor.execute("SELECT * FROM categories WHERE id=?", (category_id,))
        return self.fetchone()
    
    def update_category(self, category_id, name, icon, color):
        """Update category"""
        self.execute(
            "UPDATE categories SET name=?, icon=?, color=? WHERE id=?",
            (name, icon, color, category_id)
        )
    
    def delete_category(self, category_id):
        """Delete category"""
        self.execute("DELETE FROM categories WHERE id=?", (category_id,))
    
    # Transaction operations
    def create_transaction(self, trans_type, amount, category_id, account_id, note="", date=None):
        """Create a new transaction"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.execute(
            """INSERT INTO transactions 
               (type, amount, category_id, account_id, note, date_created) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            (trans_type, amount, category_id, account_id, note, date)
        )
        
        # Update account balance
        if trans_type == "income":
            self.update_account_balance(account_id, amount)
        else:
            self.update_account_balance(account_id, -amount)
        
        return self.cursor.lastrowid
    
    def get_transactions(self, limit=100, offset=0, filters=None):
        """Get transactions with optional filters"""
        query = """
            SELECT t.*, c.name as category_name, c.icon as category_icon, 
                   c.color as category_color, a.name as account_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            LEFT JOIN accounts a ON t.account_id = a.id
        """
        
        conditions = []
        params = []
        
        if filters:
            if filters.get('type'):
                conditions.append("t.type = ?")
                params.append(filters['type'])
            
            if filters.get('category_id'):
                conditions.append("t.category_id = ?")
                params.append(filters['category_id'])
            
            if filters.get('account_id'):
                conditions.append("t.account_id = ?")
                params.append(filters['account_id'])
            
            if filters.get('start_date'):
                conditions.append("t.date_created >= ?")
                params.append(filters['start_date'])
            
            if filters.get('end_date'):
                conditions.append("t.date_created <= ?")
                params.append(filters['end_date'])
            
            if filters.get('search'):
                conditions.append("t.note LIKE ?")
                params.append(f"%{filters['search']}%")
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY t.date_created DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        self.cursor.execute(query, params)
        return self.fetchall()
    
    def get_transaction(self, trans_id):
        """Get single transaction"""
        query = """
            SELECT t.*, c.name as category_name, c.icon as category_icon,
                   c.color as category_color, a.name as account_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            LEFT JOIN accounts a ON t.account_id = a.id
            WHERE t.id = ?
        """
        self.cursor.execute(query, (trans_id,))
        return self.fetchone()
    
    def update_transaction(self, trans_id, trans_type, amount, category_id, account_id, note, date):
        """Update transaction"""
        # Get old transaction to reverse balance change
        old_trans = self.get_transaction(trans_id)
        if old_trans:
            old_amount = old_trans['amount']
            old_account_id = old_trans['account_id']
            old_type = old_trans['type']
            
            # Reverse old balance change
            if old_type == "income":
                self.update_account_balance(old_account_id, -old_amount)
            else:
                self.update_account_balance(old_account_id, old_amount)
        
        # Update transaction
        self.execute(
            """UPDATE transactions 
               SET type=?, amount=?, category_id=?, account_id=?, note=?, date_created=?
               WHERE id=?""",
            (trans_type, amount, category_id, account_id, note, date, trans_id)
        )
        
        # Apply new balance change
        if trans_type == "income":
            self.update_account_balance(account_id, amount)
        else:
            self.update_account_balance(account_id, -amount)
    
    def delete_transaction(self, trans_id):
        """Delete transaction"""
        trans = self.get_transaction(trans_id)
        if trans:
            # Reverse balance change
            if trans['type'] == "income":
                self.update_account_balance(trans['account_id'], -trans['amount'])
            else:
                self.update_account_balance(trans['account_id'], trans['amount'])
        
        self.execute("DELETE FROM transactions WHERE id=?", (trans_id,))
    
    def get_monthly_summary(self, year=None, month=None):
        """Get monthly income and expenses summary"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        # Income
        self.cursor.execute(
            """SELECT COALESCE(SUM(amount), 0) FROM transactions 
               WHERE type='income' AND date_created >= ? AND date_created < ?""",
            (start_date, end_date)
        )
        income = self.cursor.fetchone()[0]
        
        # Expenses
        self.cursor.execute(
            """SELECT COALESCE(SUM(amount), 0) FROM transactions 
               WHERE type='expense' AND date_created >= ? AND date_created < ?""",
            (start_date, end_date)
        )
        expenses = self.cursor.fetchone()[0]
        
        return {
            'income': income,
            'expenses': expenses,
            'balance': income - expenses
        }
    
    def get_analytics_by_category(self, trans_type, year=None, month=None):
        """Get analytics grouped by category"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        start_date = f"{year}-{month:02d}-01"
        if month == 12:
            end_date = f"{year+1}-01-01"
        else:
            end_date = f"{year}-{month+1:02d}-01"
        
        query = """
            SELECT c.name, c.color, c.icon, COALESCE(SUM(t.amount), 0) as total
            FROM categories c
            LEFT JOIN transactions t ON c.id = t.category_id 
                AND t.type = ? AND t.date_created >= ? AND t.date_created < ?
            WHERE c.type = ?
            GROUP BY c.id
            ORDER BY total DESC
        """
        
        self.cursor.execute(query, (trans_type, start_date, end_date, trans_type))
        return self.fetchall()
    
    def get_monthly_trend(self, months=6):
        """Get monthly trend for analytics"""
        today = datetime.now()
        results = []
        
        for i in range(months - 1, -1, -1):
            date = today - timedelta(days=30*i)
            year = date.year
            month = date.month
            
            start_date = f"{year}-{month:02d}-01"
            if month == 12:
                end_date = f"{year+1}-01-01"
            else:
                end_date = f"{year}-{month+1:02d}-01"
            
            # Income
            self.cursor.execute(
                """SELECT COALESCE(SUM(amount), 0) FROM transactions 
                   WHERE type='income' AND date_created >= ? AND date_created < ?""",
                (start_date, end_date)
            )
            income = self.cursor.fetchone()[0]
            
            # Expenses
            self.cursor.execute(
                """SELECT COALESCE(SUM(amount), 0) FROM transactions 
                   WHERE type='expense' AND date_created >= ? AND date_created < ?""",
                (start_date, end_date)
            )
            expenses = self.cursor.fetchone()[0]
            
            results.append({
                'month': date.strftime("%b"),
                'income': income,
                'expenses': expenses
            })
        
        return results
    
    def populate_demo_data(self):
        """Populate database with demo data"""
        # Create default accounts
        accounts = [
            ("Cash", "cash", 500.0, "#14B8A6", "cash"),
            ("Main Card", "card", 2500.0, "#2DD4BF", "credit-card"),
            ("Savings", "savings", 5000.0, "#0D9488", "piggy-bank"),
            ("E-Wallet", "electronic", 750.0, "#115E59", "wallet"),
        ]
        
        for acc in accounts:
            self.create_account(*acc)
        
        # Create expense categories
        expense_categories = [
            ("Food", "expense", "food", "#F59E0B"),
            ("Transport", "expense", "bus", "#3B82F6"),
            ("Home", "expense", "home", "#8B5CF6"),
            ("Entertainment", "expense", "party", "#EC4899"),
            ("Health", "expense", "medical", "#EF4444"),
            ("Shopping", "expense", "cart", "#F97316"),
            ("Subscriptions", "expense", "repeat", "#6366F1"),
            ("Other", "expense", "tag", "#6B7280"),
        ]
        
        for cat in expense_categories:
            self.create_category(*cat)
        
        # Create income categories
        income_categories = [
            ("Salary", "income", "cash", "#14B8A6"),
            ("Freelance", "income", "briefcase", "#2DD4BF"),
            ("Gift", "income", "gift", "#F472B6"),
            ("Investments", "income", "trending-up", "#10B981"),
            ("Other", "income", "tag", "#6B7280"),
        ]
        
        for cat in income_categories:
            self.create_category(*cat)
        
        # Create sample transactions
        now = datetime.now()
        
        transactions = [
            ("income", 3500.0, 5, 2, "Monthly salary", (now - timedelta(days=5)).strftime("%Y-%m-%d")),
            ("expense", 45.50, 1, 1, "Grocery shopping", (now - timedelta(days=4)).strftime("%Y-%m-%d")),
            ("expense", 120.0, 2, 2, "Gas station", (now - timedelta(days=3)).strftime("%Y-%m-%d")),
            ("expense", 89.99, 6, 2, "New shoes", (now - timedelta(days=2)).strftime("%Y-%m-%d")),
            ("expense", 15.99, 7, 4, "Netflix subscription", (now - timedelta(days=1)).strftime("%Y-%m-%d")),
            ("income", 250.0, 6, 3, "Sold old items", (now - timedelta(days=1)).strftime("%Y-%m-%d")),
            ("expense", 65.00, 1, 1, "Restaurant dinner", now.strftime("%Y-%m-%d")),
            ("expense", 35.00, 2, 1, "Taxi rides", now.strftime("%Y-%m-%d")),
        ]
        
        for trans in transactions:
            self.create_transaction(*trans)
        
        # Set default settings
        self.execute("INSERT OR REPLACE INTO settings (id, currency, theme) VALUES (1, '$', 'light')")
