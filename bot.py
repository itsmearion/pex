import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Baca root word dari file eksternal (Mega Vocabulary List)
def load_kbbi(filepath="kbbi.txt"):
    with open(filepath, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

# Alternatif huruf stylized
stylized = {
    "a": ["a", "q", "x", "h"],
    "e": ["e", "i", "y"],
    "i": ["i", "y"],
    "o": ["o", "u"],
    "u": ["u", "o"],
    "r": ["r", "z", "x"],
    "s": ["s", "z", "x"],
    "b": ["b", "v"],
    "d": ["d", "t"],
    "g": ["g", "q", "k"],
    "k": ["k", "q"],
    "l": ["l", "r"],
    "n": ["n", "m"]
}

def stylize(word):
    new_word = ""
    for ch in word:
        if ch in stylized:
            new_word += random.choice(stylized[ch])
        else:
            new_word += ch
    return new_word

BOT_TOKEN = "7827575711:AAHOQ_X4OXblDldXXuokx76exkwPvhpli3g"  # Ganti dengan token bot Telegram lo
CHECK_URL = "https://api.telegram.org/bot{}/getChat?username=@{}"

def is_username_available(username):
    response = requests.get(CHECK_URL.format(BOT_TOKEN, username))
    if response.status_code == 200:
        data = response.json()
        return not data.get("ok", False)
    return False

def generate_usernames(kbbi_roots, n=10):
    usernames = set()
    while len(usernames) < n:
        root = random.choice(kbbi_roots)
        styled = stylize(root)
        styled = (styled + random.choice(["", "e", "r", "x", "z"]))[:5]
        if styled in usernames:
            continue
        if is_username_available(styled):
            usernames.add(styled)
    return list(usernames)

# Telegram Bot Command
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kbbi_roots = load_kbbi_roots()
    result = generate_usernames(kbbi_roots)
    reply = "\n".join(f"@{name}" for name in result)
    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("generate", generate))
    app.run_polling()
