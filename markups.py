from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup


def get_main_menu_admin():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Создать лид', callback_data='make_lead'))
    return markup


def get_lead_in_bot_markup(lead):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Инфрормация', callback_data='info'))
    markup.add(InlineKeyboardButton('Время', callback_data='time_' + lead.id))
    markup.row(InlineKeyboardButton('100 R', callback_data='bid100_' + lead.id),
               InlineKeyboardButton('200 R', callback_data='bid200_' + lead.id),
               InlineKeyboardButton('300 R', callback_data='bid300_' + lead.id))

    return markup


def get_main_menu_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Мои аукционы', callback_data='my_aucc'))
    markup.add(InlineKeyboardButton('Правила', callback_data='rules'))
    markup.add(InlineKeyboardButton('Статистика', callback_data='statistics'))
    markup.add(InlineKeyboardButton('Помощь', callback_data='help'))
    return markup


def get_back_to_main_menu_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Главное меню', callback_data='fuckgoback'))
    return markup


def get_confirm_markup():
    markup = ReplyKeyboardMarkup()
    markup.row('Всё верно', 'Отменить создание лота')
    return markup


def get_group_lot_markup(lead):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Участвовать', url=f'https://t.me/aucccionBot?start={lead.id}'))
    markup.row(InlineKeyboardButton('Время', callback_data=f'T{lead.id}'),
               InlineKeyboardButton('Информация', callback_data='info'))

    return markup

def get_time_gap_markup():
    markup = ReplyKeyboardMarkup()
    markup.row('2 минуты', '6 часов', '12 часов')
    markup.row('1 день', '2 дня')
    return markup
