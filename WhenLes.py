import datetime
import asyncio
offset = datetime.timedelta(hours=5)
tz = datetime.timezone(offset)

Nlesson = 1
schedule = {
    2: {  # Среда
        1: datetime.time(7, 50),
        2: datetime.time(9, 30),
        3: datetime.time(11, 15),
        4: datetime.time(13, 35),
        5: datetime.time(16, 10),
        6: datetime.time(17, 40),
        7: datetime.time(19, 0)
    },
    5: {  # Суббота
        1: datetime.time(8, 0),
        2: datetime.time(9, 30),
        3: datetime.time(11, 0),
        4: datetime.time(12, 30),
        5: datetime.time(14, 0),
        6: datetime.time(15, 30),
        7: datetime.time(17, 0)
    }
}


default_schedule = {
    1: datetime.time(7, 50),
    2: datetime.time(9, 30),
    3: datetime.time(11, 15),
    4: datetime.time(13, 35),
    5: datetime.time(15, 20),
    6: datetime.time(17, 0),
    7: datetime.time(18, 30)
}


async def get_time_delta(NLesson):
    today = datetime.date.today()
    weekday = today.weekday()

    # Получаем расписание для текущего дня
    Ring = schedule.get(weekday, default_schedule)

    now = datetime.datetime.now().time()

    if NLesson in Ring:
        pair_time = Ring[NLesson]
        now_datetime = datetime.datetime.combine(today, now)
        pair_datetime = datetime.datetime.combine(today, pair_time)

        # Если текущее время больше времени начала пары
        if now > pair_time:
            # Если сегодня суббота после последней пары
            if weekday == 5 and NLesson == max(Ring.keys()):
                monday_lesson = default_schedule[1]
                return f"Уроков больше нет. Следующий урок в понедельник в {monday_lesson}."
            else:
                pair_datetime += datetime.timedelta(days=1)
                delta = pair_datetime - now_datetime
                return delta


        delta = pair_datetime - now_datetime
        return delta
    else:
        return None


async def WLesson(user_input):
    try:
        user_input = int(user_input)
        time_delta = await get_time_delta(user_input)

        if isinstance(time_delta, str):
            return (time_delta)  # следующий урок в понедельник
        elif time_delta is not None:
            hours, remainder = divmod(time_delta.total_seconds(), 3600)
            minutes, _ = divmod(remainder, 60)
            return (f"До начала {user_input}-й пары осталось: {int(hours)} часов и {int(minutes)} минут.")
        else:
            return ("Некорректный номер пары.")
    except ValueError:
        return ("Пожалуйста, введите корректное число.")


if __name__ == "__main__":
    asyncio.run(WLesson())
