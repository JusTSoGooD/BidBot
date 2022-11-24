import time
import database


def calculate_ending_time(end_interval):
    return int(time.mktime(time.localtime())) + end_interval


def get_time_until_auction_end(lead_id):
    lead = database.get_lead_from_db(lead_id)
    lead_end_time = int(lead.end_time)
    interval = lead_end_time - int(time.mktime(time.localtime()))
    result = time.gmtime(interval)
    if interval > 0:
        return f'{result.tm_hour}ч. {result.tm_min} мин. {result.tm_sec} сек.'
    if interval <= 0:
        return None
