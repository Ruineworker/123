# FinWise - Personal Finance Tracker

A beautiful, modern personal finance tracking application built with Python and KivyMD for Android.

## 📱 Features

- **Dashboard**: View total balance, monthly income/expenses, and recent transactions
- **Transactions**: Add, view, and filter income and expense transactions
- **Categories**: Manage expense and income categories with custom icons and colors
- **Accounts**: Track multiple accounts (cash, bank, savings, e-wallets)
- **Analytics**: View spending patterns by category
- **Settings**: Currency selection, data backup, and reset options

## 🎨 Design

Modern fintech UI with:
- Bright turquoise-green accent color (#00C49A)
- Soft rounded cards with shadows
- Clean typography
- Intuitive bottom navigation
- Premium feel inspired by modern finance apps

## 📁 Project Structure

```
finwise_app/
├── main.py                 # Application entry point
├── libs/
│   └── database.py         # SQLite database management
├── screens/
│   ├── manager.py          # Screen manager/navigation
│   ├── dashboard.py        # Main dashboard screen
│   ├── transactions.py     # Transactions list screen
│   ├── add_transaction.py  # Add transaction form
│   ├── categories.py       # Categories management
│   ├── accounts.py         # Accounts management
│   ├── analytics.py        # Analytics screen
│   └── settings.py         # Settings screen
├── data/
│   └── finwise.db          # SQLite database (created on first run)
├── assets/                 # App icons and images
├── requirements.txt        # Python dependencies
└── buildozer.spec          # Buildozer configuration for Android
```

## 🚀 Installation & Running on Windows

### Prerequisites

1. Python 3.8 or higher
2. pip package manager

### Steps

1. **Clone or download the project:**
   ```bash
   cd finwise_app
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

## 📦 Building APK for Android

### Using Buildozer (Linux/macOS required)

Buildozer requires Linux or macOS. If you're on Windows, use WSL2 or a VM.

1. **Install Buildozer:**
   ```bash
   pip install buildozer
   ```

2. **Initialize buildozer.spec (if not present):**
   ```bash
   buildozer init
   ```

3. **Update buildozer.spec** with the provided configuration

4. **Build APK:**
   ```bash
   buildozer -v android debug
   ```

5. **Find your APK:**
   The APK will be in `bin/` folder as `finwise-0.1-debug.apk`

### Using Google Colab (Alternative for Windows users)

You can build the APK using Google Colab without needing Linux:

```python
!pip install buildozer
!pip install cython==0.29.33
!sudo apt-get update -y
!sudo apt-get install -y python3-pip build-essential git python3 python3-dev libffi-dev libssl-dev libgdk-pixbuf2.0-dev libmpc-dev libmpfr-dev libgmp-dev autoconf libtool
!buildozer -v android debug
```

## ⚙️ Configuration

### Change App Name

Edit `buildozer.spec`:
```ini
title = FinWise
package.name = finwise
```

### Change Colors

Edit `main.py`:
```python
class FinWiseApp(MDApp):
    primary_color = (0.0, 0.75, 0.6, 1)  # Turquoise-green
    secondary_color = (0.2, 0.6, 0.9, 1)  # Blue
```

### Change Default Currency

The default currency is USD. Users can change it in Settings.
To change the default, edit `libs/database.py` in the `insert_demo_data()` method.

## 🗄️ Database

The app uses SQLite with the following tables:

- **accounts**: Store user accounts/wallets
- **categories**: Income and expense categories
- **transactions**: All financial transactions
- **settings**: App preferences (currency, theme)

Database file is stored in:
- **Desktop**: `data/finwise.db`
- **Android**: App's private storage directory

## 🎯 Demo Data

On first launch, the app includes:
- 4 sample accounts (Cash, Bank Card, Savings, E-Wallet)
- 15 categories (10 expense, 5 income)
- 10 sample transactions
- Default currency: USD

## 🔧 Troubleshooting

### App crashes on startup
- Ensure all dependencies are installed
- Check Python version (3.8+)
- Delete `data/finwise.db` and restart

### Buildozer fails to build
- Ensure all system dependencies are installed
- Try `buildozer android clean` then rebuild
- Check Java/SDK versions

### UI looks wrong on desktop
- Window size is set for mobile testing
- Actual mobile appearance may vary slightly

## 📝 Requirements

See `requirements.txt` for full list:
- kivymd==1.2.0
- kivy>=2.3.0
- sqlite3 (built-in)

## 📄 License

This project is open source and available for personal and commercial use.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

Built with ❤️ using Python and KivyMD
