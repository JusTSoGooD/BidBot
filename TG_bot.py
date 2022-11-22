import telebot
import markups
import lead

class tgBot:





    def start_bot(self, key):
        bot = telebot.TeleBot(key)
        admin_menu = markups.get_main_menu_admin()
        main_menu = markups.get_main_menu_markup()

        @bot.message_handler(content_types=['text'])
        def start(message):
            if message.text == '/admin':
                bot.send_message(message.chat.id, "Главное админ меню", reply_markup = admin_menu)

            if message.text == '/start':
                bot.send_message(message.chat.id, 'Привет, я бот аукционов *название канала* Удачных торгов!', reply_markup = main_menu)
                
        @bot.message_handler(content_types=['Text'])
        def handle_text(message):
            return message.text

        def fill_lead(id):

            mesg = bot.send_message(id, 'введите название лота')

            bot.register_next_step_handler(mesg, get_lead_name)

        def get_lead_name(message):
            mesg = message.text
            bot.register_next_step_handler(mesg, get_lead_price )

        def get_lead_price(message):
            mesg = message.text
            bot.register_next_step_handler(mesg, get_lead_time)

        def get_lead_time(message):
            mesg = message.text






        @bot.callback_query_handler(func=lambda call: True)
        def query_handler(call):

            bot.answer_callback_query(callback_query_id=call.id, )
            message_id = call.message.chat.id
            data = call.data

            if data == 'make_lead':
                fill_lead(message_id)


        print("Ready")
        bot.infinity_polling()

