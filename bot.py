import random
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load kata dari kbbi.txt
def load_kbbi(filepath="kbbi.txt"):
    with open(filepath, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]

# Huruf stylized lengkap a-z
stylized = {
    "a": ["a", "q", "x", "h"],
    "b": ["b", "v", "p"],
    "c": ["c", "k", "s"],
    "d": ["d", "t"],
    "e": ["e", "i", "y"],
    "f": ["f", "v", "ph"],
    "g": ["g", "q", "k"],
    "h": ["h", "x"],
    "i": ["i", "y", "e"],
    "j": ["j", "z"],
    "k": ["k", "q", "c"],
    "l": ["l", "r", "i"],
    "m": ["m", "n"],
    "n": ["n", "m"],
    "o": ["o", "u"],
    "p": ["p", "b"],
    "q": ["q", "k"],
    "r": ["r", "z", "x"],
    "s": ["s", "z", "x"],
    "t": ["t", "d"],
    "u": ["u", "o"],
    "v": ["v", "f"],
    "w": ["w", "v"],
    "x": ["x", "z", "s"],
    "y": ["y", "i"],
    "z": ["z", "s", "x"]
}

# Gaya acak tiap huruf
def stylize(word):
    new_word = ""
    for ch in word.lower():
        if ch in stylized:
            new_word += random.choice(stylized[ch])
        else:
            new_word += ch
    return new_word

BOT_TOKEN = "7827575711:AAFgns-tzy_zEWf48iFQycaaJuFy9ylkgBE"
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

# Bot Telegram
async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kbbi_roots = load_kbbi()
    result = generate_usernames(kbbi_roots)
    reply = "\n".join(f"@{name}" for name in result)
    await update.message.reply_text(reply)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("generate", generate))
    app.run_polling()