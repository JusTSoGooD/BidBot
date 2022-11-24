import telebot
import markups
from lead import Lead
import ChannelManager
import database
import Lot_order


class TgBot:

    @staticmethod
    def start_bot(key):
        bot = telebot.TeleBot(key)
        admin_menu = markups.get_main_menu_admin()
        main_menu = markups.get_main_menu_markup()
        back_to_main_menu_markup = markups.get_back_to_main_menu_markup()

        sql_connection = database.sql_connection()
        cursor = sql_connection.cursor()
        database.create_table_lots(sql_connection, cursor)

        @bot.message_handler(content_types=['text'])
        def start(message):

            lot_id = message.text.replace("/start ", '')

            print(lot_id)
            if message.text == "/start " + lot_id:
                print(lot_id)
                lead = database.get_lead_from_db(lot_id)
                ChannelManager.send_lot_to_bot(bot, lead, message)

            if message.text == '/admin':
                bot.send_message(message.chat.id, 'Главное админ меню', reply_markup=admin_menu)

            if message.text == '/start':
                bot.send_message(message.chat.id, 'Привет, я бот аукционов *название канала* Удачных торгов!',
                                 reply_markup=main_menu)

        @bot.callback_query_handler(func=lambda call: True)
        def query_handler(call):

            bot.answer_callback_query(callback_query_id=call.id, )
            chat_id = call.message.chat.id
            data = call.data
            if data == 'make_lead':
                lead = Lead()
                Lot_order.get_lead_name(chat_id, lead, bot)

            if data == 'my_aucc':
                bot.delete_message(chat_id, call.message.id)
                bot.send_message(chat_id, 'Заглушка моих аукционов:', reply_markup=back_to_main_menu_markup)

            if data == 'rules':
                bot.delete_message(chat_id, call.message.id)
                bot.send_message(chat_id, '''После окончания торгов,победитель или продавец должены выйти на связь в течении суток‼️
Победитель обязан выкупить лот в течении ТРЁХ дней,после окончания аукциона 🔥
И прочие правила. Абоба.''', reply_markup=back_to_main_menu_markup)

            if data == 'statistics':
                bot.delete_message(chat_id, call.message.id)
                bot.send_message(chat_id, 'Заглушка графы статистики', reply_markup=back_to_main_menu_markup)

            if data == 'help':
                bot.delete_message(chat_id, call.message.id)
                bot.send_message(chat_id,
                                 'Свяжитесь с нами, если у вас возникли вопросы @JeanS_So_TighT.\n Удачных торгов и выгодных покупок!',
                                 reply_markup=back_to_main_menu_markup)

            if data == 'fuckgoback':
                bot.delete_message(chat_id, call.message.id)
                bot.send_message(chat_id, 'Привет, я бот аукционов *название канала* Удачных торгов!',
                                 reply_markup=main_menu)

        print("Ready")
        bot.infinity_polling()
