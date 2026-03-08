"""
Database Module - SQLite Database Management
Handles all database operations for accounts, categories, transactions, and settings
"""

import sqlite3
from datetime import datetime, timedelta
import os
from kivy.metrics import dp


class Database:
    def __init__(self, db_name="finwise.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        
        # Get the directory where the app is running
        if hasattr(os, 'getenv') and os.getenv('KIVY_ROOT'):
            # Android environment
            from android.storage import app_storage_path
            self.db_path = os.path.join(app_storage_path(), db_name)
        else:
            # Desktop environment
            self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", db_name)
            self.db_path = os.path.abspath(self.db_path)
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def initialize(self):
        """Initialize database tables and demo data"""
        self.connect()
        
        # Create tables
        self.create_tables()
        
        # Check if demo data exists
        self.cursor.execute("SELECT COUNT(*) FROM settings")
        count = self.cursor.fetchone()[0]
        
        if count == 0:
            self.insert_demo_data()
        
        self.close()
    
    def create_tables(self):
        """Create all database tables"""
        
        # Accounts table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT DEFAULT 'cash',
                balance REAL DEFAULT 0.0,
                color TEXT DEFAULT '#00C49A',
                icon TEXT DEFAULT 'wallet-outline',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Categories table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                icon TEXT DEFAULT 'tag-outline',
                color TEXT DEFAULT '#00C49A',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Transactions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                category_id INTEGER,
                account_id INTEGER NOT NULL,
                note TEXT,
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id),
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            )
        ''')
        
        # Settings table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency TEXT DEFAULT 'USD',
                theme TEXT DEFAULT 'light'
            )
        ''')
        
        self.conn.commit()
    
    def insert_demo_data(self):
        """Insert demo data for first-time users"""
        
        # Insert default settings
        self.cursor.execute("INSERT INTO settings (currency, theme) VALUES (?, ?)", 
                          ('USD', 'light'))
        
        # Insert demo accounts
        accounts = [
            ('Cash', 'cash', 500.0, '#00C49A', 'cash-multiple'),
            ('Bank Card', 'bank', 2500.0, '#4A90E2', 'credit-card'),
            ('Savings', 'savings', 5000.0, '#9B59B6', 'piggy-bank-outline'),
            ('E-Wallet', 'electronic', 300.0, '#F39C12', 'cellphone-link'),
        ]
        
        for acc in accounts:
            self.cursor.execute('''
                INSERT INTO accounts (name, type, balance, color, icon)
                VALUES (?, ?, ?, ?, ?)
            ''', acc)
        
        # Insert expense categories
        expense_categories = [
            ('Food', 'expense', 'food-variant', '#FF6B6B'),
            ('Transport', 'expense', 'car', '#4ECDC4'),
            ('Home', 'expense', 'home-outline', '#45B7D1'),
            ('Entertainment', 'expense', 'movie-outline', '#96CEB4'),
            ('Health', 'expense', 'heart-pulse', '#FFEAA7'),
            ('Shopping', 'expense', 'shopping-bag', '#DDA0DD'),
            ('Subscriptions', 'expense', 'repeat', '#74B9FF'),
            ('Utilities', 'expense', 'lightning-bolt', '#FAB1A0'),
            ('Education', 'expense', 'school', '#81ECEC'),
            ('Other', 'expense', 'dots-horizontal', '#B2BEC3'),
        ]
        
        for cat in expense_categories:
            self.cursor.execute('''
                INSERT INTO categories (name, type, icon, color)
                VALUES (?, ?, ?, ?)
            ''', cat)
        
        # Insert income categories
        income_categories = [
            ('Salary', 'income', 'cash', '#00C49A'),
            ('Freelance', 'income', 'laptop', '#00B894'),
            ('Gift', 'income', 'gift-outline', '#FD79A8'),
            ('Investments', 'income', 'trending-up', '#0984E3'),
            ('Other', 'income', 'plus-circle', '#636E72'),
        ]
        
        for cat in income_categories:
            self.cursor.execute('''
                INSERT INTO categories (name, type, icon, color)
                VALUES (?, ?, ?, ?)
            ''', cat)
        
        # Insert demo transactions
        today = datetime.now()
        
        demo_transactions = [
            ('income', 3000.0, 11, 2, 'Monthly salary', (today - timedelta(days=1)).strftime('%Y-%m-%d')),
            ('expense', 45.50, 1, 1, 'Grocery shopping', (today - timedelta(days=1)).strftime('%Y-%m-%d')),
            ('expense', 120.0, 2, 2, 'Gas station', (today - timedelta(days=2)).strftime('%Y-%m-%d')),
            ('expense', 89.99, 7, 2, 'Netflix subscription', (today - timedelta(days=3)).strftime('%Y-%m-%d')),
            ('expense', 250.0, 3, 2, 'Electric bill', (today - timedelta(days=4)).strftime('%Y-%m-%d')),
            ('income', 500.0, 12, 2, 'Freelance project', (today - timedelta(days=5)).strftime('%Y-%m-%d')),
            ('expense', 35.0, 1, 1, 'Restaurant', (today - timedelta(days=6)).strftime('%Y-%m-%d')),
            ('expense', 199.99, 6, 2, 'New shoes', (today - timedelta(days=7)).strftime('%Y-%m-%d')),
            ('expense', 15.0, 4, 1, 'Movie tickets', (today - timedelta(days=8)).strftime('%Y-%m-%d')),
            ('expense', 75.0, 5, 2, 'Pharmacy', (today - timedelta(days=9)).strftime('%Y-%m-%d')),
        ]
        
        for trans in demo_transactions:
            self.cursor.execute('''
                INSERT INTO transactions (type, amount, category_id, account_id, note, date_created)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', trans)
        
        self.conn.commit()
    
    # ==================== ACCOUNTS ====================
    
    def get_accounts(self):
        """Get all accounts"""
        self.connect()
        self.cursor.execute("SELECT * FROM accounts ORDER BY id")
        accounts = self.cursor.fetchall()
        self.close()
        return accounts
    
    def get_account(self, account_id):
        """Get single account by ID"""
        self.connect()
        self.cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
        account = self.cursor.fetchone()
        self.close()
        return account
    
    def add_account(self, name, acc_type='cash', balance=0.0, color='#00C49A', icon='wallet-outline'):
        """Add new account"""
        self.connect()
        self.cursor.execute('''
            INSERT INTO accounts (name, type, balance, color, icon)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, acc_type, balance, color, icon))
        self.conn.commit()
        self.close()
    
    def update_account(self, account_id, name=None, balance=None, color=None, icon=None):
        """Update account"""
        self.connect()
        if name:
            self.cursor.execute("UPDATE accounts SET name = ? WHERE id = ?", (name, account_id))
        if balance is not None:
            self.cursor.execute("UPDATE accounts SET balance = ? WHERE id = ?", (balance, account_id))
        if color:
            self.cursor.execute("UPDATE accounts SET color = ? WHERE id = ?", (color, account_id))
        if icon:
            self.cursor.execute("UPDATE accounts SET icon = ? WHERE id = ?", (icon, account_id))
        self.conn.commit()
        self.close()
    
    def delete_account(self, account_id):
        """Delete account"""
        self.connect()
        self.cursor.execute("DELETE FROM accounts WHERE id = ?", (account_id,))
        self.conn.commit()
        self.close()
    
    def get_total_balance(self):
        """Get total balance across all accounts"""
        self.connect()
        self.cursor.execute("SELECT SUM(balance) FROM accounts")
        result = self.cursor.fetchone()[0]
        self.close()
        return result if result else 0.0
    
    # ==================== CATEGORIES ====================
    
    def get_categories(self, category_type=None):
        """Get all categories, optionally filtered by type"""
        self.connect()
        if category_type:
            self.cursor.execute("SELECT * FROM categories WHERE type = ? ORDER BY name", (category_type,))
        else:
            self.cursor.execute("SELECT * FROM categories ORDER BY type, name")
        categories = self.cursor.fetchall()
        self.close()
        return categories
    
    def get_category(self, category_id):
        """Get single category by ID"""
        self.connect()
        self.cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        category = self.cursor.fetchone()
        self.close()
        return category
    
    def add_category(self, name, category_type, icon='tag-outline', color='#00C49A'):
        """Add new category"""
        self.connect()
        self.cursor.execute('''
            INSERT INTO categories (name, type, icon, color)
            VALUES (?, ?, ?, ?)
        ''', (name, category_type, icon, icon))
        self.conn.commit()
        self.close()
    
    def update_category(self, category_id, name=None, icon=None, color=None):
        """Update category"""
        self.connect()
        if name:
            self.cursor.execute("UPDATE categories SET name = ? WHERE id = ?", (name, category_id))
        if icon:
            self.cursor.execute("UPDATE categories SET icon = ? WHERE id = ?", (icon, category_id))
        if color:
            self.cursor.execute("UPDATE categories SET color = ? WHERE id = ?", (color, category_id))
        self.conn.commit()
        self.close()
    
    def delete_category(self, category_id):
        """Delete category"""
        self.connect()
        self.cursor.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        self.conn.commit()
        self.close()
    
    # ==================== TRANSACTIONS ====================
    
    def get_transactions(self, limit=None, offset=None, transaction_type=None, 
                        category_id=None, account_id=None, start_date=None, end_date=None, search=None):
        """Get transactions with filters"""
        self.connect()
        
        query = '''
            SELECT t.*, c.name as category_name, c.icon as category_icon, c.color as category_color,
                   a.name as account_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            LEFT JOIN accounts a ON t.account_id = a.id
            WHERE 1=1
        '''
        params = []
        
        if transaction_type:
            query += " AND t.type = ?"
            params.append(transaction_type)
        
        if category_id:
            query += " AND t.category_id = ?"
            params.append(category_id)
        
        if account_id:
            query += " AND t.account_id = ?"
            params.append(account_id)
        
        if start_date:
            query += " AND date(t.date_created) >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date(t.date_created) <= ?"
            params.append(end_date)
        
        if search:
            query += " AND (t.note LIKE ? OR c.name LIKE ?)"
            params.append(f"%{search}%")
            params.append(f"%{search}%")
        
        query += " ORDER BY t.date_created DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
            
            if offset:
                query += " OFFSET ?"
                params.append(offset)
        
        self.cursor.execute(query, params)
        transactions = self.cursor.fetchall()
        self.close()
        return transactions
    
    def get_transaction(self, transaction_id):
        """Get single transaction by ID"""
        self.connect()
        self.cursor.execute('''
            SELECT t.*, c.name as category_name, c.icon as category_icon, c.color as category_color,
                   a.name as account_name
            FROM transactions t
            LEFT JOIN categories c ON t.category_id = c.id
            LEFT JOIN accounts a ON t.account_id = a.id
            WHERE t.id = ?
        ''', (transaction_id,))
        transaction = self.cursor.fetchone()
        self.close()
        return transaction
    
    def add_transaction(self, transaction_type, amount, category_id, account_id, note='', date_created=None):
        """Add new transaction"""
        if date_created is None:
            date_created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self.connect()
        
        # Begin transaction
        self.cursor.execute("BEGIN")
        
        try:
            # Insert transaction
            self.cursor.execute('''
                INSERT INTO transactions (type, amount, category_id, account_id, note, date_created)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (transaction_type, amount, category_id, account_id, note, date_created))
            
            # Update account balance
            if transaction_type == 'income':
                self.cursor.execute('''
                    UPDATE accounts SET balance = balance + ? WHERE id = ?
                ''', (amount, account_id))
            else:
                self.cursor.execute('''
                    UPDATE accounts SET balance = balance - ? WHERE id = ?
                ''', (amount, account_id))
            
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            self.close()
    
    def update_transaction(self, transaction_id, amount=None, category_id=None, 
                          account_id=None, note=None, date_created=None):
        """Update transaction"""
        self.connect()
        
        # Get old transaction data
        self.cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        old_trans = self.cursor.fetchone()
        
        if old_trans:
            old_amount = old_trans[2]
            old_type = old_trans[1]
            old_account_id = old_trans[4]
            
            # Reverse old transaction effect on balance
            if old_type == 'income':
                self.cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", 
                                  (old_amount, old_account_id))
            else:
                self.cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", 
                                  (old_amount, old_account_id))
            
            # Update transaction
            if amount is not None:
                self.cursor.execute("UPDATE transactions SET amount = ? WHERE id = ?", (amount, transaction_id))
            if category_id is not None:
                self.cursor.execute("UPDATE transactions SET category_id = ? WHERE id = ?", 
                                  (category_id, transaction_id))
            if account_id is not None:
                self.cursor.execute("UPDATE transactions SET account_id = ? WHERE id = ?", 
                                  (account_id, transaction_id))
            if note is not None:
                self.cursor.execute("UPDATE transactions SET note = ? WHERE id = ?", (note, transaction_id))
            if date_created is not None:
                self.cursor.execute("UPDATE transactions SET date_created = ? WHERE id = ?", 
                                  (date_created, transaction_id))
            
            # Apply new transaction effect on balance
            new_amount = amount if amount is not None else old_amount
            new_type = old_type
            new_account_id = account_id if account_id is not None else old_account_id
            
            if new_type == 'income':
                self.cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", 
                                  (new_amount, new_account_id))
            else:
                self.cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", 
                                  (new_amount, new_account_id))
            
            self.conn.commit()
        
        self.close()
    
    def delete_transaction(self, transaction_id):
        """Delete transaction"""
        self.connect()
        
        # Get transaction data
        self.cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        transaction = self.cursor.fetchone()
        
        if transaction:
            amount = transaction[2]
            trans_type = transaction[1]
            account_id = transaction[4]
            
            # Reverse transaction effect on balance
            if trans_type == 'income':
                self.cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", 
                                  (amount, account_id))
            else:
                self.cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", 
                                  (amount, account_id))
            
            # Delete transaction
            self.cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
            self.conn.commit()
        
        self.close()
    
    # ==================== ANALYTICS ====================
    
    def get_expenses_by_category(self, start_date=None, end_date=None):
        """Get expenses grouped by category"""
        self.connect()
        
        query = '''
            SELECT c.id, c.name, c.icon, c.color, SUM(t.amount) as total
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.type = 'expense'
        '''
        params = []
        
        if start_date:
            query += " AND date(t.date_created) >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date(t.date_created) <= ?"
            params.append(end_date)
        
        query += " GROUP BY c.id ORDER BY total DESC"
        
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        self.close()
        return results
    
    def get_income_by_category(self, start_date=None, end_date=None):
        """Get income grouped by category"""
        self.connect()
        
        query = '''
            SELECT c.id, c.name, c.icon, c.color, SUM(t.amount) as total
            FROM transactions t
            JOIN categories c ON t.category_id = c.id
            WHERE t.type = 'income'
        '''
        params = []
        
        if start_date:
            query += " AND date(t.date_created) >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND date(t.date_created) <= ?"
            params.append(end_date)
        
        query += " GROUP BY c.id ORDER BY total DESC"
        
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        self.close()
        return results
    
    def get_monthly_summary(self, year=None, month=None):
        """Get monthly income and expenses summary"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        self.connect()
        
        # Get income for the month
        self.cursor.execute('''
            SELECT SUM(amount) FROM transactions 
            WHERE type = 'income' 
            AND strftime('%Y', date_created) = ? 
            AND strftime('%m', date_created) = ?
        ''', (str(year), str(month).zfill(2)))
        income = self.cursor.fetchone()[0] or 0.0
        
        # Get expenses for the month
        self.cursor.execute('''
            SELECT SUM(amount) FROM transactions 
            WHERE type = 'expense' 
            AND strftime('%Y', date_created) = ? 
            AND strftime('%m', date_created) = ?
        ''', (str(year), str(month).zfill(2)))
        expenses = self.cursor.fetchone()[0] or 0.0
        
        self.close()
        return {'income': income, 'expenses': expenses, 'savings': income - expenses}
    
    def get_daily_transactions(self, days=30):
        """Get daily transaction totals for chart"""
        self.connect()
        
        start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        self.cursor.execute('''
            SELECT date(date_created) as date, type, SUM(amount) as total
            FROM transactions
            WHERE date(date_created) >= ?
            GROUP BY date, type
            ORDER BY date
        ''', (start_date,))
        
        results = self.cursor.fetchall()
        self.close()
        return results
    
    # ==================== SETTINGS ====================
    
    def get_settings(self):
        """Get app settings"""
        self.connect()
        self.cursor.execute("SELECT * FROM settings LIMIT 1")
        settings = self.cursor.fetchone()
        self.close()
        return settings
    
    def get_currency(self):
        """Get currency setting"""
        settings = self.get_settings()
        return settings[1] if settings else 'USD'
    
    def update_settings(self, currency=None, theme=None):
        """Update settings"""
        self.connect()
        
        if currency:
            self.cursor.execute("UPDATE settings SET currency = ?", (currency,))
        if theme:
            self.cursor.execute("UPDATE settings SET theme = ?", (theme,))
        
        self.conn.commit()
        self.close()
    
    # ==================== UTILS ====================
    
    def backup_database(self, backup_path):
        """Create database backup"""
        import shutil
        shutil.copy2(self.db_path, backup_path)
    
    def reset_database(self):
        """Reset database to demo state"""
        self.close()
        
        # Delete existing database
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        
        # Reinitialize
        self.initialize()
