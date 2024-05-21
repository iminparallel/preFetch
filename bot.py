import os 
import telebot
from utils import get_asset_data

BOT_TOKEN = os.environ.get("BOT_TOKEN")


bot = telebot.TeleBot(BOT_TOKEN)

commands = {
    "start" : "greetings",
    "help" : "command details",
    "assDet" : "get information of a specific asset",
    "assList" : "get the available asset listing"
}


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how may I /help you today?")

@bot.message_handler(commands=['help'])
def command_help(message):
    hlp = "the following commands are available"
    for key in commands:
        hlp += "/" + key + ": " + commands[key] + "\n"
    bot.send_message(message.chat.id, hlp, parse_mode="Markdown")

@bot.message_handler(commands=['assDet'])
def command_assetDetails(message):
    q  = "what asset should I fetch for you?"
    snt = bot.send_message(message.chat.id, q, parse_mode="Markdown")
    bot.register_next_step_handler(snt, fetchData)

def fetchData(message):
    curr = message.text
    data = get_asset_data(curr)
    st = ""
    for i in data.keys():
        st += str(i) + "->" + str(data[i]) + "\n"
    bot.send_message(message.chat.id, f'here is the details for {curr}', parse_mode="Markdown")
    bot.send_message(message.chat.id, st, parse_mode="Markdown")
    

@bot.message_handler(commands=['assList'])
def command_assetList(message):
    q  = "here's a list of all the available assets"
    data = get_asset_data("")
    st = ""
    k = 0
    l = []
    for i in data['products']:
        l.append(i['product_id'])
    bot.send_message(message.chat.id, q, parse_mode="Markdown")
    for i in l:
        st += i + "| "
        k +=1
        if k == 50:
            st += "\n"
            k = 0
            bot.send_message(message.chat.id, st, parse_mode="Markdown")
            st = ""

    

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()