import re

import telebot

import Time_manager
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

        @bot.message_handler(content_types=['text'])
        def start(message):

            lot_id = message.text.replace("/start ", '')
            if message.text == "/start " + lot_id:
                lead = database.get_lead_from_db(lot_id)
                ChannelManager.send_lot_to_bot(bot, lead, message)

            if message.text == '/admin':
                bot.send_message(message.chat.id, 'Главное админ меню', reply_markup=admin_menu)

            if message.text == '/start':
                bot.send_message(message.chat.id, 'Привет, я бот аукционов *название канала* Удачных торгов!',
                                 reply_markup=main_menu)

        @bot.callback_query_handler(func=lambda call: True)
        def query_handler(call):


            chat_id = call.message.chat.id
            data = call.data
            flag = data[0]
            lot_id = re.search("[A-Z]+", data)
            lot_id = lot_id[0]

            if data == 'make_lead':
                lead = Lead()
                Lot_order.get_lead_name(chat_id, lead, bot)

            if data == 'my_aucc':
                bot.delete_message(chat_id, call.message.id)
                bot.send_message(chat_id, 'Заглушка моих аукционов:', reply_markup=back_to_main_menu_markup)

            if data == 'rules':
                bot.delete_message(chat_id, call.message.id)
                bot.send_message(chat_id, '''После окончания торгов,победитель или продавец должены выйти на связь в 
                течении суток‼️ Победитель обязан выкупить лот в течении ТРЁХ дней,после окончания аукциона 🔥 И 
                прочие правила. Абоба.''', reply_markup=back_to_main_menu_markup)

            if data == 'statistics':
                bot.delete_message(chat_id, call.message.id)
                bot.send_message(chat_id, 'Заглушка графы статистики', reply_markup=back_to_main_menu_markup)

            if data == 'help':
                bot.delete_message(chat_id, call.message.id)
                bot.send_message(chat_id,
                                 'Свяжитесь с нами, если у вас возникли вопросы @JeanS_So_TighT.\n Удачных торгов и '
                                 'выгодных покупок!',
                                 reply_markup=back_to_main_menu_markup)

            if data == 'fuckgoback':
                bot.delete_message(chat_id, call.message.id)
                bot.send_message(chat_id, 'Привет, я бот аукционов *название канала* Удачных торгов!',
                                 reply_markup=main_menu)

            if data == 'info':
                bot.answer_callback_query(call.id,
                                          text='''Делая ставку участник подтверждает желание и возможность выкупить лот, 
в случае невыкупа лота участника ебет в жопу грузин!''',
                                          show_alert=True)
            if flag == 'T':
                lead_id = data[1:]
                end_time = Time_manager.get_time_until_auction_end(lead_id)
                if end_time is None:
                    bot.answer_callback_query(call.id, "Аукцион завершен", show_alert=False)
                else:
                    bot.answer_callback_query(call.id, f"До конца аукциона {end_time}", show_alert=False)


            if data == 'bid100_' + lot_id:
                lot = database.get_lead_from_db(lot_id)
                lot.price = lot.price + 100

                pass
            if data == 'bid200_' + lot_id:
                pass
            if data == 'bid300_' + lot_id:
                pass
            if data == 'time_' + lot_id:
                pass





        print("Ready")
        bot.infinity_polling()
