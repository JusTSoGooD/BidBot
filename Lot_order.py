import markups
from telebot.types import ReplyKeyboardRemove
import ChannelManager
import database
import os

confirm_markup = markups.get_confirm_markup()
time_markup = markups.get_time_gap_markup()

path = os.path.abspath(__file__).rpartition('\\')[0]
if not os.path.exists(f'{path}\\Photo'):
    os.mkdir(f'{path}\\Photo')

if not os.path.exists(f'{path}\\Video'):
    os.mkdir(f'{path}\\Video')


def download_lead_photo(message, lead, bot):
    photo_id = message.photo[2].file_id
    file_path = bot.get_file(photo_id).file_path
    file = bot.download_file(file_path)
    with open(f'{path}\\Photo\\{lead.id}.jpg', 'wb') as code:
        code.write(file)


def download_lead_video(message, lead, bot):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'{path}\\Video\\{lead.id}.mp4', 'wb') as code:
        code.write(downloaded_file)


def get_lead_name(user_id, lead, bot):
    next_step = bot.send_message(user_id, 'Введите имя лота')
    bot.register_next_step_handler(next_step, get_lead_description, lead, bot)


def get_lead_description(message, lead, bot):
    lead.name = message.text
    next_step = bot.send_message(message.chat.id, 'Введите описание лота')
    bot.register_next_step_handler(next_step, get_lead_price, lead, bot)


def get_lead_price(message, lead, bot):
    lead.description = message.text
    next_step = bot.send_message(message.chat.id, 'Введите стартовую цену лота (в долярах)')
    bot.register_next_step_handler(next_step, get_end_time, lead, bot)


def get_end_time(message, lead, bot):
    lead.price = message.text
    next_step = bot.send_message(message.chat.id, 'С помощью кнопок определите время, через которое окончится аукцион',
                                 reply_markup=time_markup)
    bot.register_next_step_handler(next_step, get_lead_photo, lead, bot)


def get_lead_photo(message, lead, bot):
    if message.text == '2 минуты':
        lead.end_time = 120
    else:
        lead.end_time = 1000

    next_step = bot.send_message(message.chat.id,
                                 'Пришлите фотографию лота *в случае отсутствия фото отправьте любой символ*',
                                 reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(next_step, get_lead_video, lead, bot)


def get_lead_video(message, lead, bot):
    if message.content_type == 'photo':
        download_lead_photo(message, lead, bot)
        lead.photo = f'{path}\\Photo\\{lead.id}.jpg'

    next_step = bot.send_message(message.chat.id,
                                 'Пришлите видео с лотом *в случае отсутствия отправьте любой символ*')
    bot.register_next_step_handler(next_step, confirm_lead, lead, bot)


def confirm_lead(message, lead, bot):
    if message.content_type == 'video':
        download_lead_video(message, lead, bot)
        lead.video = f'{path}\\Video\\{lead.id}.mp4'

    bot.send_message(message.chat.id, "Проверьте, правильно ли введена информация по лоту")
    text = f"Название: {lead.name}\nОписание: {lead.description}\nВремя окончания: через {lead.end_time} секунд\n" \
           f"Стартовая цена: {lead.price}$ "
    if lead.photo is not None:
        next_step = bot.send_photo(message.chat.id, photo=open(lead.photo, 'rb'), caption=text,
                                   reply_markup=confirm_markup)
        bot.register_next_step_handler(next_step, finalize_lead, lead, bot)
    elif lead.video is not None:
        next_step = bot.send_video(message.chat.id, video=open(lead.video, 'rb'), caption=text,
                                   reply_markup=confirm_markup)
        bot.register_next_step_handler(next_step, finalize_lead, lead, bot)
    else:
        next_step = bot.send_message(message.chat.id, text, reply_markup=confirm_markup)
        bot.register_next_step_handler(next_step, finalize_lead, lead, bot)


def finalize_lead(message, lead, bot):
    if message.text == 'Всё верно':
        database.add_info_in_table(lead)
        bot.send_message(message.chat.id, "Лот отправлен", reply_markup=ReplyKeyboardRemove())
        ChannelManager.send_lot_to_channel(bot, lead)
    elif message.text == 'Отменить создание лота':
        bot.send_message(message.chat.id, 'Создание лота отменено', reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, "Команда не распознана", reply_markup=ReplyKeyboardRemove())
