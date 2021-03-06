help_message = '''
Через этого бота можно купить предметы интерьера, чтобы посмотреть, как происходит покупка и оплата в Telegram.
Отправьте команду /buy, чтобы перейти к покупке.
Узнать правила и положения можно воспользовавшись командой /terms.
'''

start_message = 'Привет! Это демонстрация работы платежей в Telegram!\n' + help_message

pre_buy_demo_alert = '''\
Так как сейчас я запущен в тестовом режиме, для оплаты нужно использовать карточку с номером `1111 1111 1111 1026, 12/22, CVC 000`
Счёт для оплаты:
'''

terms = '''\
*Спасибо, что выбрали нашего бота. Мы надеемся, вам понравится ваша новая машина времени!*
1. Если машина времени не будет доставлена вовремя, пожалуйста, произведите переосмысление вашей концепции времени и попробуйте снова.
2. Если вы обнаружите, что машина времени не работает, будьте добры связаться с нашими сервисными мастерскими будущего с экзопланеты Trappist-1e. Они будут доступны в любом месте в период с мая 2075 года по ноябрь 4000 года нашей эры.
3. Если вы хотите вернуть деньги, будьте так любезны подать заявку вчера, и мы немедленно совершим возврат.
'''

tm_title = 'Самая настоящая Машина Времени'
tm_description = '''\
Стул не требует сборки, поэтому вы можете начать пользоваться им сразу же после покупки.
Прекрасно подойдет для балкона или другого небольшого помещения, складывается и не займет много места при хранении.
Прочный и простой в уходе стул изготовлен из стали с порошковым покрытием и пластика.
Материалы, из которых изготовлена эта садовая мебель, не требуют ухода.
'''

AU_error = '''\
Попробуйте выбрать другой адрес!
'''

wrong_email = '''\
Указанный имейл не действителен.
Попробуйте указать другой имейл.
'''

successful_payment = '''
Ура! Платеж на сумму `{total_amount} {currency}` совершен успешно!
Правила возврата средств смотрите в /terms
Перейти к покупкам - /buy
'''


MESSAGES = {
    'start': start_message,
    'help': help_message,
    'pre_buy_demo_alert': pre_buy_demo_alert,
    'terms': terms,
    'tm_title': tm_title,
    'tm_description': tm_description,
    'AU_error': AU_error,
    'wrong_email': wrong_email,
    'successful_payment': successful_payment,
}