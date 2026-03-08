"""
Database Models - Table Creation
"""

from libs.database import Database


def init_db(db: Database):
    """Initialize database tables"""
    
    # Create accounts table
    db.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            balance REAL DEFAULT 0.0,
            color TEXT DEFAULT '#14B8A6',
            icon TEXT DEFAULT 'wallet',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create categories table
    db.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            icon TEXT DEFAULT 'tag',
            color TEXT DEFAULT '#14B8A6',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create transactions table
    db.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            category_id INTEGER,
            account_id INTEGER NOT NULL,
            note TEXT DEFAULT '',
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id),
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    """)
    
    # Create settings table
    db.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            currency TEXT DEFAULT '$',
            theme TEXT DEFAULT 'light'
        )
    """)
    
    # Insert default settings if not exists
    db.execute("INSERT OR IGNORE INTO settings (id, currency, theme) VALUES (1, '$', 'light')")
