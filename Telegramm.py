import gc

from TGbot import TGstart
import asyncio
import logging
from RReturn import start_return
from aiogram import Bot, Dispatcher, types
import questions
import datetime
from DB import create_DB
import sqlite3
import psutil
import os
import sys
offset = datetime.timedelta(hours=5)
tz = datetime.timezone(offset)

create_DB()
bot = Bot(token="Ваш токен")
dp = Dispatcher()


async def send_reschedule():

    try:

        conn = sqlite3.connect('UKSIVTsup.db')
        cur = conn.cursor()

        # Выборка данных из таблицы info_users
        cur.execute("SELECT user_id, group_inf FROM info_users")
        rows = cur.fetchall()



        for row in rows:
            user_id = row[0]

            group_inf = row[1]

            print(user_id)
            print(group_inf)

            chat = types.Chat(id=user_id, type='private')
            text = await start_return(group_inf)
            import gc




            try:
                await bot.send_message(chat_id=user_id, text=(text))
                gc.collect()

            except:
                logging.error(f"Error sending message to user_id {user_id}")


        cur.close()
        conn.close()
    except Exception as ex:
        logging.error(f"An error occurred: {ex}")



async def job():
    while True:
        now = datetime.datetime.now()
        if now.hour == 5 and now.minute == 0:
            await send_reschedule()
            # Ждем до следующего дня
            tomorrow = now + datetime.timedelta(days=1)
            next_day = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 5, 0)
            seconds_until_next_day = (next_day - now).total_seconds()
            await asyncio.sleep(seconds_until_next_day)
            gc.collect()
        else:
            # Ждем 1 минуту и проверяем снова
            await asyncio.sleep(60)

async def RestartTG():
    while True:
        try:
            await TGstart()
            process = psutil.Process()

            await asyncio.sleep(60)
            gc.collect()
        except Exception as e:

            asyncio.run(RestartTG())


async def start_bot():

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        task_job = asyncio.create_task(job())  # Запускаем job как асинхронную задачу
        task_restart = asyncio.create_task(RestartTG())
        dp.include_router(questions.router)
        await dp.start_polling(bot)
        await task_job  # Ожидаем завершения задачи job
        await task_restart  # Ожидаем завершения задачи RestartTG
    except Exception as ex:
        logging.error(f"An error occurred while starting the bot: {ex}")
        asyncio.run(RestartTG())

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(start_bot())
            asyncio.run(RestartTG())

              # Вызываем основной код
        except Exception as e:
            python = sys.executable  # Получаем путь к интерпретатору Python
            os.execl(python, python, *sys.argv)


job()
