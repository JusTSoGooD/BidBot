import telebot

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu_admin():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Создать лид', callback_data='make_lead'))
    return markup


def get_lead_menu_users():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Инфрормация', callback_data='info'))
    markup.add(InlineKeyboardButton('Время', callback_data='time'))
    markup.row(InlineKeyboardButton('100 R', callback_data='bid100'),
               InlineKeyboardButton('200 R', callback_data='bid200'),
               InlineKeyboardButton('300 R', callback_data='bid300'))

def get_main_menu_markup():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Мои аукционы', callback_data='my_aucc'))
    markup.add(InlineKeyboardButton('Правила', callback_data='rules'))
    markup.add(InlineKeyboardButton('Статистика', callback_data='statistics'))
    markup.add(InlineKeyboardButton('Помощь', callback_data='help'))
    
