import telebot
import markups

CHANNEL_ID = -1001843060074


def send_lot_to_channel(bot, lead):
    text = f"Название: {lead.name}\nОписание: {lead.description}\nВремя окончания: через {lead.end_time} секунд\n" \
           f"Стартовая цена: {lead.price} $ "
    if lead.video is not None:
        bot.send_video(CHANNEL_ID, video=open(lead.video, 'rb'), caption=text,
                       reply_markup=markups.get_group_lot_markup(lead))
    elif lead.photo is not None:
        bot.send_photo(CHANNEL_ID, photo=open(lead.photo, 'rb'), caption=text,
                       reply_markup=markups.get_group_lot_markup(lead))
    else:
        bot.send_message(CHANNEL_ID, text,
                         reply_markup=markups.get_group_lot_markup(lead))


def send_lot_to_bot(bot, lead, message):
    text = f" {lead.name}\n {lead.description}\nСтартовая цена: {lead.price} $"
    if lead.video is not None:
        bot.send_video(message.chat.id, video=open(lead.video, 'rb'), caption=text,
                       reply_markup=markups.get_lead_in_bot_markup(lead))
    elif lead.photo is not None:
        bot.send_photo(message.chat.id, photo=open(lead.photo, 'rb'), caption=text,
                       reply_markup=markups.get_lead_in_bot_markup(lead))
    else:
        bot.send_message(message.chat.id, text,
                         reply_markup=markups.get_lead_in_bot_markup(lead))

