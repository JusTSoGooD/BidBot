import telebot
import ChannelManager
import markups
from lead import Lead
import datetime
import os
from telebot.types import ReplyKeyboardRemove
import ChannelManager
import database


class TgBot:

    @staticmethod
    def start_bot(key):
        bot = telebot.TeleBot(key)
        admin_menu = markups.get_main_menu_admin()
        main_menu = markups.get_main_menu_markup()
        confirm_markup = markups.get_confirm_markup()

        sql_connection = database.sql_connection()
        cursor = sql_connection.cursor()
        database.create_table_lots(sql_connection, cursor)

        path = os.path.abspath(__file__).rpartition('\\')[0]
        if not os.path.exists(f'{path}\\Photo'):
            os.mkdir(f'{path}\\Photo')

        if not os.path.exists(f'{path}\\Video'):
            os.mkdir(f'{path}\\Video')

        def download_lead_photo(message, lead):
            photo_id = message.photo[2].file_id
            file_path = bot.get_file(photo_id).file_path
            file = bot.download_file(file_path)
            with open(f'{path}\\Photo\\{lead.id}.jpg', 'wb') as code:
                code.write(file)

        def download_lead_video(message, lead):
            file_info = bot.get_file(message.video.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(f'{path}\\Video\\{lead.id}.mp4', 'wb') as code:
                code.write(downloaded_file)

        @bot.message_handler(content_types=['text'])
        def start(message):

            lot_id = message.text.replace("/start ", '')

            print(lot_id)
            if  message.text == "/start " + lot_id:
                print(lot_id)
                lead = database.get_lead_from_db(lot_id)
                ChannelManager.send_lot_to_bot(bot, lead, message)


            if message.text == '/admin':
                bot.send_message(message.chat.id, 'Главное админ меню', reply_markup=admin_menu)

            if message.text == '/start':
                bot.send_message(message.chat.id, 'Привет, я бот аукционов *название канала* Удачных торгов!',
                                 reply_markup=main_menu)

        def get_lead_name(user_id, lead):
            next_step = bot.send_message(user_id, 'Введите имя лота')
            bot.register_next_step_handler(next_step, get_lead_price, lead)

        def get_lead_price(message, lead):
            lead.name = message.text
            next_step = bot.send_message(message.chat.id, 'Введите стартовую цену лота (в долларах)')
            bot.register_next_step_handler(next_step, get_lead_description, lead)

        def get_lead_description(message, lead):
            lead.price = message.text
            next_step = bot.send_message(message.chat.id, 'Введите описание лота')
            bot.register_next_step_handler(next_step, get_lead_photo, lead)

        def get_lead_photo(message, lead):
            lead.description = message.text
            next_step = bot.send_message(message.chat.id,
                                         'Пришлите фотографию лота *в случае отсутствия фото отправьте любой символ*')
            bot.register_next_step_handler(next_step, get_lead_video, lead)

        def get_lead_video(message, lead):
            if message.content_type == 'photo':
                download_lead_photo(message, lead)
                lead.photo = f'{path}\\Photo\\{lead.id}.jpg'

            next_step = bot.send_message(message.chat.id,
                                         'Пришлите видео с лотом *в случае отсутствия отправьте любой символ*')
            bot.register_next_step_handler(next_step, confirm_lead, lead)

        def confirm_lead(message, lead):
            if message.content_type == 'video':
                download_lead_video(message, lead)
                lead.video = f'{path}\\Video\\{lead.id}.mp4'

            bot.send_message(message.chat.id, "Проверьте, правильно ли введена информация по лоту")
            text = f"Название: {lead.name}\nОписание: {lead.description}\nСтартовая цена: {lead.price}$"
            if lead.photo is not None:
                next_step = bot.send_photo(message.chat.id, photo=open(lead.photo, 'rb'), caption=text,
                                           reply_markup=confirm_markup)
                bot.register_next_step_handler(next_step, finalize_lead, lead)
            elif lead.video is not None:
                next_step = bot.send_video(message.chat.id, video=open(lead.video, 'rb'), caption=text,
                                           reply_markup=confirm_markup)
                bot.register_next_step_handler(next_step, finalize_lead, lead)
            else:
                next_step = bot.send_message(message.chat.id, text, reply_markup=confirm_markup)
                bot.register_next_step_handler(next_step, finalize_lead, lead)

        def finalize_lead(message, lead):
            if message.text == 'Всё верно':
                database.add_info_in_table(lead)
                bot.send_message(message.chat.id, "Заглушка отправки лота", reply_markup=ReplyKeyboardRemove())
                ChannelManager.send_lot_to_channel(bot, lead)
            elif message.text == 'Отменить создание лота':
                bot.send_message(message.chat.id, 'Создание лота отменено', reply_markup=ReplyKeyboardRemove())
            else:
                bot.send_message(message.chat.id, "Команда не распознана", reply_markup=ReplyKeyboardRemove())


        @bot.callback_query_handler(func=lambda call: True)
        def query_handler(call):

            bot.answer_callback_query(callback_query_id=call.id, )
            message_id = call.message.chat.id
            data = call.data
            if data == 'make_lead':
                lead = Lead()
                get_lead_name(message_id, lead)





        print("Ready")
        bot.infinity_polling()
