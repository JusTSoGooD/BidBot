import sqlite3
import lead
from sqlite3 import Error
import Time_manager


def sql_connection():
    try:

        connection = sqlite3.connect('hard.db')

        print("Connection is established: Database is created in hard")
        return connection
    except Error:

        print(Error)


def create_table_lots(connection, cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS lots(
             ID_LOT TEXT PRIMARY KEY,
             Name TEXT,
             Description TEXT, 
             Price TEXT,
             end_time TEXT,
             Winner TEXT)
        """)
    connection.commit()
    print('done')


def add_info_in_table(lead):
    connection = sql_connection()
    cursor = connection.cursor()
    lead.end_time = Time_manager.calculate_ending_time(lead.end_time)
    insert_in_db = f"""INSERT INTO lots (ID_LOT, Name, Description, Price, end_time) 
                    VALUES ('{lead.id}', '{lead.name}', '{lead.description}', '{lead.price}', '{lead.end_time}'); """
    cursor.execute(insert_in_db)
    connection.commit()


def get_lead_from_db(id):
    connection = sql_connection()
    cursor = connection.cursor()
    sql_select_lead = f"""SELECT * FROM lots WHERE ID_LOT = ?"""
    cursor.execute(sql_select_lead, (id,))
    records = cursor.fetchall()
    lot = lead.Lead()
    for row in records:
        lot.id = row[0]
        lot.name = row[1]
        lot.description = row[2]
        lot.price = row[3]
        lot.end_time = row[4]

    return lot
