import gc
from TGbot import text, textT
import datetime
offset = datetime.timedelta(hours=5)
tz = datetime.timezone(offset)

async def start_return(group):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    Day = today.strftime('%d')
    Month = today.strftime('%m')
    Day_t = tomorrow.strftime('%d')
    Month_t = tomorrow.strftime('%m')

    if today.weekday() == 6:  # Проверяем, если сегодня воскресенье

        taskT = await Return(group, textT, date=1)
        result = f'Замены:\nНа {Day}.{Month} \nНе учебный день"\n\nНа {Day_t}.{Month_t} {taskT}'
        return result
    elif tomorrow.weekday() == 6:
        task = await Return(group, text, date=0)

        result = f"Замены:\nНа {Day}.{Month} {task}\n\nНа {Day_t}.{Month_t} \nНе учебный день"
        return result


    else:
        task = await Return(group, text, date=0)
        taskT = await Return(group, textT, date=1)
        result = f"Замены:\nНа {Day}.{Month}{task}\n\nНа {Day_t}.{Month_t} {taskT}"
        return result


async def Return(group, text, date):
    if date == 1:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        Day = tomorrow.strftime('%d')
        Month = tomorrow.strftime('%m')
    else:
        Day = datetime.date.today().strftime('%d')
        Month = datetime.date.today().strftime('%m')


    groups = (
                '23ПО-2', '23ВЕБ-1', '23ВЕБ-2', '23З-1', '23З-2', '23Л-1', '23Л-2', '23ОИБ-1', '23ОИБ-2',
                '23П-1', '23П-2', '23П-3', '23П-4', '23П-5', '23П-6', '23ПД-1', '23ПД-2', '23ПО-1', '23ПО-2',
                '23ПО-3', '23ПО-4', '23ПО-5', '23СА-1', '23СА-2', '23СА-3', '23уКСК-1', '23уЛ-1', '23Э-1',
                '23Э-2',

                '22БД-1', '22ВЕБ-1', '22ВЕБ-2', '22ЗИО-1', '22ЗИО-2', '22ИС-1', '22Л-1', '22Л-2',
                '22ОИБ-1', '22ОИБ-2', '22П-1', '22П-2', '22П-3', '22ПД-1', '22ПД-2', '22ПО-1', '22ПО-2',
                '22ПО-3', '22ПСА-1', '22ПСА-2', '22ПСА-3', '22СА-1', '22СА-2', '22уКСК-1', '22уКСК-2',
                '22Э-1', '22Э-2',

                '21БД-1', '21ВЕБ-1', '21ВЕБ-2', '21ЗИО-1', '21ЗИО-2', '21ЗИО-3',
                '21ИС-1', '21Л-1', '21Л-2', '21ОИБ-1', '21ОИБ-2', '21ОИБ-3', '21П-1', '21П-2', '21П-3',
                '21ПД-1', '21ПД-1' '21ПД-2', '21ПД-2' '21ПД-3', '21ПД-3'  '21ПО-1', '21ПО-1', '21ПО-2', '21ПО-2' '21ПО-3', '21ПО-4',
                '21ПСА-1', '21ПСА-2' '21ПСА-3', '21ПСА-4', '21ПСА-6', '21СА-1',
                '21СА-2', '21СА-2', '21уКСК-1', '21Э-1', '21Э-2',

                '20ВЕБ-1', '20ВЕБ-2' '20ИС-1', '20ОИБ-1', '20П-1', '20П-3',
                '20СА-1')

    #Функция для удаления группы из текста и обрезки до начала следующей группы
    async def remove_L(text, group):
        index = text.find(group)  # Находим индекс начала группы в тексте
        text = text[index:].replace(group, "")  # Удаляем группу и обрезаем текст
        return text

    # Функция для поиска следующей группы из списка
    async def indexing(text, groups):

        min_index = len(text)  # Устанавливаем начальное минимальное значение индекса
        for i in groups:
            index = text.find(i)
            if index == -1 and '-' in i:  # Если группа не найдена и содержит дефис
                i = i.split('-')[0]  # Берем только часть до дефиса
                index = text.find(i)
            if index != -1 and index < min_index:  # Если группа найдена и индекс меньше текущего минимального
                min_index = index  # Обновляем минимальный индекс
        if min_index != len(text):  # Если был найден индекс
            text = text[:min_index]  # Обрезаем текст до начала следующей группы
        return text.lower()

    # Функция для получения уникальных замен для заданной группы
    async def replacements(text, group, groups):
        text = await remove_L(text, group)  # Удаляем группу и обрезаем текст
        text = await indexing(text, groups)  # Находим конец текста до следующей группы
        print(len(text))
        if len(text) <= 12:

            return f" отсутствуют"
        elif "-на практике" in text:
            return f" отсутствуют"
        else:

            unique_replacements = set()  # Множество для хранения уникальных замен
            for line in text.split('\n'):  # Перебираем строки в конечном тексте
                if line.strip() not in unique_replacements:  # Проверяем уникальность строки
                    unique_replacements.add(line.strip())  # Добавляем уникальную строку в множество

            return f"{'\n'.join(unique_replacements)}"

    result = await replacements(text, group, groups)
    print(result)
    gc.collect()
    return result



