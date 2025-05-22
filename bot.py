import telebot
import requests

API_TOKEN = '7995161698:AAHq8XOaxk7Hz7YP7gjNuhRFa770maC9M8o'  # Ton token Telegram
TON_CENTER_API_KEY = '5d7d10ce1deb47f492191acddf5de22146ede57c26389ae7044256f8cefbeb0b'  # Ta clé API TON Center (à créer)

bot = telebot.TeleBot(API_TOKEN)

def get_wallet_tokens(address):
    url = "https://toncenter.com/api/v2/getAddressInformation"
    params = {
        "address": address,
        "api_key": TON_CENTER_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data.get("ok"):
        return data["result"].get("tokens", [])
    return []

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salut! Envoie-moi ton wallet TON pour vérifier les tokens.")

@bot.message_handler(func=lambda message: True)
def clean_wallet(message):
    wallet = message.text.strip()
    tokens = get_wallet_tokens(wallet)
    if not tokens:
        bot.reply_to(message, "Aucun token trouvé ou wallet invalide.")
        return

    shitcoins = [t for t in tokens if t.get("balance", 0) < 1]
    if shitcoins:
        names = ", ".join([t["name"] for t in shitcoins])
        bot.reply_to(message, f"Tokens à considérer pour nettoyage : {names}")
    else:
        bot.reply_to(message, "Aucun shitcoin détecté.")

bot.polling()
