

from aiogram import Bot
from RReturn import start_return
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Router, F
from WhenLes import WLesson




bot = Bot(token="Ваш токен")

import sqlite3
import asyncio
from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Список всех групп
router = Router()

NUMBER = ['1','2','3','4','5','6','7']
# Список всех групп
YEARS = ['2024', '2023', '2022', '2021']
DIRECTIONS = {
    '2024': ['24ВЕБ','24з', '24ИИС',
             '24Л', '24ОИБ','24П',
             '24ПД','24СА','24уКСК',
             '24уЛ','24Э', '24Ю'],
    
    
    
    '2023': ['23ПО', '23ВЕБ','23з',
             '23Л', '23ОИБ','23П',
             '23ПД','23СА','23уКСК',
             '23уЛ','23Э'],

    '2022': ['22БД', '22ВЕБ', '22ЗИО' ,
             '22ИС', '22Л','22ОИБ',
             '22П', '22ПД', '22ПО',
             '22ПСА', '22СА', '22уКСК',
             '22Э'],

    '2021': ['21БД', '21ВЕБ', '21ЗИО',
             '21ИС', '21Л', '21ОИБ',
             '21П', '21ПД',  '21ПО',
             '21ПСА', '21СА'
             ,'21уКСК', '21Э']

}
GROUPS = {
    '24уКСК':["24уКСК-1","24уКСК-2"],
    '24СА':["24СА-1","24СА-2", "24СА-3"],
    '24П':["24П-1","24П-2","24П-3","24П-4","24П-5"],
    '24ВЕБ':["24ВЕБ-1","24ВЕБ-2"],
    '24ИИС':["24ИИС-1","24ИИС-2"],
    '24ОИБ':["24ОИБ-1","24ОИБ-2","24ОИБ-3"],
    '24з':["24з-1","24з-2"],
    '24Э':["24Э-1","24Э-2"],
    '24Ю':["24Ю-1","24Ю-2","24Ю-3","24Ю-4"],
    '24ПД':["24ПД-1","24ПД-2","24ПД-3"],
    '24Л':["24Л-1","24Л-2"],
    '24уЛ':["24уЛ-1"],
    '23ВЕБ': ['23ВЕБ-1', '23ВЕБ-2'],
    '23ПО': ['23ПО-1', '23ПО-2'],
    '23СА': ['23СА-1', '23СА-2'],
    '23уКСК': ['23уКСК-1'],
    '23уЛ': ['23уЛ-1'],
    '23Э': ['23З-1', '23З-2'],
    '23П': ['23П-1', '23П-2', '23П-3', '23П-4', '23П-5', '23П-6'],
    '23ПД': ['23ПД-1', '23ПД-2'],
    '23ОИБ': ['23ОИБ-1', '23ОИБ-2'],
    '23з': ['23з-1', '23з-2'],
    '23Л': ['23Л-1', '23Л-2'],
    '22БД':['22БД-1'],
    '22ВЕБ':['22ВЕБ-1', '22ВЕБ-2'],
    '22ЗИО':['22ЗИО-1', '22ЗИО-2'],
    '22ИС':['22ИС-1'],
    '22Л':['22Л-1', '22Л-2'],
    '22ОИБ':['22ОИБ-1', '22ОИБ-2'],
    '22П':['22П-1', '22П-2', '22П-3'],
    '22ПД':['22ПД-1', '22ПД-2'],
    '22ПО':['22ПО-1', '22ПО-2','22ПО-3'],
    '22ПСА':['22ПСА-1', '22ПСА-2', '22ПСА-3'],
    '22СА':['22СА-1', '22СА-2'],
    '22уКСК':['22уКСК-1', '22уКСК-2'],
    '22Э':['22Э-1', '22Э-2'],
    '21БД':['21БД-1'],
    '21ВЕБ':["21ВЕБ-1", '21ВЕБ-2'],
    '21ЗИО':['21ЗИО-1', '21ЗИО-2', '21ЗИО-3'],
    '21ИС':['21ИС-1'],
    '21Л':['21Л-1', '21Л-2'],
    '21ОИБ':['21ОИБ-1', '21ОИБ-2', '21ОИБ-3'],
    '21П':['21П-1', '21П-2', '21П-3'],
    '21ПД':['21ПД-1', '21ПД-2', '21ПД-3'],
    '21ПО':['21ПО-1', '21ПО-2', '21ПО-3', '21ПО-4',],
    '21ПСА':['21ПСА-1', '21ПСА-2', '21ПСА-3', '21ПСА-4', '21ПСА-6'],
    '21СА':['21СА-1', '21СА-2'],
    '21уКСК':['21уКСК-1'],
    '21Э':['21Э-1', '21Э-2']

}

