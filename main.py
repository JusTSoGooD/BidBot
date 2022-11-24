import TG_bot
import database

if __name__ == '__main__':
    database.create_users_table()
    database.create_table_lots()
    key = "5930644426:AAFuHA6TvisDtSxXBDRfBOX2r6x_TqTDh6k"
    TG_bot.TgBot().start_bot(key)


