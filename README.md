# 🔮 Crypto Analysis Bot (Public)

A public Telegram bot that sends technical analysis for **BTC, BNB, and SOL** to any channel where it is added as an admin.

## 📊 Schedule

| Time (UTC) | Analysis Type |
|------------|---------------|
| 09:00 | Daily (1D) |
| 21:00 | 4-Hour (4H) |

## 🪙 Coins Analyzed

- **Bitcoin (BTC/USDT)**
- **BNB (BNB/USDT)**
- **Solana (SOL/USDT)**

## 🚀 How to Add Bot to Your Channel

1. Add the bot as **Admin** in your Telegram channel
2. Give it permission to **Send Messages** and **Send Photos**
3. Go to GitHub Actions → **Discover Channels** → Click **Run workflow**
4. The bot will automatically discover your channel and start sending analysis!

## ⚙️ Setup (For Bot Owner)

### 1. Create GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Description |
|--------|-------------|
| `BOT_TOKEN` | Your Telegram Bot Token from @BotFather |
| `GITHUB_TOKEN` | Already provided by GitHub (for pushing channels.json) |

### 2. File Structure

```
📁 repo/
├── bot.py                  # Main analysis bot
├── discover.py             # Channel discovery bot
├── channels.json           # List of channels (auto-managed)
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── .github/workflows/
    ├── main.yml            # Runs analysis twice daily
    └── discover.yml        # Discovers new channels (manual)
```

### 3. Workflows

- **Analysis Bot** (`main.yml`): Runs automatically at 09:00 and 21:00 UTC
- **Discover Channels** (`discover.yml`): Run manually to update channel list

## 📈 Technical Indicators

- EMA 20, 50, 200
- RSI (Relative Strength Index)
- MACD with Histogram
- Bollinger Bands
- Stochastic Oscillator
- Volume Analysis

## 📝 Notes

- The bot sends analysis to **ALL channels** in `channels.json`
- Run **Discover Channels** workflow after adding the bot to a new channel
- The bot will skip channels where it is no longer an admin

---

**Not Financial Advice** — For educational purposes only.
