import config
import telebot
from telebot import types
from geopy.distance import vincenty
import messages
import os
import mysql.connector


mydb = config.mysqlpath

cur = mydb.cursor()
# sql = 'ALTER TABLE `bot_shop_db`.`catalog` DROP COLUMN `names`'
# cur.execute(sql)
# mydb.commit()
# cur = mydb.cursor()
# # furniture_foto = cur.execute('SELECT decription FROM bot_shop_db.catalog')
# cur.execute('SELECT * FROM catalog')
# furniture_foto = cur.fetchall()
# # cur.fetchall()
# f = open(os(furniture_foto), 'rb')
# print(f.read())

bot = telebot.TeleBot(config.token)

# class User:
#     def __init__(self, user_id, img, count):
#         self.user_id = user_id
#         # self.img = img
#         # self.count = count
#
#
# busket = {}


class UserBusket(object):
    user_busket = {}
    def __init__(self, user_id):
        self.user = user_id

    def add_in_buscet(self, product, price):
        if not poduct in self.user_busket:
            self.user_busket[product] = price


    def remove_in_buscet(self, product, price):
        if poduct in self.user_busket:
            del self.user_busket[product]

new_user_busket = UserBusket('Uliya')

#########################################
# cur.execute('SELECT name FROM bot_shop_db.catalog
# where id = call.data.split('_')[1]')
# product  = cur.fetchall()





###########################################
# cur.execute('SELECT id FROM catalog')
# data_id = cur.fetchall()

# new_user = User('Vasiya')
# new_user.basket.append({'id': '1', 'count': 1})

PRICE = telebot.types.LabeledPrice(label='Самый хороший товар', amount=100000)

markup_keyboard = types.ReplyKeyboardMarkup(row_width=1)
item1 = types.KeyboardButton("Адреса магазинов", request_location=True)
item2 = types.KeyboardButton("Варианты оплаты")
item3 = types.KeyboardButton("Способы доставки")
markup_keyboard.add(item1, item2, item3)



markup_keyboard_inline = types.InlineKeyboardMarkup()
item1_inline = types.InlineKeyboardButton("Оплата картой", callback_data='card')
item2_inline = types.InlineKeyboardButton("Наличными курьеру", callback_data='cash')
item3_inline = types.InlineKeyboardButton("Почтовый перевод", callback_data='post')
markup_keyboard_inline.add(item1_inline, item2_inline, item3_inline)

markup_ready_busket = types.InlineKeyboardMarkup()
item1_ready_busket = types.InlineKeyboardButton("Перейти в корзину", callback_data='inbusket')
markup_ready_busket.add(item1_ready_busket)

markup_catalog = types.InlineKeyboardMarkup()
item1_catalog = types.InlineKeyboardButton("Посуда", callback_data='tableware')
item2_catalog = types.InlineKeyboardButton("Предметы интерьера", callback_data='interior_items')
item3_catalog = types.InlineKeyboardButton("Мебель", callback_data='furniture')
markup_catalog.add(item1_catalog, item2_catalog, item3_catalog)

@bot.message_handler(commands=['catalog'])
def category_catalog(message):
    bot.send_message(message.chat.id, text='Выберети категорию:',
                 reply_markup=markup_catalog)


# ОПЛАТА НАЧАЛО

@bot.message_handler(commands=['terms'])
def pay_on_line(message):
    bot.send_message(message.chat.id, text=messages.terms)


@bot.message_handler(commands=['buy'])
def pay_on_line(message):
    bot.send_message(message.chat.id, text=messages.pre_buy_demo_alert)
    bot.send_invoice(message.chat.id, title=config.lot['title'],
                             description=config.lot['description'],
                             invoice_payload=config.lot['payload'],
                             provider_token=config.lot['provaider_token'],
                             currency=config.lot['currency'],
                             prices= [PRICE],
                             start_parameter=config.lot['start_parametr'],
                             photo_url=None,
                             photo_size=None,
                             photo_width=None,
                             photo_height=None,
                             need_name=None, need_phone_number=None, need_email=None,
                             need_shipping_address=None,
                             is_flexible=False,
                     )


@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# ОПЛАТА КОНЕЦ


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,'Добро пожаловать, {0.first_name}! \n Я - {1.first_name}\n'
                                     ' Бот интернет-магазина \n'
                                     '/catalog - перейти в каталог'  .format(message.from_user, bot.get_me()),
                                     parse_mode='html', reply_markup = markup_keyboard)



@bot.message_handler(content_types='text')
def send_message(message):
    if message.text == 'Варианты оплаты':
        bot.send_message(message.chat.id, 'Возможные способы оплаты:',
                         reply_markup = markup_keyboard_inline)

    elif message.text == 'Способы доставки':
        bot.send_message(message.chat.id, 'Курьерская доставка, Доставка почтой, Доставка в пункт самовывоза,Самовывоз из магазина',
                         reply_markup = markup_keyboard)
    else:
        bot.send_message(message.chat.id, message.text, reply_markup = markup_keyboard )

