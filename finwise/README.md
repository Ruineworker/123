# FinWise - Personal Finance Tracker

A modern, beautiful Android finance tracking application built with Python and KivyMD.

## 📱 Features

- **Dashboard**: View total balance, monthly income/expenses, and recent transactions
- **Transactions**: Add, view, filter, and search income/expense transactions
- **Categories**: Manage expense and income categories with custom icons and colors
- **Accounts**: Track multiple accounts (cash, cards, savings, e-wallets)
- **Analytics**: Visual breakdown of expenses/income by category and monthly trends
- **Settings**: Customize currency, theme, backup database, reset data

## 🎨 Design

Modern fintech UI with:
- Bright teal-green accent color (#14B8A6)
- Soft rounded cards with elevation
- Clean typography
- Bottom navigation bar
- Hero card for total balance
- Category icons with colors

## 📁 Project Structure

```
finwise/
├── main.py                 # Application entry point
├── main.kv                 # Main KV layout
├── requirements.txt        # Python dependencies
├── buildozer.spec          # Buildozer configuration for Android
├── assets/                 # Images and icons
├── libs/
│   ├── __init__.py
│   ├── database.py         # SQLite database operations
│   └── models.py           # Database schema initialization
└── screens/
    ├── __init__.py
    ├── splash.py/kv        # Splash screen
    ├── dashboard.py/kv     # Main dashboard
    ├── transactions.py/kv  # Transactions list
    ├── add_transaction.py/kv  # Add/edit transaction form
    ├── categories.py/kv    # Categories management
    ├── accounts.py/kv      # Accounts management
    ├── analytics.py/kv     # Analytics and charts
    └── settings.py/kv      # Settings screen
```

## 🚀 Installation & Running

### On Windows/Linux (Desktop Testing)

1. **Install Python 3.8+**

2. **Install dependencies:**
```bash
pip install kivy==2.3.0 kivymd==1.2.0 pillow
```

3. **Run the application:**
```bash
cd finwise
python main.py
```

### On Android (Build APK)

1. **Install Buildozer (Linux/macOS only):**
```bash
pip install buildozer
```

2. **Install Java JDK and Android SDK**

3. **Initialize Buildozer (if not already done):**
```bash
buildozer init
```

4. **Build the APK:**
```bash
buildozer -v android debug
```

5. **Find APK in `bin/` directory**

For release build:
```bash
buildozer -v android release
```

## 📋 Requirements

- Python 3.8+
- Kivy 2.3.0
- KivyMD 1.2.0
- Pillow 10.2.0
- SQLite3 (included with Python)

## 🗄️ Database

The app uses SQLite with the following tables:

- **accounts**: Store user accounts (cash, cards, etc.)
- **categories**: Expense and income categories
- **transactions**: All financial transactions
- **settings**: App preferences (currency, theme)

Demo data is automatically populated on first run.

## 🎯 Usage

### Adding Transactions

1. Tap "+ Income" or "+ Expense" on dashboard
2. Or tap the FAB (+) button on transactions screen
3. Select type, enter amount, choose category and account
4. Add optional note and date
5. Tap "Save Transaction"

### Filtering Transactions

- Use filter chips (All/Income/Expenses)
- Search by note/description
- Filter by date range

### Managing Categories

1. Go to Settings → Categories
2. Toggle between Expense/Income tabs
3. View existing categories with icons
4. Add new categories (coming soon)

### Managing Accounts

1. Go to Accounts from bottom nav
2. View all accounts with balances
3. Total balance shown at top
4. Add new accounts (coming soon)

### Analytics

- Monthly summary cards
- Expenses by category breakdown
- Income by category breakdown
- 6-month trend history

### Settings

- Change currency ($, €, £, ¥, ₽)
- Toggle light/dark theme
- Backup database
- Reset to demo data

## 🎨 Customization

### Change Colors

Edit `main.py` theme colors:

```python
self.theme_cls.colors = {
    "primary": "#14B8A6",  # Main accent color
    "secondary": "#2DD4BF",  # Secondary accent
    "background": "#F0FDFA",  # Background color
    "surface": "#FFFFFF",  # Card background
}
```

### Change App Name

Edit `buildozer.spec`:
```
title = YourAppName
package.name = yourappname
```

### Add More Icons

KivyMD uses Material Design Icons. Find icons at:
https://pictogrammers.com/library/mdi/

## 🔧 Troubleshooting

### App crashes on startup
- Check that all dependencies are installed
- Ensure Python version is 3.8+
- Delete `finwise.db` and restart

### Buildozer fails to build
- Ensure Java JDK 11+ is installed
- Set ANDROID_HOME environment variable
- Run `buildozer android clean` and rebuild

### Database errors
- Close the app completely
- Delete `finwise.db` file
- Restart the app

## 📝 License

MIT License - Feel free to use and modify.

## 🤝 Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

## 📞 Support

For issues and questions, please open a GitHub issue.

---

Built with ❤️ using Python and KivyMD
