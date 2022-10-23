import telebot
import json
import requests
import http.client
import botfunctions
from telebot import types
API_TOKEN = '5302168691:AAHT_cyagO98FCOg9iqv-dCylYStToxouhU'
r = 0
P = 0
n = 0
t = 0
bot = telebot.TeleBot(API_TOKEN)
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def start(message):
    murckup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Сложный процент")
    item2 = types.KeyboardButton("Цена финансового инструмена")
    item3 = types.KeyboardButton("Погода в любом городе")
    item4 = types.KeyboardButton("Количество заболевших короновирусом")
    item5 = types.KeyboardButton("Телефонный код страны")
    murckup.add(item1, item2, item3, item4, item5)
    bot.send_message(message.chat.id, "Выберете предложеныые функции",  reply_markup= murckup)
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.chat.type == "private":
        if message.text == "Сложный процент":
            msg = bot.send_message(message.from_user.id, 'Введите Ставку процента: ')
            bot.register_next_step_handler(msg, rate)
        elif message.text == "Цена финансового инструмена":
            Tick = bot.send_message(message.from_user.id, 'Введите тикер: ')
            bot.register_next_step_handler(Tick, tick_)
        elif message.text == "Погода в любом городе":
            Wether = bot.send_message(message.from_user.id, 'Введите город на английском с заглавной буквы: ')
            bot.register_next_step_handler(Wether, wether_)
        elif message.text == "Количество заболевших короновирусом":
            Time = bot.send_message(message.from_user.id, 'Введите страну(на анлгийском с заглавной буквы): ')
            bot.register_next_step_handler(Time, time_)
        elif message.text == "Телефонный код страны":
            Phone = bot.send_message(message.from_user.id, 'Введите страну(на анлгийском с заглавной буквы): ')
            bot.register_next_step_handler(Phone, phoneCode)
def rate(message):
    global r
    r = message.text
    sum = bot.send_message(message.from_user.id, 'Введите начальнцю сумму: ')
    bot.register_next_step_handler(sum, sum_)
def sum_(message):
    global P
    P = message.text
    N = bot.send_message(message.from_user.id, 'Введите период начисления процента: ')
    bot.register_next_step_handler(N, N_)
def N_(message):
    global n
    n = message.text
    R = bot.send_message(message.from_user.id, 'Введите количество периодов начисления процента: ')
    bot.register_next_step_handler(R, T_)
def T_(message):
    global t
    t = message.text
    compound_interest_ = bot.send_message(message.from_user.id, 'Итог: ')
    bot.register_next_step_handler(compound_interest_, compound_interest(P, r, n, t, message))

def compound_interest(P, r, n, t, message):
    try:
        global A
        A = botfunctions.get_compound_interest(P,r,n,t)
        bot.send_message(message.from_user.id, A)
    except:
        bot.send_message(message.from_user.id, "Неправильные данные, выберете другие функции")

def tick_(message):
    try:
        tick = message.text
        data=botfunctions.get_tick(tick)
        bot.send_message(message.from_user.id, data)
    except:
        bot.send_message(message.from_user.id, "Такого тикера не существует, выбереьте другие функции")
def wether_(message):
    try:
        city = message.text
        c,d = botfunctions.get_wether(city)
        bot.send_message(message.from_user.id, f"Температура: {c}")
        bot.send_message(message.from_user.id, f"Погода: {d}")
    except:
        bot.send_message(message.from_user.id, "Неверный город, выберетe функцию")

def time_(message):
    try:
        contry = str(message.text)
        k = botfunctions.get_corona(contry)
        bot.send_message(message.from_user.id, k)
    except:
        bot.send_message(message.from_user.id, "Неверная страна, выберете функцию")


def phoneCode(message):
    contry = message.text
    code=botfunctions.get_phone_code(contry)
    if len(code)>0:
        bot.send_message(message.from_user.id, f"Код страны: {code}")
    else:  bot.send_message(message.from_user.id, "Неверная страна, выберет функцию")

bot.infinity_polling()