# Функция для работы с базой данных
async def update_user_info(user_id, group, username=None):
    conn = sqlite3.connect('UKSIVTsup.db')
    cur = conn.cursor()

    if username is not None:
        cur.execute(
            "INSERT INTO info_users(user_id, group_inf, username) VALUES (?, ?, ?) ON CONFLICT (user_id) "
            "DO UPDATE SET group_inf = excluded.group_inf, username = excluded.username",
            (user_id, group, username))
    else:
        print("Ошибка: значение username равно None")
        cur.execute(
            "INSERT INTO info_users(user_id, group_inf) VALUES (?, ?) ON CONFLICT (user_id) DO UPDATE SET group_inf = ?",
            (user_id, group, group))

    conn.commit()
    cur.close()
    conn.close()



def create_inline_keyboard(buttons):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[  # Добавляем список кнопок
            [InlineKeyboardButton(text=text, callback_data=callback_data)]
            for text, callback_data in buttons
        ]
    )
    return keyboard

@router.callback_query(lambda c: c.data in YEARS)
async def year_handler(callback: types.CallbackQuery):
    year = callback.data
    await callback.answer()

    # Создаем кнопки для направлений
    buttons = [(direction, direction) for direction in DIRECTIONS[year]]
    await callback.message.edit_text("Выберите направление:", reply_markup=create_inline_keyboard(buttons))

@router.callback_query(lambda c: c.data in [direction for directions in DIRECTIONS.values() for direction in directions])
async def direction_handler(callback: types.CallbackQuery):
    direction = callback.data
    await callback.answer()

    # Создаем кнопки для групп
    buttons = [(group, group) for group in GROUPS[direction]]
    await callback.message.edit_text("Выберите группу:", reply_markup=create_inline_keyboard(buttons))

@router.callback_query(lambda c: c.data in [group for groups in GROUPS.values() for group in groups])
async def group_handler(callback: types.CallbackQuery):
    group = callback.data
    await callback.answer()

    user_id = callback.from_user.id
    username = callback.from_user.username

    await update_user_info(user_id, group, username)

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Replacment",
        callback_data="Replacment")
    )
    builder.add(types.InlineKeyboardButton(
        text="Ring",
        callback_data="Ring")
    )

    await callback.message.answer(
            """  Menu:
Replacment - запрос замен
Ring - Через сколько X пара            
            
                            """ ,
        reply_markup=builder.as_markup(),
    )

    SF = await callback.message.edit_text(f"Группа {group} сохранена!")
    text = await start_return(group)
    ANS = await callback.message.answer(text)
    await asyncio.sleep(9)
    await SF.delete()
    await asyncio.sleep(16)
    await ANS.delete()

@router.callback_query(F.data == "Replacment")
async def Replacment(callback: types.CallbackQuery):
    # Создаем кнопки для выбора года
    buttons = [(year, year) for year in YEARS]
    await callback.message.edit_text("Пожалуйста, выберите год:", reply_markup=create_inline_keyboard(buttons))


@router.message(Command("start"))
async def start(message: types.Message):
    # Сохраняем данные о пользователе
    global user_id
    global username
    user_id = message.from_user.id
    username = message.from_user.username


    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Replacment",
        callback_data="Replacment")
    )
    builder.add(types.InlineKeyboardButton(
        text="Ring",
        callback_data="Ring")
    )

    await message.answer(
        """      Menu:
Replacment - запрос замен
Ring - Через сколько X пара            
            
                            """ ,
        reply_markup=builder.as_markup(),
    )

@router.callback_query(F.data == "Ring")
async def Ring(callback: types.CallbackQuery):
    buttons = [(num, num) for num in NUMBER]
    ANSr = await callback.message.edit_text("Пожалуйста, выберите номер группы:", reply_markup=create_inline_keyboard(buttons))
    await asyncio.sleep(9)
    await ANSr.delete()

@router.callback_query(F.data.in_(NUMBER))  # Обработчик для выбора номера группы
async def handle_group_selection(callback: types.CallbackQuery):
    await callback.message.edit_reply_markup()
    num = callback.data  # Здесь мы получаем выбранный номер группы
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Replacment",
        callback_data="Replacment")
    )
    builder.add(types.InlineKeyboardButton(
        text="Ring",
        callback_data="Ring")
    )

    await callback.message.answer(
        """      Menu:
Replacment - запрос замен
Ring - Через сколько X пара            
            
                            """ ,
        reply_markup=builder.as_markup(),
    )
    ANSr = await WLesson(num)
    ANSr = await callback.message.answer(ANSr)
    await asyncio.sleep(9)
    await ANSr.delete()



