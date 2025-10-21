# 🤖 Instagram Following Bot

A smart and stealthy **Instagram automation bot** built using **Python + Selenium** that automatically follows accounts from another user's *following list* — while behaving like a real human to minimize detection risks.

---

## 🚀 Features

* 🧠 **Human-like Behavior**

  * Randomized delays and mouse movements
  * Realistic typing simulation with typos and corrections

* 🔒 **Safety-Oriented**

  * Built-in block detection
  * Cooldown between follows
  * One-run-per-day guideline

* 🔍 **Smart Navigation**

  * Auto-login
  * Natural scrolling and browsing
  * Fallback search method if direct profile access fails

* 🧾 **Activity Logging**

  * Every step is logged in the console for easy debugging and monitoring

---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Automation Framework:** Selenium
* **WebDriver:** ChromeDriver
* **Other Tools:** `logging`, `random`, `time`

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/instagram-following-bot.git
cd instagram-following-bot
```

### 2. Install dependencies

Make sure you have Python 3.9+ and pip installed, then run:

```bash
pip install selenium
```

### 3. Set up ChromeDriver

Download and place **ChromeDriver** compatible with your Chrome version:

* [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)

Ensure it's in your PATH or in the same directory as `main.py`.

---

## ⚙️ Configuration

In `main.py`, update the `CONFIG` dictionary at the top:

```python
CONFIG = {
    'username': 'your_username',
    'password': 'your_password',
    'target_account': 'target_profile_username',
    'max_follows': 2,
    'follow_delay': (25, 40)
}
```

**Parameters:**

* `username` → Your Instagram username
* `password` → Your Instagram password
* `target_account` → The account whose *following list* you want to follow from
* `max_follows` → How many accounts to follow per run
* `follow_delay` → Random delay between follows (seconds)

---

## ▶️ Run the Bot

```bash
python main.py
```

You’ll see:

```
============================================================
INSTAGRAM FOLLOWING BOT
============================================================
PURPOSE:
Follows accounts that <target_account> follows
...
Press ENTER to start (Ctrl+C to cancel)...
```

Then the bot logs into Instagram, opens the target’s profile, and starts following accounts safely.

---

## ⚠️ Safety Rules (Read Before Running)

1. **Run once per day maximum**
2. **Wait 48+ hours after any block**
3. **Use account manually for 30+ minutes before automation**
4. **Avoid running on newly created accounts**
5. **Do not use with your main account**

Instagram automation is against platform terms — use **for educational purposes only** and **at your own risk.**

---

## 🧩 File Structure

```
📁 instagram-following-bot
│
├── main.py              # Main bot script
├── README.md            # Documentation
└── requirements.txt     # Python dependencies (optional)
```

You can create a `requirements.txt` with:

```
selenium
```

---

## 🏆 Author

**👨‍💻 Joy Mondal**
Full-Stack Web Developer | Python Automation Enthusiast
🔗 [GitHub Profile](https://github.com/jaymondal45)

---

## 🧠 Disclaimer

This project is for **educational and research purposes only**.
Use responsibly — the author is **not responsible** for any misuse or violations of Instagram’s terms.

---
