import telebot
import json
import requests
import http.client
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
    item4 = types.KeyboardButton("Время в любом городе")
    murckup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, "Выберете предложеныые функции",  reply_markup= murckup)
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.chat.type == "private":
        if message.text == "Сложный процент":
            msg = bot.send_message(message.from_user.id, 'Введите Ставку процента: ')
            bot.register_next_step_handler(msg, rate)
            compound_interest(P, r, n, t)
        elif message.text == "Цена финансового инструмена":
            Tick = bot.send_message(message.from_user.id, 'Введите тикер: ')
            bot.register_next_step_handler(Tick, tick_)
        elif message.text == "Погода в любом городе":
            Wether = bot.send_message(message.from_user.id, 'Введите город: ')
            bot.register_next_step_handler(Wether, wether_)
        elif message.text == "Время в любом городе":
            Time = bot.send_message(message.from_user.id, 'Введите город: ')
            bot.register_next_step_handler(Time, time_)
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
    global A
    A = float(P) * (1 + float(r)/float(n))**(float(n)*float(t))
    bot.send_message(message.from_user.id, A)
def tick_(message):
    try:
        tick = message.text
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={tick}&interval=5min&apikey=CGPKI6K7AFNVC2BH'
        r = requests.get(url)
        data = r.json()
        keys = list(data['Time Series (5min)'].keys())
        data = data['Time Series (5min)'][keys[0]]['1. open']
        bot.send_message(message.from_user.id, data)
    except:
        bot.send_message(message.from_user.id, "Такого тикера не существует, выбереьте другие функции")
def wether_(message):
    try:
        city = message.text
        conn = http.client.HTTPSConnection("api.collectapi.com")
        headers = {
            'content-type': "application/json",
            'authorization': "apikey 0bV3nYpxAMMVN3BejSiLq3:2LYioVfn8vyWJhcfnjFkcK"
            }

        conn.request("GET", f"/weather/getWeather?data.lang=tr&data.city={city}", headers=headers)
        res = conn.getresponse()
        data = res.read()
        a = data.decode("utf-8")
        b = json.loads(a)
        c = b["result"][0]["degree"]
        d = b["result"][0]["status"]
        bot.send_message(message.from_user.id, f"Температура: {c}")
        bot.send_message(message.from_user.id, f"Погода: {d}")
    except:
        bot.send_message(message.from_user.id, "Неверный город, выберет функцию")

def time_(message):
    #try:
        contry = str(message.text)
        conn = http.client.HTTPSConnection("api.collectapi.com")

        headers = {
            'content-type': "application/json",
            'authorization': "apikey 0bV3nYpxAMMVN3BejSiLq3:2LYioVfn8vyWJhcfnjFkcK"
        }

        conn.request("GET", "/corona/countriesData", headers=headers)

        res = conn.getresponse()
        data = res.read()

        a = data.decode("utf-8")
        print(data)
        b = json.loads(a)
        c = b["result"][0][f"{contry}"]
        bot.send_message(message.from_user.id, c)
    #except:
        bot.send_message(message.from_user.id, "Неверный город, выберет функцию")
bot.infinity_polling()