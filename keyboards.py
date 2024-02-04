from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData


async def start_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Хочу попасть в базу ЕРА', callback_data='bloger'),
        InlineKeyboardButton(text='Менеджер блогеров / агенство', callback_data='manager'),
        InlineKeyboardButton(text='Хочу работать в ЕРА', callback_data='work'),
        InlineKeyboardButton(text='Influence-GR', callback_data='barter'),
        InlineKeyboardButton(text='Сотрудничество', callback_data='colab_start'),
        InlineKeyboardButton(text='Эксклюзивный контракт', callback_data='exclusive_conract'),
        InlineKeyboardButton(text='Контакты', callback_data='contacts')
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup

# ВОЗМОЖНО НЕ ПРИГОДИТСЯ (СТАРАЯ КЛАВА ДЛЯ СОТРУДНЧЕСТВА)
# async def colab_keyboard() -> InlineKeyboardMarkup:
#     buttons = [
#         InlineKeyboardButton(text='Бартер', callback_data='barter'),
#         InlineKeyboardButton(text='Я менеджер блогеров', callback_data='manager'),
#         InlineKeyboardButton(text='Сотрудничество с ЕРА', callback_data='colab_start'),
#         InlineKeyboardButton(text='Назад', callback_data='start')
#     ]
#     markup = InlineKeyboardMarkup(row_width=1)
#     markup.add(*buttons)
#     return markup


async def manager_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Да. Можем найти блогеров исходя из запроса клиента', callback_data='y'),
        InlineKeyboardButton(text='Нет. Работаю только со своими блогерами', callback_data='n')
    ]
    markup = InlineKeyboardMarkup( row_width=1)
    markup.add(*buttons)
    return markup


async def bloger_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Instagram', callback_data='Instagram'),
        InlineKeyboardButton(text='YouTube', callback_data='YT'),
        InlineKeyboardButton(text='VK', callback_data='VK'),
        InlineKeyboardButton(text='Telegram', callback_data='TG'),
        InlineKeyboardButton(text='Дзен', callback_data='Дзен'),
        InlineKeyboardButton(text='Другое', callback_data='Другое'),
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
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [InlineKeyboardButton(text=i, callback_data=f'Topic_{i}') for i in lst]
    markup.add(*buttons)
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


async def registr_end() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Добавить еще одну социальную сеть', callback_data='bloger'),
        InlineKeyboardButton(text='Завершить регистрацию', callback_data='start'),
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup


async def reels_keyboard(media) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Да ✅', callback_data=f'reels_yes_{media}'),
        InlineKeyboardButton(text='Нет ❌', callback_data=f'reels_no_{media}')
    ]
    markup = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*buttons)
    markup.add(InlineKeyboardButton(text=f'Отменить регистрацию', callback_data='start'))
    return markup


async def back_keyboard(string) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=f'{string}', callback_data='start'),
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup


async def pass_keyboard(q) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text='Пропустить вопрос', callback_data=f'pass_{q}'),
    ]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(*buttons)
    return markup


