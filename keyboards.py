from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

EventsCallback = CallbackData('event', 'action', 'id')


async def start_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Хочу быть блогером ЕРА', callback_data='bloger'),
        InlineKeyboardButton(text='Хочу работать в ЕРА', callback_data='work'),
        InlineKeyboardButton(text='Сотрудничетсво', callback_data='collaboration'),
        InlineKeyboardButton(text='Контакты', callback_data='contacts')
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup


async def colab_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Бартер', callback_data='barter'),
        InlineKeyboardButton(text='Я мнеджер блогеров, хочу сотрудничать с ЕРА', callback_data='manager'),
        InlineKeyboardButton(text='Сотрудничетсво с ЕРА', callback_data='colab_start'),
        InlineKeyboardButton(text='Назад', callback_data='start')
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup


async def manager_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text='Да✅'),
        KeyboardButton(text='Нет❌')
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*buttons)
    return markup


async def bloger_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Instagram', callback_data='Instagram'),
        InlineKeyboardButton(text='YouTube', callback_data='YT'),
        InlineKeyboardButton(text='VK', callback_data='VK'),
        InlineKeyboardButton(text='Telegram', callback_data='TG'),
        InlineKeyboardButton(text='Дзен', callback_data='Дзен'),
        InlineKeyboardButton(text='Назад', callback_data='start')
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup


async def number_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text='Да✅'),
        KeyboardButton(text='нет, ввести другой')
    ]
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*buttons)
    return markup


async def topic_keyboard(lst) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=1)
    for i in lst:
        button = InlineKeyboardButton(text=i, callback_data=f'Topic_{i}')
        markup.add(button)
    button = InlineKeyboardButton(text="✅Закончить выбор", callback_data='topic_end')
    markup.add(button)
    return markup


async def topic_keyboard_2() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Выбрать еще категорию', callback_data='topic_start'),
        InlineKeyboardButton(text='✅Закончить выбор', callback_data='topic_end'),
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup


async def back_keyboard(string) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=f'{string}', callback_data='start'),
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup


