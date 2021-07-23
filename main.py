import telebot
from telebot import types
import yaml
import sqlite3


token="1948348894:AAEGn97tT-XyOzW0DKUNn9ZuBUXH1BpqB50"
first_order_number=1000
path="oreders_telebot.db"


def add_and_get_number(table_name, id, username, firstname, lastname, model, count):
    global first_order_number,path
    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute(
        f"""INSERT INTO {str(table_name)} 
        (
        id,
        username,
        firstname,
        lastname,
        model,
        count
        )
        VALUES (
                {int(id)},
                '{username}',
                '{firstname}',
                '{lastname}',
                '{model}',
                {int(count)}
                )"""
    )
    con.commit()
    cur = con.cursor()
    number = [i for i in cur.execute(f'SELECT MAX(number) FROM {table_name}')][0][0]
    return number + first_order_number

def Keyboard_Generator(buttons):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in buttons:
        button = types.KeyboardButton(text=i)
        keyboard.add(button)
    return keyboard

def Inline_Keyboard_Generator(buttons):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    for i in buttons:
        button = types.InlineKeyboardButton(i[0],callback_data=i[1])
        keyboard.add(button)
    return keyboard


def Buy_Item(chat_id,Item_Name):
    print(Item_Name,chat_id)
    if Item_Name=="AirPods_2":
        keyboard=Keyboard_Generator(["Заказать AirPods 2",'Вернуться в каталог'])
        bot.send_message(chat_id,"Отличный выбор👍",reply_markup=keyboard)
        bot.send_photo(chat_id, open('airpods2.jpg', 'rb'))
        bot.send_photo(chat_id, open('airpods2_price.jpg', 'rb'))

    if Item_Name=="AirPods_Pro":
        keyboard=Keyboard_Generator(["Заказать AirPods Pro",'Вернуться в каталог'])
        bot.send_message(chat_id,"Отличный выбор👍",reply_markup=keyboard)
        bot.send_photo(chat_id, open('airpodspro.jpg', 'rb'))
        bot.send_photo(chat_id, open('airpodspro_price.jpg', 'rb'))

def InlineButton_worker(chat_id, data, call):
    if data=="AirPods_2":
        Buy_Item(chat_id,"AirPods_2")

    if data=="AirPods_Pro":
        Buy_Item(chat_id,"AirPods_Pro")

    if "count" in data:
        count=count_worker(data)
        print(count)
        generate_order(chat_id,count[1],count[0],call)

def generate_count_keyboard(name):
    name=str(name)
    buttons=[
        ["1", f"count_1_{name}"],
        ["2", f"count_2_{name}"],
        ["3", f"count_3_{name}"],
        ["4", f"count_4_{name}"],
        ["5", f"count_5_{name}"],
        ["6", f"count_6_{name}"],
        ["7", f"count_7_{name}"],
        ["8", f"count_8_{name}"],
        ["9", f"count_9_{name}"],
        ["10", f"count_10_{name}"],
        ["Больше 10➡", f"count_more_10_{name}"]
    ]
    return Inline_Keyboard_Generator(buttons)

def count_worker(data):
    if "_more_" in data:
        return [0,str(data).replace("count_more_10_","")]
    data=str(data).replace("count_","").split("_")
    return data


def send_Pods(chat_id):
    keyboard=Inline_Keyboard_Generator([["Купить AirPods 2","AirPods_2"]])
    bot.send_photo(chat_id,open('airpods2.jpg','rb'),reply_markup=keyboard)
    keyboard = Inline_Keyboard_Generator([["Купить AirPods Pro", "AirPods_Pro"]])
    bot.send_photo(chat_id, open('airpodspro.jpg', 'rb'), reply_markup=keyboard)
    keyboard = Keyboard_Generator(["Telegram", "Instagram"])
    bot.send_message(chat_id, "Если ты сомневаешься в нашей компетентности и боишься быть обманутым, "
                              "тогда зацени наши Telegram канал и Instagram", reply_markup=keyboard)

def generate_order(chat_id,name,count,data):
    print(chat_id)
    number = payment(data.from_user,name,count)
    if number!=0:
        keyboard=Keyboard_Generator(['Вернуться в каталог'])
        bot.send_message(chat_id, "Ожидайте. Скоро с вами свяжется наш менеджер")
        #bot.send_message(chat_id,'Или свяжитесь с ним сами +7(903)542-21-02')
        bot.send_message(chat_id, 'Или свяжитесь с ним сами или идите нахуй')
        bot.send_message(chat_id,f'Номер вашего заказа {number}', reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "ERR")
        bot.send_message(chat_id, "У нас небольшие неполадки. Попробуй позже")
        keyboard = Keyboard_Generator(["ДА", "НЕТ"])
        sticker = open('sticker.webp', 'rb')
        bot.send_message(chat_id, "Хочешь купить новые AirPods?")
        bot.send_sticker(chat_id, sticker)
        bot.send_message(chat_id, "Тогда ты по адресу 👍", reply_markup=keyboard)

def payment(user_contacts,Airpods_model,count):
    chat_admin_id = 808525546
    print(user_contacts,Airpods_model,count)

    user_contacts=yaml.safe_load(str(user_contacts))
    user_id = str(user_contacts['id'])
    username = str(user_contacts['username'])
    first_name = str(user_contacts['first_name'])
    last_name=str(user_contacts["last_name"])
    number=add_and_get_number("orders",user_id,username,first_name,last_name,Airpods_model,count)

    message_to_admin=str(
        "\n"+
        " Model: " + '"' + Airpods_model + '"' + "\n"+
        " Count: " + str(count) + "\n"+
        " id: " + user_id + "\n"+
        " username: @" + username + "\n"+
        " Имя: "+ first_name + "\n"+
        " Фамилия: " + last_name + "\n"+
        " Link: " + f"https://t.me/{username}" +
        "\n"
    )
    count_shateg=24
    message_to_admin = "#"*(count_shateg-len(str(number))//2) +\
                       " " + str(number) + " " +\
                       "#"*(count_shateg-len(str(number))//2) +\
                       message_to_admin +\
                       "#"*(count_shateg*2)
    print(message_to_admin)
    if True:
        bot.send_message(chat_admin_id,message_to_admin)
    return number

def Message_worker(text_message,chat_id,data):
    print(text_message.lower())
    if text_message.lower() == 'да' or text_message.lower()=="хочу купить airpods":
        bot.send_message(chat_id, "Тогда ПОЕХАЛИ ❗❗❗")
        send_Pods(chat_id)

    elif text_message.lower() == 'нет':
        keyboard = Keyboard_Generator(["Telegram", "Instagram","Хочу купить AirPods"])
        bot.send_message(chat_id, "Если ты сомневаешься в нашей компетентности и боишься быть обманутым, "
                                  "тогда зацени наши Telegram канал и Instagram", reply_markup=keyboard)

    elif text_message.lower() == 'instagram':
        bot.send_message(chat_id,"📸 http://instagram.com/airpodstore01")
        keyboard = Keyboard_Generator(["ДА", "НЕТ","Telegram"])
        bot.send_message(chat_id, "Хочешь купить новые AirPods?",reply_markup=keyboard)


    elif text_message.lower() == 'telegram':
        bot.send_message(chat_id, "📺 Тут блять должна быть ссылка на телегу")
        keyboard = Keyboard_Generator(["ДА", "НЕТ","Instagram"])
        bot.send_message(chat_id, "Хочешь купить новые AirPods?", reply_markup=keyboard)

    elif text_message.lower() == 'вернуться в каталог':
        send_Pods(chat_id)

    elif text_message=="Заказать AirPods 2" or text_message=="Заказать AirPods Pro":
        keyboard = Keyboard_Generator(['Вернуться в каталог'])
        bot.send_message(chat_id,f"Сколько штук хотите заказать{text_message.replace('Заказать ','')}", reply_markup=keyboard)

        if "AirPods 2" in text_message:
            bot.send_photo(chat_id,open('airpods2.jpg',"rb"),reply_markup=generate_count_keyboard("AirPods 2"))

        elif "AirPods Pro" in text_message:
            bot.send_photo(chat_id,open('airpodspro.jpg',"rb"),reply_markup=generate_count_keyboard("AirPods Pro"))

    else:
        bot.send_message(chat_id, "Что❓ Я не знаю такую команду ❌")
        keyboard = Keyboard_Generator(["ДА", "НЕТ"])
        sticker = open('sticker.webp', 'rb')
        bot.send_message(chat_id, "Хочешь купить новые AirPods?")
        bot.send_sticker(chat_id, sticker)
        bot.send_message(chat_id, "Тогда ты по адресу 👍", reply_markup=keyboard)


bot=telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = Keyboard_Generator(["ДА", "НЕТ"])
    sticker=open('sticker.webp','rb')
    bot.send_message(message.chat.id, "Привет")
    bot.send_message(message.chat.id, "Хочешь купить новые AirPods?")
    bot.send_sticker(message.chat.id,sticker)
    bot.send_message(message.chat.id, "Тогда ты по адресу 👍",reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_message(message):
    if message.chat.type=='private':
        text_message = message.text
        chat_id = message.chat.id
        data=message
        try:
            if text_message != text_message:
                bot.send_message(chat_id, "ERR")
                bot.send_message(chat_id, "У нас небольшие неполадки. Попробуй позже")
                keyboard = Keyboard_Generator(["ДА", "НЕТ"])
                sticker = open('sticker.webp', 'rb')
                bot.send_message(chat_id, "Хочешь купить новые AirPods?")
                bot.send_sticker(chat_id, sticker)
                bot.send_message(chat_id, "Тогда ты по адресу 👍", reply_markup=keyboard)

            text_message = str(text_message).replace("\n",'')
            Message_worker(text_message, chat_id,data)

        except:
            bot.send_message(chat_id, "ERR")
            bot.send_message(chat_id, "У нас небольшие неполадки. Попробуй позже")
            keyboard = Keyboard_Generator(["ДА", "НЕТ"])
            sticker = open('sticker.webp', 'rb')
            bot.send_message(chat_id, "Хочешь купить новые AirPods?")
            bot.send_sticker(chat_id, sticker)
            bot.send_message(chat_id, "Тогда ты по адресу 👍", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def Callback_inline(call):
    try:
        if call.message:
            chat_id = call.message.chat.id
            data=str(call.data)
            InlineButton_worker(chat_id, data, call)
    except Exception as e:
        print("ERR",repr(e))
        chat_id = call.message.chat.id
        bot.send_message(chat_id, "ERR")
        bot.send_message(chat_id, "У нас небольшие неполадки. Попробуй позже")
        keyboard = Keyboard_Generator(["ДА", "НЕТ"])
        sticker = open('sticker.webp', 'rb')
        bot.send_message(chat_id, "Хочешь купить новые AirPods?")
        bot.send_sticker(chat_id, sticker)
        bot.send_message(chat_id, "Тогда ты по адресу 👍", reply_markup=keyboard)


if __name__=="__main__":
    print("________________________BOT_IS_STARTUP________________________")
    bot.polling(none_stop=True)