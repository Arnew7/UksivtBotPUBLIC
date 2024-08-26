import os
# Устанавливаем соединение с базой данных
import sqlite3

def create_DB():
# Подключение к базе данных
    if not os.path.exists('UKSIVTsup.db'):
        conn = sqlite3.connect('UKSIVTsup.db')
        cursor = conn.cursor()

        # Создание таблицы
        cursor.execute('''CREATE TABLE info_users
                       (user_id INTEGER PRIMARY KEY, group_inf TEXT, username TEXT DEFAULT 'null')''')

        conn.commit()
        conn.close()
    else:
        return