@bot.message_handler(func=lambda message: True, content_types=['location'])
def shops_location(message):
    lat = message.location.latitude
    lon = message.location.longitude
    print(lat, lon)

    distance = []
    for i in config.shops:
        result = vincenty((i['lat'], i['lon']), (lat, lon)).kilometers
        distance.append(result)
        index_ = distance.index(min(distance))

    bot.send_message(message.chat.id, 'Ближайший к вам магазин:')

    bot.send_venue(message.chat.id, config.shops[index_]['lat'], config.shops[index_]['lat'],
                                config.shops[index_]['title'], config.shops[index_]['address'])



@bot.callback_query_handler(func=lambda call:True)
def choose_catalog(call):

    if call.data in ('tableware', 'interior_items', 'furniture'):
        cur.execute(f"SELECT * FROM catalog WHERE category = '{call.data}' LIMIT 3")
        photos = cur.fetchall()
        for itm in photos:
            f = open(itm[3], 'rb')
            markup_in_busket = types.InlineKeyboardMarkup(row_width=2)
            # item1_in_busket = types.InlineKeyboardButton(text="В корзину " + str(itm[0]), callback_data=itm[0])
            # item1_in_busket = types.InlineKeyboardButton(text="Купить за " + str(itm[5]) + "руб", callback_data=f"id_{itm[0]}")
            item1_in_busket = types.InlineKeyboardButton(text="Добавить", callback_data=f"id_{itm[0]}")
            item2_in_busket = types.InlineKeyboardButton(text='Удалить', callback_data=f"del_{itm[0]}")
            markup_in_busket.add(item1_in_busket, item2_in_busket)
            bot.send_photo(call.message.chat.id, photo=f.read(), caption=itm[2])
            bot.send_message(call.message.chat.id, text=itm[4])
            bot.send_message(call.message.chat.id, text='Чтобы вернуться в каталог нажмите - /catalog \n '
                                                        'Чтобы добавьте в корзину нажмите на кнопку',
                             reply_markup=markup_in_busket)

    if call.data.split('_')[0] == 'id':
        messages_id = call.message.chat.id
        good_id_add = call.data.split('_')[1]
        print(good_id_add)
        msq = "INSERT INTO add_in_busket (id_user_from_chat, id_product_from_catalog) VALUES ( %s, %s)"
        val =[(messages_id ,good_id_add)]
        cur.executemany(msq,val)
        mydb.commit()

        # if new_user_busket.user_busket.get(good_id):
        #     new_user_busket.user_busket[good_id] += 1
        # else:
        #     new_user_busket.user_busket[good_id] = 1
        bot.answer_callback_query(call.id, show_alert=True, text="Товар добавлен в корзину")
        bot.send_message(call.message.chat.id, text='Для перехода в корзину нажмите кнопку',
                     reply_markup=markup_ready_busket)
        # if new_user_busket.user_busket[good_id] in new_user_busket.user_busket:
        #     for key in new_user_busket.user_busket:
        #         print(new_user_busket.user_busket[key])


    if call.data.split('_')[0] == 'del':
        messages_id = call.message.chat.id
        print(type(messages_id))
        good_id_del = call.data.split('_')[1]
        print(good_id_del)
        msq = "UPDATE add_in_busket SET status = %s WHERE id_user_from_chat = %s AND " \
              "id_product_from_catalog = %s LIMIT 1"
        val =[('deleted', messages_id, good_id_del)]
        cur.executemany(msq,val)
        mydb.commit()
        bot.answer_callback_query(call.id, show_alert=True, text="Товар удален из корзины")
    if call.data == 'inbusket':
        messages_id = call.message.chat.id





    # if call.data == 'interior_items':
    #     for file in os.listdir('C:/catalog/interior_items'):
    #         if file.split('.')[-1] == 'jpg':
    #             f = open('C:/catalog/interior_items/' + file, 'rb')
    #             f = f.read()
    #             bot.send_photo(call.message.chat.id, photo=f, caption='Предметы интерьера')
    #             bot.send_message(call.message.chat.id, text='Чтобы вернуться в каталог нажмите - /catalog \n'
    #                                                         'Чтобы добавить товар в корзину нажмите на кнопку.',
    #                              reply_markup=markup_in_busket)
    # if call.data == 'furniture':
    #     for file in os.listdir('C:/catalog/furniture'):
    #         if file.split('.')[-1] == 'jpg':
    #             f = open('C:/catalog/furniture/' + file, 'rb')
    #             f = f.read()
    #             msg = bot.send_photo(call.message.chat.id, photo=f, caption='Мебель')
    #             bot.send_message(call.message.chat.id, text='Чтобы вернуться в каталог нажмите - /catalog, \n'
    #                                                         'Чтобы добавить товар в крзину нажмите на кнопку',
    #                              reply_markup=markup_in_busket)
    #             bot.register_next_step_handler(msg, callback='furniture')

    if call.data == 'card':
        bot.send_message(call.message.chat.id, 'Оплата on-line по карте.')
        bot.send_message(call.message.chat.id, text=messages.help_message)
    if call.data == 'cash':
        bot.send_message(call.message.chat.id, text='Вы можете оплатить заказ наличными при получении заказа'
                                                    ' в любом ближайшем магазине')
    if call.data == 'post':
        bot.send_message(call.message.chat.id, text='100% предоплата. В зависимости от удаленности места - '
                                                    ' доставка занимает от нескольких дней да месяца')





# def info_zakaz(message):
#     try:
#         user_id = message.from_user.id
#         user_data[chat_id] = User(message.text)




bot.polling()