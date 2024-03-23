import os
from aiogram import types, Dispatcher, types
from keyboards import start_keyboard, manager_keyboard, bloger_keyboard, number_keyboard, registr_end, work_keyboard
from keyboards import topic_keyboard, topic_keyboard_2, back_keyboard, back_keyboard2, reels_keyboard, pass_keyboard, client_keyboard
from keyboards import client_TypeColab_keyboard 
from aiogram.dispatcher import FSMContext
from states import SocMedia
from states import Work, Barter, Manager, Colab, Instagram, YT, VK, TG, DZ, Another, Manager_new, Work_write, Client
from funcs import get_config, Bloger, is_link, is_number
import time
from asyncio import sleep

# работа с гугл таблицами
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
         'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]
credentials_file = 'credentials.json'
spreadsheet_era_id = '1zCcn7vOub--6X7gQZ85UCkwCbTjxWjk7xl9b5Ffsqpk'
spreadsheet_bloger_id = '14eYmCcO-T5kCI0qOuD15ICfceIbBsZ9tn9JJ2pz9u7c'
creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
client = gspread.authorize(creds)


# ОБРАЗЕЦ ДЛЯ ПОДКЛЮЧЕНИЯ
# spreadsheet = client.open_by_key(spreadsheet_id)
# sheet = spreadsheet.get_worksheet(0)  # 0 refers to the first sheet


async def number_wrong(message, number=True,
                       text2='К сожалению, Вы прислали ссылку неверного формата. Повторно укажите сылку в формате "https://somesite.ru"'):
    text = 'Вы ввели номер неверного формата. Пожалуйства, следуйте формату +7***-***-**-**. \nВведите номер телефона повторно'
    if number == False:
        text = text2
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)


async def start(message: types.Message):
    text = '''Приветствую! На связи Единое Рекламное Агентство ЕРА ✌🏻Жми:

<b>Я блогер, хочу в базу ЕРА</b>
✏️ Получай рекламные/коммерческие и другие интересные предложения.

<b>Я Менеджер блогеров / агентство</b>
✏️ Интегрируем тебя и твоих блогеров ко входящим рекламным запросам наших клиентов.

<b>Хочу работать в ЕРА</b>
✏️Стань частью нашей большой команды. Мы найдем место для всех😉 

<b>Мероприятия и бартеры</b>
✏️ Получай уведомления о PR-событиях, мероприятиях и спец. проектах, которые ты можешь посетить бесплатно. В этой рубрике и другие бартеры: товарка, услуги и др. 

<b>Сотрудничество </b>
✏️Мы «за» сотрудничество, партнерство и участие в интересных проектах. Пиши, возможно, твое предложение актуально нам как никогда😉 

<b>Эксклюзивный контракт</b>
✏️Приоритет во всех проектах безусловно отдается резидassентам агентства. Прочитай информацию о том, как им можно стать.
'''
    markup = await start_keyboard()
    if isinstance(message, types.Message):
        await message.answer(text=text, reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        await message.message.answer(text=text, reply_markup=markup)


async def start_again(message: types.Message):
    text = '''Вы закончили регистрацию! Можете продолжить работу с нашим ботом в других разделах. '''
    markup = await start_keyboard()
    await message.answer(text=text, reply_markup=markup)


async def help(message: types.Message):
    await message.answer('help')


async def me(message: types.Message):
    print(message)

def deleter(func):
    async def wrapper(*args, **kwargs):
        if isinstance(args[0], types.CallbackQuery):
            if not args[0].data == 'back':
                await args[0].bot.delete_message(args[0].message.chat.id, args[0].message.message_id)
        else:
            await args[0].bot.delete_message(args[0].chat.id, args[0].message_id-1)
        return await func(*args, kwargs['state'])
    return wrapper


@deleter
async def back_start(message: types.Message, state: FSMContext):
    ''' старт после отмены регистрации'''
    await state.finish()
    await start(message)


async def back(call: types.CallbackQuery, state: FSMContext):
    await call.bot.delete_message(call.message.chat.id, call.message.message_id)
    res = await state.get_state()
    if res == None:
        await start_again(call.message)
        return

    if res.split(':')[0] == 'SocMedia':
        await SocMedia.previous()
        data = await state.get_data()
        func = data['func']
        await func(call, state=state)


    elif res.split(':')[0] == 'Manager_new':
        await Manager_new.previous()
        data = await state.get_data()
        func = data['func']
        await func(call, state=state)


    elif res.split(':')[0] == 'Colab':
        await SocMedia.previous()
        data = await state.get_data()
        func = data['func']
        await func(call, state=state)


    elif res.split(':')[0] == 'Work':
        await Work.previous()
        data = await state.get_data()
        func = data['func']
        await func(call, state=state)


    elif res.split(':')[0] == 'Client':
        await Client.previous()
        data = await state.get_data()
        func = data['func']
        await func(call, state=state)


    res = await state.get_state()
    if res == None:
        await start_again(call.message)
        return


@deleter
async def start_soc_media(message: types.Message, state: FSMContext):
    """Начало опроса (хочу попасть в ера)"""
    await state.set_state(SocMedia.Name.state)
    await state.update_data(username=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)
    text = '''Ну что ж, приступим к добавлению. Это займет у Вас не более 2-3 минут😉

Как я могу к Вам обращаться?'''
    markup = None
    await message.message.answer(text, reply_markup=markup)

@deleter
async def soc_media_name(message: types.Message, state: FSMContext):
    """Запоминает имя, спрашивает основную соцсеть"""
    if isinstance(message, types.Message):
        await state.update_data(name=message.text)
        if message.text.isdigit():
            await message.answer('<b>Напишите текстом</b>')
            return
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.update_data(func=start_soc_media)
    data = await state.get_data()
    name = data['name']
    text = f'''<u>Вопрос 1 из 6</u>
<b>{name}, какая у Вас основная социальная сеть?</b>'''
    await state.set_state(SocMedia.SM.state)
    markup = await bloger_keyboard()
    await message.answer(text, reply_markup=markup)

@deleter
async def soc_media_sm(call: types.CallbackQuery, state: FSMContext):
    """Запоминает осн.соцсеть, спраш. ссылку на соц.с."""
    await state.update_data(SM=call.data)
    await state.update_data(func=soc_media_name)
    text = '''<b>Скопируйте и вставьте прямую кликабельную ссылку на Вашу основную социальную сеть.</b>'''
    await state.set_state(SocMedia.Link.state)
    markup = await back_keyboard2('Отмена регистрации')
    await call.message.answer(text, reply_markup=markup)

@deleter
async def soc_media_link(message: types.Message, state: FSMContext):
    """Запоминает осн.соцсеть, спраш. подписч"""
    await state.update_data(func=soc_media_sm)
    if is_link(message.text) == True:
        await state.update_data(link=message.text)
        text = '''<u>Вопрос 2 из 6</u>
<b>Количество подписчиков?</b>
<i>(Полным числом, с пробелами, без сокращений, пример: 1 220 000)</i>'''
        await state.set_state(SocMedia.Subs.state)
        markup = await back_keyboard2('Отмена регистрации')
        await message.answer(text, reply_markup=markup)
    else:
        text = '<i>*URL введен некорректно. Пожалуйста, повторите ввод URL еще раз.</i>'
        markup = await back_keyboard2('Отменить регистрацию')
        if isinstance(message, types.CallbackQuery):
            message = message.message
        await message.answer(text, reply_markup=markup)

@deleter
async def soc_media_link2(message: types.Message, state: FSMContext):
    if isinstance(message, types.Message):
        await state.update_data(link=message.text)
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.update_data(func=soc_media_sm)
    text = '''<u>Вопрос 2 из 6</u>
<b>Количество подписчиков?</b>
<i>(Полным числом, с пробелами, без сокращений, пример: 1 220 000)</i>'''
    await state.set_state(SocMedia.Subs.state)
    markup = await back_keyboard2('Отмена регистрации')
    await message.answer(text, reply_markup=markup)

@deleter
async def soc_media_subs(message: types.Message, state: FSMContext):
    """Запоминает subs, спрашивает city"""
    if isinstance(message, types.Message):
        await state.update_data(subs=message.text)
        if not message.text.isdigit():
            await message.answer('<b>Напишите только число, без текста</b>')
            return
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.update_data(func=soc_media_link2)
    text = f'''<u>Вопрос 3 из 6</u>
<b>Город Вашего постоянного проживания?</b>'''
    await state.set_state(SocMedia.City.state)
    markup = await back_keyboard2('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)

@deleter
async def soc_media_city(message: types.Message, state: FSMContext):
    """Запоминает city, спрашивает geo1"""
    if isinstance(message, types.Message):
        await state.update_data(city=message.text)
        if message.text.isdigit():
            await message.answer('<b>Напишите текстом</b>')
            return
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.update_data(func=soc_media_subs)
    text = f'''<u>Вопрос 4 из 6</u>
<b>Основное ГЕО Ваших подписчиков?</b>
<em>(Укажите Страну)</em>'''
    await state.set_state(SocMedia.Geo1.state)
    markup = await back_keyboard2('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)

@deleter
async def soc_media_geo1(message: types.Message, state: FSMContext):
    """Запоминает geo1, спрашивает geo2"""
    if isinstance(message, types.Message):
        await state.update_data(geo1=message.text)
        if message.text.isdigit():
            await message.answer('<b>Напишите текстом</b>')
            return
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.update_data(func=soc_media_city)
    text = f'''<u>Вопрос 4 из 6</u>
<b>Основное ГЕО Ваших подписчиков?</b>
<em>(Укажите город)</em>'''
    await state.set_state(SocMedia.Geo2.state)
    markup = await back_keyboard2('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)

@deleter
async def soc_media_geo2(message: types.Message, state: FSMContext):
    """Запоминает geo2, спрашивает тематику"""
    if isinstance(message, types.CallbackQuery):
        message = message.message
    if message.text.isdigit():
        await message.answer('<b>Напишите текстом</b>')
        return
    await state.update_data(func=soc_media_geo1)
    await state.update_data(geo2=message.text)
    await state.update_data(topic=[])
    text = f'''<u>Вопрос 5 из 6</u>
<b>Укажите тематику Вашего блога?</b>

<i>(Вы можете выбрать несколько тематик, поочередно)</i>'''
    lst = get_config(flag=True)
    await state.set_state(SocMedia.Topic.state)
    markup = await topic_keyboard(lst)
    await message.answer(text, reply_markup=markup)


async def soc_media_topic(call: types.CallbackQuery, state: FSMContext):
    """Обрабатывает выбор тематики"""
    if call.data.split('_')[1] == 'Другое (указать в примечании)':
        text = '<b>Укажите тематику одним сообщением</b>\n\n<i>(Вы можете выбрать несколько тематик, поочередно)</i>'
        await state.set_state(SocMedia.Topic_another.state)
        await call.message.edit_text(text=text)
        return
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(call.data.split('_')[1])
    await state.update_data(topic=lst)
    text = f'''<b>Тематика: {call.data.split('_')[1]} добавлена!
    Желаете выбрать еще тематику?</b>'''
    markup = await topic_keyboard_2()
    await call.message.edit_text(text=text, reply_markup=markup)


async def soc_media_topic_2(call: types.CallbackQuery, state: FSMContext):
    """обрабатывает клавиатуры выбора новой тематики или закончить выбор"""
    if call.data == 'topic_start':
        lst = get_config(flag=True)
        text = '<b>Выберите тематику Вашего контента:</b>'
        markup = await topic_keyboard(lst)
        await call.message.edit_text(text=text, reply_markup=markup)
        return
    elif call.data == 'topic_end':
        lst = await state.get_data()
        name = lst['name']
        lst = lst['topic']
        lst = ', '.join(lst)
        await state.update_data(topic=lst)
        await state.update_data(func=soc_media_geo2)
        markup = await back_keyboard2('Отменить регистрацию')
    text = f'''<em>Вопрос 6 из 6</em>
<b>{name}, кратко опишите о чем Ваш блог, что вы транслируете?</b>

<i>(Не менее 15 слов)</i>'''
    await call.message.edit_text(text=text, reply_markup=markup)
    await state.set_state(SocMedia.Description.state)

@deleter
async def soc_media_topic_another(message: types.Message, state: FSMContext):
    if isinstance(message, types.CallbackQuery):
        message = message.message
    ''' Обрабатывает выбор тематики - другое'''
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(message.text)
    await state.update_data(topic=lst)
    text = f'''<b>Тематика: {message.text} добавлена!
    желаете выбрать еще тематику?</b>'''
    markup = await topic_keyboard_2()
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(SocMedia.Topic.state)

@deleter
async def soc_media_description(message: types.Message, state: FSMContext):
    if isinstance(message, types.CallbackQuery):
        message = message.message
    """Заканчивает процесс регистрации"""
    if message.text.isdigit():
        await message.answer('<b>Напишите текстом</b>')
        return
    if len(message.text.split()) < 15:
        await message.answer('<b>Вы написали меньше 15 слов.\nОпишите о чем Ваш блог <i>(используйте минимум 15 слов)</i></b>')
        return
    await state.update_data(desc=message.text)
    lst = await state.get_data()
    text = '''<b>Вы можете добавить информацию о еще одной социальной сети, или же завершить процесс регистрации</b>'''
    markup = await registr_end()
    await message.answer(text=text, reply_markup=markup)
    await state.finish()
    print(lst)

@deleter
async def soc_media_description2(message: types.Message, state: FSMContext):
    """обработка завершение регистрации"""
    if isinstance(message, types.CallbackQuery):
        message = message.message
    markup = await back_keyboard("В главное меню")
    text = '''✅ Отлично. В ближайшее время с вами свяжутся наши специалисты

Ожидайте ответного сообщения от сотрудника ЕРА в этом боте'''
    await message.answer(text=text, reply_markup=markup)




# MANAGER_NEW
@deleter
async def manager_new_start(call: types.CallbackQuery, state: FSMContext):
    """Начало опроса manager"""
    await state.set_state(Manager_new.Name.state)
    text = '''Ну что ж, приступим к добавлению. Это займет у Вас не более 1 минуты😉

Как я могу к Вам обращаться?'''
    markup = await back_keyboard('Отменить регистрацию')
    await call.message.answer(text, reply_markup=markup)

@deleter
async def manager_new_name(message: types.Message, state: FSMContext):
    """Запись имя, вопрос кол-во блогеров"""
    await state.update_data(func=manager_new_start)
    await state.update_data(username=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)
    if isinstance(message, types.Message):
        await state.update_data(name=message.text)
        if message.text.isdigit():
            await message.answer('<b>Напишите текстом</b>')
            return
    await state.set_state(Manager_new.Count.state)
    data = await state.get_data()
    name = data['name']
    if isinstance(message, types.CallbackQuery):
        message = message.message
    text = f'''<b>{name}, подскажите примерное или точное количество блогеров в Вашей базе?</b>'''
    markup = await back_keyboard2('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)

@deleter
async def manager_new_count(message: types.Message, state: FSMContext):
    """Запись кол-во блогеров, вопрос назв комп"""
    if isinstance(message, types.Message):
        await state.update_data(count=message.text)
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.update_data(func=manager_new_name)
    await state.set_state(Manager_new.Company.state)
    text = '''<b>Укажите название вашей компании ?</b>

<i>Если нет - пропустите вопрос</i>'''
    markup = await pass_keyboard(q='Company')
    await message.answer(text, reply_markup=markup)

@deleter
async def manager_new_company(message: types.Message, state: FSMContext):
    """Запись назв. компании, вопрос сайт комп."""
    await state.update_data(func=manager_new_count)
    if isinstance(message, types.CallbackQuery):
        if message.data != 'back':
            await state.update_data(func=manager_new_count)
            await state.update_data(company='Нет')
            text = '''<b>Укажите ссылку на Ваш сайт</b>\n\n<i>Если нет - пропустите вопрос</i>'''
            markup = await pass_keyboard(q='Site')
            await message.message.answer(text, reply_markup=markup)
            await state.set_state(Manager_new.Link.state)
            return
    else:
        await state.update_data(func=manager_new_count)
        if message.text.isdigit():
            await message.answer('<b>Напишите текстом</b>')
            return
        await state.update_data(company=message.text)
    text = '''<b>Укажите ссылку на Ваш сайт</b>

<i>Если нет - пропустите вопрос</i>'''
    markup = await pass_keyboard(q='Site')
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await message.answer(text, reply_markup=markup)
    await state.set_state(Manager_new.Link.state)

@deleter
async def manager_new_link(message: types.Message, state: FSMContext):
    """Запись сайт компании, вопрос подбор"""
    await state.update_data(func=manager_new_company)
    if isinstance(message, types.CallbackQuery):
        await state.update_data(site='Нет')
        text = '<b>Занимаетесь ли Вы поиском / подбором блогеров под точечный запрос от клиента?</b>'
        markup = await manager_keyboard()
        await message.message.answer(text, reply_markup=markup)
        await state.set_state(Manager_new.Q.state)
        return
    else:
        if is_link(message.text) == True:
            await state.update_data(company=message.text)
            text = ''' <b>Занимаетесь ли Вы поиском / подбором блогеров под точечный запрос от клиента?</b>'''
            markup = await manager_keyboard()
            await state.set_state(Manager_new.Q.state)
        else:
            text = '<i>*URL введен некорректно. Пожалуйста, повторите ввод URL еще раз.</i>'
            markup = await pass_keyboard(q='Site')
    await message.answer(text, reply_markup=markup)

@deleter
async def manager_new_q(call: types.CallbackQuery, state: FSMContext):
    """end manager"""
    if call.data == 'y':
        await state.update_data(q='Да')
    else:
        await state.update_data(q='Нет')
    data = await state.get_data()
    print(data)
    markup = await back_keyboard("В главное меню")
    text = '''✅ Отлично. В ближайшее время с вами свяжутся наши специалисты

Ожидайте ответного сообщения от сотрудника ЕРА в этом боте'''
    await call.message.answer(text=text, reply_markup=markup)


# НАЧАЛО ОПРОСА БАРТЕР
async def start_poll_barter(message: types.Message, state: FSMContext):
    ''' Начало опроса по бартеру, Name '''
    await state.set_state(Barter.Name.state)
    await state.update_data(username=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)
    text = '''Для заполнения анкеты на Бартер следуйте инструкциям:
    \nВпишите свое полное имя.'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)


async def barter_name(message: types.Message, state: FSMContext):
    ''' Запоминает имя, спрашивает номер телефона'''
    await state.update_data(name=message.text)
    text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Barter.Number.state)


async def barter_number(message: types.Message, state: FSMContext):
    ''' Запоминает номер телефона, спрашивает ссылку на соцсеть'''
    if is_number(message.text) == True:
        await state.update_data(number=message.text)
        text = 'пришлите ссылку на свою основную соцсеть'
        markup = await back_keyboard('Отменить регистрацию')
        await message.answer(text, reply_markup=markup)
        await state.set_state(Barter.Link.state)
    else:
        text = 'Вы ввели номер неверного формата. Пожалуйства, следуйте формату +7***-***-**-**. \nВведите номер телефона повторно'
        markup = await back_keyboard('Отменить регистрацию')
        await message.answer(text, reply_markup=markup)


async def barter_link(message: types.Message, state: FSMContext):
    ''' Запоминает ссылку на основную соцсеть и спрашивает количетсво подписчиков'''
    if is_link(message.text) == True:
        await state.update_data(link=message.text)
        text = 'Впишите количество ваших подписчиков'
        markup = await back_keyboard('Отменить регистрацию')
        await message.answer(text, reply_markup=markup)
        await state.set_state(Barter.Subs.state)
    else:
        text = 'К сожалению, Вы прислали ссылку неверного формата. Повторно укажите сылку в формате "https://somesite.ru"'
        markup = await back_keyboard('Отменить регистрацию')
        await message.answer(text, reply_markup=markup)


async def barter_subs(message: types.Message, state: FSMContext):
    ''' Запоминает количество подписчиков и спрашивает из какого города'''
    await state.update_data(subs=message.text)
    text = 'В каком городе Вы проживаете?'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Barter.City.state)


async def barter_city(message: types.Message, state: FSMContext):
    ''' Запоминает город и спрашивает предложение'''
    await state.update_data(city=message.text)
    text = 'Напишите Ваше предложение о сотрудничестве одним сообщением'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Barter.Offer.state)


async def barter_offer(message: types.Message, state: FSMContext):
    ''' Запоминает offer, заканчивает регистрацию'''
    await state.update_data(offer=message.text)
    text = '✅ Благодарим за интерес к сотрудничеству! С вами свяжутся в ближайшее время наши специалисты '
    await message.answer(text=text)
    spreadsheet = client.open_by_key(spreadsheet_era_id)
    sheet = spreadsheet.get_worksheet(1)
    data = await state.get_data()
    sheet.append_row(list(data.values()))
    await state.finish()
    await start_again(message)


# НАЧАЛО ОПРОСА МЕНЕДЖЕР
async def start_poll_manager(message: types.Message, state: FSMContext):
    ''' Начало опроса по бартеру, Number '''
    await state.set_state(Manager.Number.state)
    await state.update_data(username=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)
    text = '''Для заполнения анкеты менеджера блогеров следуйте инструкциям:
    \nНапишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)


async def manager_number(message: types.Message, state: FSMContext):
    ''' Запоминает номер телефона, спрашивает Name'''
    if is_number(message.text) == True:
        await state.update_data(number=message.text)
        text = 'Впишите свое полное имя.'
        markup = await back_keyboard('Отменить регистрацию')
        await message.answer(text, reply_markup=markup)
        await state.set_state(Manager.Name.state)
    else:
        await number_wrong(message)


async def manager_name(message: types.Message, state: FSMContext):
    ''' Запоминает имя, спрашивает ссылку на список блогеров'''
    await state.update_data(name=message.text)
    text = 'Ссылка на список Ваших блогеров'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Manager.Link.state)


async def manager_link(message: types.Message, state: FSMContext):
    ''' Запоминает ссылку на список блогеров и справшивает exclusive'''
    if is_link(message.text) == True:
        await state.update_data(link=message.text)
        text = 'Есть ли блогеры у Вас на эксклюзивном сотрудничестве и/или те у кого Вы непосредственно PR.'
        markup = await reels_keyboard('M')
        await message.answer(text=text, reply_markup=markup)
        await state.set_state(Manager.Exclusive.state)
    else:
        await number_wrong(message, number=False)


async def manager_exclusive(message: types.Message, state: FSMContext):
    ''' Запоминает exclusive, - if else'''
    data = message.data
    data = data.split('_')
    if data[1] == "yes":
        text = "Пришлите ссылки на этих блогеров одним сообщением"
        await state.set_state(Manager.Exclusive_links.state)
    if data[1] == "no":
        await state.update_data(exclusive="Нет")
        text = 'Помимо предоставления своих блогеров для рекламных интеграций, заинтересованы ли вы также в подборе блогеров под конкретный рекламный запрос?'
        await state.set_state(Manager.Q.state)
    markup = await back_keyboard('Отменить регистрацию')
    await message.message.answer(text, reply_markup=markup)


async def manager_exclusive_links(message: types.Message, state: FSMContext):
    ''' Запоминает exclusive_links задает последний вопрос'''
    data = '  ___  '.join(message.text.split())
    await message.answer(data)

    await state.update_data(exclusive=data)
    text = 'Помимо предоставления своих блогеров для рекламных интеграций, заинтересованы ли вы также в подборе блогеров под конкретный рекламный запрос?'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Manager.Q.state)


async def manager_q(message: types.Message, state: FSMContext):
    ''' Запоминает вопрос, заканчивает регистрацию'''
    await state.update_data(q=message.text)
    text = '✅ Благодарим за интерес к сотрудничеству! С вами свяжутся в ближайшее время наши специалисты '
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
    spreadsheet = client.open_by_key(spreadsheet_era_id)
    sheet = spreadsheet.get_worksheet(2)
    data = await state.get_data()
    sheet.append_row(list(data.values()))
    await state.finish()
    await start_again(message)


# НАЧАЛО ОПРОСА СОТРУДНИЧЕСТВО
@deleter
async def start_poll_col(message: types.Message, state: FSMContext):
    ''' Начало опроса по сотрудничеству, Name '''
    await state.set_state(Colab.Name.state)
    await state.update_data(username=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)
    text = '''Для оставления заявки на сотрудничество ответьте на несколько вопросов.

Это займет у Вас не более 2-3 минут😉

Как я могу к Вам обращаться?'''
    markup = None
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)

@deleter
async def colab_name(message: types.Message, state: FSMContext):
    ''' Запоминает name и спрашивает post'''
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.update_data(func=start_poll_col)
    await state.update_data(name=message.text)
    text = '''<u>Вопрос 1 из 3</u> 

<b>Название Вашей компании</b>'''
    markup = await pass_keyboard(q="Colab")
    await message.answer(text, reply_markup=markup)
    await state.set_state(Colab.Company.state)

@deleter
async def colab_company(message: types.Message, state: FSMContext):
    ''' Запоминает company и спрашивает reason'''
    await state.update_data(func=colab_name)
    text = '''<u>Вопрос 2 из 3</u> 

<b>Ваша должность</b>'''
    markup = await pass_keyboard(q="Colab")
    await state.set_state(Colab.Post.state)
    if isinstance(message, types.CallbackQuery):
        await state.update_data(company='Нет')
        await message.message.answer(text, reply_markup=markup)
        return
    else:
        await state.update_data(company=message.text)
        await message.answer(text, reply_markup=markup)

    
@deleter
async def colab_post(message: types.Message, state: FSMContext):
    ''' Запоминает post и спрашивает reason'''
    await state.update_data(func=colab_company)
    text = '''<u>Вопрос 3 из 3</u> 

<b>Причина Вашего обращения</b>

<i>(Опишите суть вашего обращения / Ваш запрос)</i>'''
    markup = await back_keyboard2('Отменить регистрацию')
    await state.set_state(Colab.Reason.state)
    if isinstance(message, types.CallbackQuery):
        await state.update_data(post='Нет')
        await message.message.answer(text, reply_markup=markup)
        return
    else:
        await state.update_data(post=message.text)
    await message.answer(text, reply_markup=markup)

@deleter
async def colab_reason(message: types.Message, state: FSMContext):
    ''' Запоминает reason и завершает опрос'''
    await state.update_data(reason=message.text)
    text = '''✅ Благодарю, Вы оставили вашу заявку на сотрудничество.

Ожидайте ответного сообщения от сотрудника ЕРА в этом боте'''
    lst = await state.get_data()
    await message.answer(text)
    print(lst)
    await state.finish()
    await start_again(message)


# НАЧАЛО ОПРОСА ЭКСКЛЮЗИВНЫЙ КОНТРАКТ
@deleter
async def start_ExcConract(call: types.CallbackQuery, state: FSMContext):
    text = '''Сейчас я перенаправлю тебя на руководителя отдела инфлюенс-маркетинга. Отправь ему сообщение по этой форме:

1) Ссылки на все социальные сети с количеством подписчиков в каждой из них

Пример:
Telegram (354 тыс)- ссылка
VK (223 тыс) - ссылка 
Instagram (15 тыс) - ссылка 

2) Скрины статистика по каждой из них 

3) Краткая информация о себе

Контакт:
https://t.me/ByAlexeev''' 
    markup = await back_keyboard("Назад")
    await call.message.answer(text, reply_markup=markup)


# НАЧАЛО ОПРОСА ЭКСКЛЮЗИВНЫЙ КОНТРАКТ
@deleter
async def start_Work(call: types.CallbackQuery, state: FSMContext):
    with open('work.txt', encoding='utf-8') as f:
        text = f.read() 
    markup = await work_keyboard()
    await call.message.answer(text, reply_markup=markup, disable_web_page_preview=True)


@deleter
async def work_profile_start(call: types.CallbackQuery, state: FSMContext):
    """Спрашивает имя"""
    await state.set_state(Work.Name.state)
    await state.update_data(func=start_Work)
    if call.data == 'work_profile':
        await state.update_data(username=call.from_user.username)
        await state.update_data(user_id=call.from_user.id)
    text = """Ну что-ж, приступим к анкетированию. Это займет у Вас не более 2-3 минут😉\n
Как я могу к Вам обращаться?"""
    markup = None
    await call.message.answer(text, reply_markup=markup)



@deleter
async def work_name(message: types.Message, state: FSMContext):
    "Запоминает имя, спрашивает должность"
    if isinstance(message, types.CallbackQuery):
        message = message.message
    else:
        await state.update_data(name=message.text)
    await state.update_data(func=work_profile_start)
    text = """<u>Вопрос 1 из 8</u>\n
<b>Напишите желаемую должность в компании</b>"""
    markup = await back_keyboard2('Отменить регистрацию') 
    await state.set_state(Work.Post.state)
    await message.answer(text, reply_markup=markup)



@deleter
async def work_post(message: types.Message, state: FSMContext):
    "Запоминает должность, спрашивает опыт"
    if isinstance(message, types.CallbackQuery):
        message = message.message
    else:
        await state.update_data(post=message.text)
    await state.update_data(func=work_name)
    text = """<u>Вопрос 2 из 8</u>\n
<b>Если ли у вас опыт в этой должности, если есть, то какой он?</b>"""
    markup = await back_keyboard2('Отменить регистрацию') 
    await state.set_state(Work.Exp.state)
    await message.answer(text, reply_markup=markup)


@deleter
async def work_exp(message: types.Message, state: FSMContext):
    "Запоминает exp, спрашивает skills"
    if isinstance(message, types.CallbackQuery):
        message = message.message
    else:
        await state.update_data(exp=message.text)
    await state.update_data(func=work_post)
    text = """<u>Вопрос 3 из 8</u>\n
<b>Ваши главные Hard и Soft skills</b>"""
    markup = await back_keyboard2('Отменить регистрацию') 
    await state.set_state(Work.Skills.state)
    await message.answer(text, reply_markup=markup)


@deleter
async def work_skills(message: types.Message, state: FSMContext):
    "Запоминает skills, спрашивает REASON"
    if isinstance(message, types.CallbackQuery):
        message = message.message
    else:
        await state.update_data(skills=message.text)
    await state.update_data(func=work_exp)
    text = """<u>Вопрос 4 из 8</u>\n
<b>Почему Вы хотите трудоустроится в ЕРА?</b>"""
    markup = await back_keyboard2('Отменить регистрацию') 
    await state.set_state(Work.Reason.state)
    await message.answer(text, reply_markup=markup)


@deleter
async def work_reason(message: types.Message, state: FSMContext):
    "Запоминает reason, спрашивает age"
    if isinstance(message, types.CallbackQuery):
        message = message.message    
    else:
        await state.update_data(reason=message.text)
    await state.update_data(func=work_skills)
    text = """<u>Вопрос 5 из 8</u>\n
<b>Напишите свой возраст</b>"""
    markup = await back_keyboard2('Отменить регистрацию') 
    await state.set_state(Work.Age.state)
    await message.answer(text, reply_markup=markup)


@deleter
async def work_age(message: types.Message, state: FSMContext):
    "Запоминает age, спрашивает load"
    if isinstance(message, types.CallbackQuery):
        message = message.message
    else:
        await state.update_data(age=message.text)
    await state.update_data(func=work_reason)
    text = """<u>Вопрос 6 из 8</u>\n
<b>Текущая степень загруженности (учеба, другая работа, разница во времени с МСК)</b>"""
    markup = await back_keyboard2('Отменить регистрацию') 
    await state.set_state(Work.Load.state)
    await message.answer(text, reply_markup=markup)


@deleter
async def work_load(message: types.Message, state: FSMContext):
    "Запоминает load, спрашивает resume"
    if isinstance(message, types.CallbackQuery):
        message = message.message
    else:
        await state.update_data(load=message.text)
    await state.update_data(func=work_age)
    text = """<u>Вопрос 7 из 8</u>\n
<b>Пришлите ссылку на Ваше резюме:</b>"""
    markup = await pass_keyboard('Нет резюме', a=True) 
    await state.set_state(Work.Link_resume.state)
    await message.answer(text, reply_markup=markup)


@deleter
async def work_linkResume(message: types.Message, state: FSMContext):
    "Запоминает resume, спрашивает case"
    await state.update_data(func=work_load)
    text = """<u>Вопрос 8 из 8</u>\n
<b>Пришлите ссылку на Ваши кейсы:</b>"""
    if isinstance(message, types.CallbackQuery):
        message = message.message
        await state.update_data(resume="нет резюме")
        await state.set_state(Work.Link_case.state)
        markup = await pass_keyboard('Нет кейсов', a=True) 
        await message.answer(text, reply_markup=markup)
        return
    if is_link(message.text) == True:
        await state.update_data(resume=message.text)
    else:
        await number_wrong(message, number=False)
        return
    markup = await pass_keyboard('Нет резюме', a=True) 
    await state.set_state(Work.Link_case.state)
    await message.answer(text, reply_markup=markup)


@deleter
async def work_linkCase(message: types.Message, state: FSMContext):
    "Запоминает case, завершает регистрацию"
    await state.update_data(func=work_linkResume)
    text = """Благодарю, Вы прошли анкетирование. \n\nОжидайте ответного сообщения от сотрудника ЕРА в этом боте"""
    if isinstance(message, types.CallbackQuery):
        message = message.message
        await state.update_data(case="нет кейсов")
    elif is_link(message.text) == True:
        await state.update_data(case=message.text)
    else:
        await number_wrong(message, number=False)
        return
    lst = await state.get_data()
    print(lst)
    await message.answer(text)
    await state.finish()
    await start_again(message)


@deleter
async def work_write(message: types.Message, state: FSMContext):
    text = 'Введите пароль для изменения текcта вакансий '
    await state.set_state(Work_write.Pass.state)
    await message.answer(text)


async def work_pass(message: types.Message, state: FSMContext):
    if message.text != 'era123123':
        await start(message)
        await state.finish()
        return
    await state.set_state(Work_write.Text.state)
    text = 'СТАРЫЙ ТЕКСТ: \n\n\n'
    with open('work.txt', encoding='utf-8') as f:
        text += f.read() 
    text += '\n\n\n Теперь введите новый текст для этого раздела'
    await state.set_state(Work_write.Text.state)
    await message.answer(text, disable_web_page_preview=True)

@deleter
async def work_text(message: types.Message, state: FSMContext):
    text = message.text
    with open('work.txt', mode='w', encoding='utf-8') as f:
        f.write(text)
    with open('work.txt', encoding='utf-8') as f:
        text = 'НОВЫЙ ТЕКСТ: \n\n\n' + f.read() 
    await message.answer(text, disable_web_page_preview=True)
    await sleep(4)
    await state.finish()
    await start(message)


# НАЧАЛО ОПРОСА КЛИЕНТАМ
@deleter
async def clients_start(call: types.CallbackQuery, state: FSMContext):
    "нааинает опрос по клиентам"
    await state.set_state(Client.Name.state)
    await state.update_data(username=call.from_user.username)
    await state.update_data(user_id=call.from_user.id)
    text = """Оставьте свою заявку. С Вами свяжется спеиалист ЕРА в течение часа после ее заполнения."""
    markup = await client_keyboard()
    await call.message.answer(text, reply_markup=markup)


@deleter
async def clients_name(message: types.Message, state: FSMContext):
    "спрашивает имя"
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.update_data(func=clients_start)
    text = """Отлично, как я могу к Вам обращаться?"""
    markup = None 
    await state.set_state(Client.Company.state)
    await message.answer(text, reply_markup=markup)


@deleter
async def clients_company(message: types.Message, state: FSMContext):
    "спрашивает компанию"
    if isinstance(message, types.CallbackQuery):
        message = message.message
    await state.update_data(func=clients_name)
    text = """<u>Вопрос 1 из 5</u>\n
<b>Название Вашей компании</b>"""
    markup = await pass_keyboard('Пропустить вопрос', a=True) 
    await state.set_state(Client.Post.state)
    await message.answer(text, reply_markup=markup)


@deleter
async def clients_post(message: types.Message, state: FSMContext):
    "запоминает company, спрашивает post"
    await state.update_data(func=clients_company)
    if isinstance(message, types.CallbackQuery):
        await state.update_data(company='нет')
        message = message.message
    else:
        await state.update_data(company=message.text)
    text = """<u>Вопрос 2 из 5</u>\n
<b>Ваша должность</b>"""
    markup = await pass_keyboard('Пропустить вопрос', a=True) 
    await state.set_state(Client.Site.state)
    await message.answer(text, reply_markup=markup)


@deleter
async def clients_site(message: types.Message, state: FSMContext):
    "запоминает post, спрашивает site"
    await state.update_data(func=clients_post)
    if isinstance(message, types.CallbackQuery):
        await state.update_data(post='нет')
        message = message.message
    else:
        await state.update_data(post=message.text)
    text = """<u>Вопрос 3 из 5</u>\n
<b>Ссылки на сайт или другой ресурс</b>"""
    markup = await pass_keyboard('Пропустить вопрос', a=True) 
    await state.set_state(Client.Reason.state)
    await message.answer(text, reply_markup=markup)


@deleter
async def clients_reason(message: types.Message, state: FSMContext):
    "запоминает site, спрашивает reason"
    await state.update_data(func=clients_site)
    if isinstance(message, types.CallbackQuery):
        await state.update_data(post='нет')
        message = message.message
    elif is_link(message.text) == True:
        await state.update_data(site=message.text)
    else:
        await number_wrong(message, number=False)
        return
    text = """<u>Вопрос 4 из 5</u>\n
<b>Причина Вашего обращения</b>\n
<i>(Опишите суть Вашего обращения / Ваш запрос)</i>"""
    markup = await back_keyboard2('Отменить регистрацию') 
    await state.set_state(Client.Type.state)
    await message.answer(text, reply_markup=markup)


@deleter
async def clients_type(message: types.Message, state: FSMContext):
    "спрашивает компанию"
    await state.update_data(func=clients_reason)
    await state.update_data(reason=message.text)
    text = """<u>Вопрос 5 из 5</u>\n
<b>Тип желаемого сотрудничества</b>"""
    markup = await client_TypeColab_keyboard() 
    await state.set_state(Client.End.state)
    await message.answer(text, reply_markup=markup)


@deleter
async def clients_end(call: types.CallbackQuery, state: FSMContext):
    "запоминает typeColab, заканчивает регистрацию"
    if isinstance(call, types.Message):
        text = "Выберите тип сотрудничества, нажав на кнопку"
        await call.answer(text)
        return
    await state.update_data(type=call.data)
    text = """Благодарю, Вы оставили заявку на сотрудничество.\n
Ожидайте ответного сообщения от сотрудника ЕРА в этом боте в течение часа.\n
Также просим изучить условия работы нашего Агенства ЕРА:\n
Условия:
https://bloggers.era-agency.ru"""
    markup = await back_keyboard('в меню') 
    lst = await state.get_data()
    print(lst)
    await state.finish()
    await call.message.answer(text, reply_markup=markup, disable_web_page_preview=True)

"""TODO: testing clients and work"""


# НАЧАЛО ОПРОСА БЛОГЕР
async def start_poll_bloger(message: types.Message, state: FSMContext):
    ''' Выбераем соцсеть для регистрации '''
    text = '''Выберите социальную сеть со своим блогом
    (после заполенения информации об одном, можно будет добавить другие социальные сети)'''
    markup = await bloger_keyboard()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


# НАЧАЛО ОПРОСА INSTAGRM
async def start_poll_inst(message: types.Message, state: FSMContext, flag=None):
    ''' Начало опроса блогера инста, Number '''
    await state.set_state(Instagram.Number.state)
    await state.update_data(username=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)
    if Bloger(str(message.from_user.id)).check():
        num = Bloger(str(message.from_user.id)).get()
        text = f'Использовать номер {num}?'
        markup = await number_keyboard()
        await state.set_state(Instagram.Wait.state)
    else:
        # Запросить номер
        text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = await back_keyboard('Отменить регистрацию')
    if flag:
        text = 'Напишите свой новый номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = types.ReplyKeyboardRemove()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


async def inst_number(call: types.CallbackQuery, state: FSMContext):
    ''' Запоминает number и спрашивает Link'''
    if (call.data if type(call) is types.CallbackQuery else call.text) == 'number_y':
        await state.update_data(number=Bloger(f"{call.from_user.id}").get())
        text = 'Отправьте ссылку на Ваш Instagram'
    elif (call.data if type(call) is types.CallbackQuery else call.text) == 'number_n':
        await start_poll_inst(call, state, flag=True)
    else:
        if is_number(call.text) == True:
            await state.update_data(number=call.text)
            Bloger(f"{call.from_user.id}").record(call.text)
        else:
            await number_wrong(call)
            return
    text = 'Отправьте ссылку на Ваш Instagram'
    markup = await back_keyboard('Отменить регистрацию')
    await call.answer(text, reply_markup=markup)
    await state.set_state(Instagram.Link.state)


async def inst_number_wait(message: types.Message, state: FSMContext):
    if message.text == "Да✅":
        await state.update_data(number=Bloger(f"{message.from_user.id}").get())
        text = 'Отправьте ссылку на Ваш Instagram'
    else:
        await start_poll_inst(message, state, flag=True)
        await state.set_state(Instagram.Number.state)
        return
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Instagram.Link.state)


async def inst_link(message: types.Message, state: FSMContext):
    ''' Запоминает ссылку на инст и спрашивает тематику'''
    if is_link(message.text) == True:
        await state.update_data(link=message.text)
        await state.update_data(topic=[])
        lst = get_config(flag=True)
        text = 'Выберите тематику Вашего контента:'
        markup = await topic_keyboard(lst)
        await message.answer(text=text, reply_markup=markup)
        await state.set_state(Instagram.Topic.state)
    else:
        await number_wrong(message, number=False,
                           text2='К сожалению, Вы прислали ссылку неверного формата. Повторно укажите сылку в формате "https://somesite.ru"')


async def inst_topic_choose(message: types.Message, state: FSMContext):
    ''' Обрабатывает выбор тематики '''
    if message.data.split('_')[1] == 'Другое (указать в примечании)':
        text = 'Укажите тематику одним сообщением'
        await state.set_state(Instagram.Topic_another.state)
        await message.message.edit_text(text=text)
        return
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(message.data.split('_')[1])
    await state.update_data(topic=lst)
    text = f'''Тематика: {message.data.split('_')[1]} добавлена!
Желаете выбрать еще тематику?'''
    markup = await topic_keyboard_2()
    await message.message.edit_text(text=text, reply_markup=markup)


async def inst_topic_another(message: types.Message, state: FSMContext):
    ''' Обрабатывает выбор тематики - другое'''
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(message.text)
    await state.update_data(topic=lst)
    text = f'''Тематика: {message.text} добавлена!
    желаете выбрать еще тематику?'''
    markup = await topic_keyboard_2()
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(Instagram.Topic.state)


async def inst_topic_choose_2(message: types.Message, state: FSMContext):
    ''' обрабатывает клавиатуры выбора новой тематики ил закончить выбор '''
    if message.data == 'topic_start':
        lst = get_config(flag=True)
        text = 'Выберите тематику Вашего контента:'
        markup = await topic_keyboard(lst)
        await message.message.edit_text(text=text, reply_markup=markup)
        return
    elif message.data == 'topic_end':
        lst = await state.get_data()
        lst = lst['topic']
        lst = ', '.join(lst)
        await state.update_data(topic=lst)
        markup = await back_keyboard('Отменить регистрацию')
    text = f'''Введите количество Ваших подписчиков'''
    await message.message.edit_text(text=text, reply_markup=markup)
    await state.set_state(Instagram.Subs.state)


async def inst_subs(message: types.Message, state: FSMContext):
    ''' Запоминает количество подписчиков и спрашивает опсиание блога'''
    await state.update_data(subs=message.text)
    text = 'Краткое описание блога \n*Опишите, что Вы транслируете в блоге'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Instagram.Description.state)


async def inst_descroption(message: types.Message, state: FSMContext):
    ''' Запоминает описание и спрашивает город'''
    await state.update_data(description=message.text)
    text = 'Ваш город?'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Instagram.City.state)


async def inst_city(message: types.Message, state: FSMContext):
    ''' Запоминает город и спрашивает цену сторис'''
    await state.update_data(city=message.text)
    text = '''Средняя стоимость серии сторис (3-4шт) 
*Мы понимаем, что стоимость будет варьироваться в зависимости от запроса, поэтому просим указать именно среднюю стоимость.'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Instagram.Stories.state)


async def inst_stories(message: types.Message, state: FSMContext):
    ''' Запоминает цену сторис и спрашивает охват сторис'''
    await state.update_data(stories=message.text)
    text = '''Укажите средние охваты сторис за последнюю неделю'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Instagram.Stories_scope.state)


async def inst_stories_scope(message: types.Message, state: FSMContext):
    ''' Запоминает охват сторис и спрашивает цену рилс'''
    await state.update_data(stories_scope=message.text)
    text = '''Средняя стоимость рилс в профиле'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Instagram.Reels.state)


async def inst_reels(message: types.Message, state: FSMContext):
    ''' Запоминает цену рилс и спрашивает охват рилс'''
    await state.update_data(reels=message.text)
    text = '''Укажите средние охваты Рилс за последнюю неделю'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(Instagram.Reels_scope.state)


async def inst_reels_scope(message: types.Message, state: FSMContext):
    ''' Запоминает охват рилс и спрашивает статистку'''
    await state.update_data(reels_scope=message.text)
    text = '''Ссылка на статистику 
*Ссылка на любой удобный для Вас диск, содержащий охваты просмотров сторис, постов/рилс за последнюю неделю. Статистику аудитории по гендеру, возрасту, географии. '''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(Instagram.Statistic.state)


async def inst_statistic(message: types.Message, state: FSMContext):
    ''' Запоминает статистику, заканчивает регистрацию'''
    if is_link(message.text) == True:
        await state.update_data(statistic=message.text)
        text = '✅ Благодарим за интерес к сотрудничеству! С вами свяжутся в ближайшее время наши специалисты '
        await message.answer(text=text)
        spreadsheet = client.open_by_key(spreadsheet_bloger_id)
        sheet = spreadsheet.get_worksheet(0)
        num = len(sheet.col_values(1)) + 1
        data = await state.get_data()
        data = list(data.values())
        cell_list = sheet.range(f'A{num}:AQ{num}')
        cell_index = [0, 1, 2, 3, 4, 5, 10, 11, 18, 19, 27, 28, 33]
        for i, val in enumerate(cell_index):
            cell_list[val].value = data[i]
        cell_list.pop(9)
        sheet.update_cells(cell_list)
        await state.finish()
        await start_again(message)
    else:
        await number_wrong(message, number=False)


# НАЧАЛО ОПРОСА YOUTUBE
async def start_poll_yt(message: types.Message, state: FSMContext, flag=None):
    ''' Начало опроса блогера инста, Number '''
    await state.set_state(YT.Number.state)
    await state.update_data(username=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)
    if Bloger(str(message.from_user.id)).check():
        num = Bloger(str(message.from_user.id)).get()
        text = f'Использовать номер {num}?'
        markup = await number_keyboard()
        await state.set_state(YT.Wait.state)
    else:
        # Запросить номер
        text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = await back_keyboard('Отменить регистрацию')
    if flag:
        text = 'Напишите свой новый номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = types.ReplyKeyboardRemove()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


async def yt_number(call: types.CallbackQuery, state: FSMContext):
    ''' Запоминает number и спрашивает Link'''
    if (call.data if type(call) is types.CallbackQuery else call.text) == 'number_y':
        await state.update_data(number=Bloger(f"{call.from_user.id}").get())
        text = 'Ссылка на YouTube канал \n*В формате https://www.youtube.com/channel'
    elif (call.data if type(call) is types.CallbackQuery else call.text) == 'number_n':
        await start_poll_yt(call, state, flag=True)
    else:
        if is_number((call.data if type(call) is types.CallbackQuery else call.text)) == True:
            await state.update_data(number=call.text)
            Bloger(f"{call.from_user.id}").record(call.text)
        else:
            await number_wrong(call)
            return
    text = 'Ссылка на YouTube канал \n*В формате https://www.youtube.com/channel'
    markup = await back_keyboard('Отменить регистрацию')
    await call.answer(text=text, reply_markup=markup)
    await state.set_state(YT.Link.state)


async def yt_number_wait(message: types.Message, state: FSMContext):
    if message.text == "Да✅":
        await state.update_data(number=Bloger(f"{message.from_user.id}").get())
        text = 'Ссылка на YouTube канал \n*В формате https://www.youtube.com/channel'
    else:
        await start_poll_yt(message, state, flag=True)
        await state.set_state(YT.Number.state)
        return
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(YT.Link.state)


async def yt_link(message: types.Message, state: FSMContext):
    ''' Запоминает ссылку на yt и спрашивает тематику'''
    if is_link(message.text) == True:
        await state.update_data(link=message.text)
        await state.update_data(topic=[])
        lst = get_config(flag=True)
        text = 'Выберите тематики, подходящие под ваш блог:'
        markup = await topic_keyboard(lst)
        await message.answer(text=text, reply_markup=markup)
        await state.set_state(YT.Topic.state)
    else:
        await number_wrong(message, number=False)


async def yt_topic_choose(message: types.Message, state: FSMContext):
    ''' Обрабатывает выбор тематики yt'''
    if message.data.split('_')[1] == 'Другое (указать в примечании)':
        text = 'Укажите тематику одним сообщением'
        await state.set_state(YT.Topic_another.state)
        await message.message.edit_text(text=text)
        return
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(message.data.split('_')[1])
    await state.update_data(topic=lst)
    text = f'''Тематика: {message.data.split('_')[1]} добавлена!
Желаете выбрать еще тематику?'''
    markup = await topic_keyboard_2()
    await message.message.edit_text(text=text, reply_markup=markup)


async def yt_topic_another(message: types.Message, state: FSMContext):
    ''' Обрабатывает выбор тематики - другое'''
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(message.text)
    await state.update_data(topic=lst)
    text = f'''Тематика: {message.text} добавлена!
Желаете выбрать еще тематику?'''
    markup = await topic_keyboard_2()
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(YT.Topic.state)


async def yt_topic_choose_2(message: types.Message, state: FSMContext):
    ''' обрабатывает клавиатуры выбора новой тематики ил закончить выбор '''
    if message.data == 'topic_start':
        lst = get_config(flag=True)
        text = 'Выберите тематику Вашего контента:'
        markup = await topic_keyboard(lst)
        await message.message.edit_text(text=text, reply_markup=markup)
        return
    elif message.data == 'topic_end':
        lst = await state.get_data()
        lst = lst['topic']
        lst = ', '.join(lst)
        await state.update_data(topic=lst)
        markup = await back_keyboard('Отменить регистрацию')
    text = f'''Введите количество Ваших подписчиков'''
    await message.message.edit_text(text=text, reply_markup=markup)
    await state.set_state(YT.Subs.state)


async def yt_subs(message: types.Message, state: FSMContext):
    ''' Запоминает количество подписчиков и спрашивает опсиание блога'''
    await state.update_data(subs=message.text)
    text = 'Краткое описание блога \n*Опишите, что Вы транслируете в блоге'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(YT.Description.state)


async def yt_descroption(message: types.Message, state: FSMContext):
    ''' Запоминает описание и спрашивает country'''
    await state.update_data(description=message.text)
    text = 'Укажите Вашу страну'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(YT.Country.state)


async def yt_country(message: types.Message, state: FSMContext):
    ''' Запоминает country и спрашивает цену shorts'''
    await state.update_data(city=message.text)
    text = '''Размещаете ли Вы контент в формате Shorts?'''
    markup = await reels_keyboard('YT')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(YT.Question_shotrs.state)


async def yt_questions_shorts(message: types.Message, state: FSMContext):
    ''' Запоминает questions_shorts и pass'''
    data = message.data.split("_")
    if data[1] == 'yes':
        text = "Укажите стоимость размещения Shorts"
        await state.set_state(YT.Shorts.state)
    if data[1] == 'no':
        await state.update_data(stories="не размещает")
        await state.update_data(stories_scope="не размещает")
        text = '''Стоимость размещения интеграции
*Мы понимаем, что стоимость будет варьироваться в зависимости от запроса, поэтому просим указать среднюю стоимость.'''
        await state.set_state(YT.Video.state)

    markup = await back_keyboard('Отменить регистрацию')
    await message.message.answer(text=text, reply_markup=markup)


async def yt_shorts(message: types.Message, state: FSMContext):
    ''' Запоминает цену shorts и спрашивает охват shorts'''
    await state.update_data(stories=message.text)
    text = '''Укажите средние просмотры Shorts'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(YT.Shorts_views.state)


async def yt_shorts_views(message: types.Message, state: FSMContext):
    ''' Запоминает охват shorts и спрашивает цену интеграции'''
    await state.update_data(stories_scope=message.text)
    text = '''Стоимость размещения интеграции
*Мы понимаем, что стоимость будет варьироваться в зависимости от запроса, поэтому просим указать среднюю стоимость.'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(YT.Video.state)


async def yt_video(message: types.Message, state: FSMContext):
    ''' Запоминает цену интеграции и спрашивает охват видео'''
    await state.update_data(reels=message.text)
    text = '''Укажите средние просмотры горизонтальных видео'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(YT.Video_views.state)


async def yt_video_views(message: types.Message, state: FSMContext):
    ''' Запоминает охват video и спрашивает статистку'''
    await state.update_data(reels_scope=message.text)
    text = '''Ссылка на статистику 
*Ссылка на любой удобный для Вас диск, содержащий статистику аудитории по гендеру, возрасту, географии. '''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(YT.Statistic.state)


async def yt_statistic(message: types.Message, state: FSMContext):
    ''' Запоминает статистику, заканчивает регистрацию'''
    if is_link(message.text) == True:
        await state.update_data(statistic=message.text)
        text = '✅ Благодарим за интерес к сотрудничеству! С вами свяжутся в ближайшее время наши специалисты '
        await message.answer(text=text)
        spreadsheet = client.open_by_key(spreadsheet_bloger_id)
        sheet = spreadsheet.get_worksheet(1)
        num = len(sheet.col_values(1)) + 1
        data = await state.get_data()
        data = list(data.values())
        cell_list = sheet.range(f'A{num}:AQ{num}')
        cell_index = [0, 1, 2, 3, 4, 5, 10, 12, 16, 17, 22, 23, 31]
        for i, val in enumerate(cell_index):
            cell_list[val].value = data[i]
        cell_list.pop(41)
        cell_list.pop(34)
        cell_list.pop(11)
        cell_list.pop(9)
        sheet.update_cells(cell_list)
        await state.finish()
        await start_again(message)
    else:
        await number_wrong(message, number=False)


# НАЧАЛО ОПРОСА VK
async def start_poll_vk(message: types.Message, state: FSMContext, flag=None):
    ''' Начало опроса блогера vk, Number '''
    await state.set_state(VK.Number.state)
    await state.update_data(username=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)
    if Bloger(str(message.from_user.id)).check():
        num = Bloger(str(message.from_user.id)).get()
        text = f'Использовать номер {num}?'
        markup = await number_keyboard()
        await state.set_state(VK.Wait.state)
    else:
        # Запросить номер
        text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = await back_keyboard('Отменить регистрацию')
    if flag:
        text = 'Напишите свой новый номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = types.ReplyKeyboardRemove()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


async def vk_number(call: types.CallbackQuery, state: FSMContext):
    ''' Запоминает number и спрашивает Link'''
    if (call.data if type(call) is types.CallbackQuery else call.text) == 'number_y':
        await state.update_data(number=Bloger(f"{call.from_user.id}").get())
        text = 'Ссылка на страницу Вконтакте'
    elif (call.data if type(call) is types.CallbackQuery else call.text) == 'number_n':
        await start_poll_vk(call, state, flag=True)
    else:
        if is_number((call.data if type(call) is types.CallbackQuery else call.text)) == True:
            await state.update_data(number=call.text)
            Bloger(f"{call.from_user.id}").record(call.text)
        else:
            await number_wrong(call)
            return
    text = 'Ссылка на страницу Вконтакте'
    markup = await back_keyboard('Отменить регистрацию')
    await call.answer(text=text, reply_markup=markup)
    await state.set_state(VK.Link.state)


async def vk_number_wait(message: types.Message, state: FSMContext):
    if message.text == "Да✅":
        await state.update_data(number=Bloger(f"{message.from_user.id}").get())
        text = 'Ссылка на страницу Вконтакте'
    else:
        await start_poll_vk(message, state, flag=True)
        await state.set_state(VK.Number.state)
        return
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(VK.Link.state)


async def vk_link(message: types.Message, state: FSMContext):
    ''' Запоминает ссылку на vk и спрашивает тематику'''
    if is_link(message.text) == True:
        await state.update_data(link=message.text)
        await state.update_data(topic=[])
        lst = get_config(flag=True)
        text = 'Выберите тематики, подходящие под ваш блог:'
        markup = await topic_keyboard(lst)
        await message.answer(text=text, reply_markup=markup)
        await state.set_state(VK.Topic.state)
    else:
        await number_wrong(message, number=False)


async def vk_topic_choose(message: types.Message, state: FSMContext):
    ''' Обрабатывает выбор тематики vk'''
    if message.data.split('_')[1] == 'Другое (указать в примечании)':
        text = 'Укажите тематику одним сообщением'
        await state.set_state(VK.Topic_another.state)
        await message.message.edit_text(text=text)
        return
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(message.data.split('_')[1])
    await state.update_data(topic=lst)
    text = f'''Тематика: {message.data.split('_')[1]} добавлена!
Желаете выбрать еще тематику?'''
    markup = await topic_keyboard_2()
    await message.message.edit_text(text=text, reply_markup=markup)


async def vk_topic_another(message: types.Message, state: FSMContext):
    ''' Обрабатывает выбор тематики - другое'''
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(message.text)
    await state.update_data(topic=lst)
    text = f'''Тематика: {message.text} добавлена!
Желаете выбрать еще тематику?'''
    markup = await topic_keyboard_2()
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(VK.Topic.state)


async def vk_topic_choose_2(message: types.Message, state: FSMContext):
    ''' обрабатывает клавиатуры выбора новой тематики ил закончить выбор '''
    if message.data == 'topic_start':
        lst = get_config(flag=True)
        text = 'Выберите тематику Вашего контента:'
        markup = await topic_keyboard(lst)
        await message.message.edit_text(text=text, reply_markup=markup)
        return
    elif message.data == 'topic_end':
        lst = await state.get_data()
        lst = lst['topic']
        lst = ', '.join(lst)
        await state.update_data(topic=lst)
        markup = await back_keyboard('Отменить регистрацию')
    text = f'''Введите количество Ваших подписчиков'''
    await message.message.edit_text(text=text, reply_markup=markup)
    await state.set_state(VK.Subs.state)


async def vk_subs(message: types.Message, state: FSMContext):
    ''' Запоминает количество подписчиков и спрашивает опсиание блога'''
    await state.update_data(subs=message.text)
    text = 'Краткое описание блога \n*Опишите, что Вы транслируете в блоге'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(VK.Description.state)


async def vk_descroption(message: types.Message, state: FSMContext):
    ''' Запоминает описание и спрашивает country'''
    await state.update_data(description=message.text)
    text = 'Укажите Вашу страну и гоород'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(VK.Country.state)


async def vk_country(message: types.Message, state: FSMContext):
    ''' Запоминает country и спрашивает просмотры поста'''
    await state.update_data(city=message.text)
    text = '''Среднее количество просмотров постов'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(VK.Post_views.state)


async def vk_post_views(message: types.Message, state: FSMContext):
    ''' Запоминает охват post и спрашивает цену поста'''
    await state.update_data(stories_scope=message.text)
    text = '''Средняя стоимость поста'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(VK.Post.state)


async def vk_post(message: types.Message, state: FSMContext):
    ''' Запоминает цену post и спрашивает просмотры клипов '''
    await state.update_data(stories=message.text)
    text = '''Укажите, публикуете ли вы контент в формате VK клипов?'''
    markup = await reels_keyboard('VK')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(VK.Question_shotrs.state)


async def vk_questions_clips(message: types.Message, state: FSMContext):
    ''' Запоминает questions_clips и спрашивает pass '''
    data = message.data.split("_")
    if data[1] == 'yes':
        text = "Укажите среднее количество просмотров VK - клипов"
        await state.set_state(VK.Clip_views.state)
    if data[1] == 'no':
        await state.update_data(reels="не размещает")
        await state.update_data(reels_scope="не размещает")
        text = '''Ссылка на статистику 
*Ссылка на любой удобный для Вас диск, содержащий статистику аудитории по гендеру, возрасту, географии. '''
        await state.set_state(VK.Statistic.state)

    markup = await back_keyboard('Отменить регистрацию')
    await message.message.answer(text=text, reply_markup=markup)


async def vk_clip_views(message: types.Message, state: FSMContext):
    ''' Запоминает охват clip и спрашивает цену clip'''
    await state.update_data(reels_scope=message.text)
    text = '''Средняя стоимость VK-клипа'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(VK.Clip.state)


async def vk_clip(message: types.Message, state: FSMContext):
    ''' Запоминает цену clip и спрашивает статистику'''
    await state.update_data(reels=message.text)
    text = '''Ссылка на статистику 
*Ссылка на любой удобный для Вас диск, содержащий статистику аудитории по гендеру, возрасту, географии. '''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(VK.Statistic.state)


async def vk_statistic(message: types.Message, state: FSMContext):
    ''' Запоминает статистику, заканчивает регистрацию'''
    if is_link(message.text) == True:
        await state.update_data(statistic=message.text)
        text = '✅ Благодарим за интерес к сотрудничеству! С вами свяжутся в ближайшее время наши специалисты '
        await message.answer(text=text)
        spreadsheet = client.open_by_key(spreadsheet_bloger_id)
        sheet = spreadsheet.get_worksheet(2)
        num = len(sheet.col_values(1)) + 1
        data = await state.get_data()
        data = list(data.values())
        cell_list = sheet.range(f'A{num}:AQ{num}')
        cell_index = [0, 1, 2, 3, 4, 5, 9, 11, 14, 16, 24, 25, 33]
        for i, val in enumerate(cell_index):
            cell_list[val].value = data[i]
        cell_list.pop(41)
        cell_list.pop(34)
        cell_list.pop(10)
        sheet.update_cells(cell_list)
        await state.finish()
        await start_again(message)
    else:
        await number_wrong(message, number=False)


# НАЧАЛО ОПРОСА TG
async def start_poll_tg(message: types.Message, state: FSMContext, flag=None):
    ''' Начало опроса блогера tg, Number '''
    await state.set_state(TG.Number.state)
    await state.update_data(username=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)
    if Bloger(str(message.from_user.id)).check():
        num = Bloger(str(message.from_user.id)).get()
        text = f'Использовать номер {num}?'
        markup = await number_keyboard()
        await state.set_state(TG.Wait.state)
    else:
        # Запросить номер
        text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = await back_keyboard('Отменить регистрацию')
    if flag:
        text = 'Напишите свой новый номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = types.ReplyKeyboardRemove()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


async def tg_number(call: types.CallbackQuery, state: FSMContext):
    ''' Запоминает number и спрашивает Link'''
    if (call.data if type(call) is types.CallbackQuery else call.text) == 'number_y':
        await state.update_data(number=Bloger(f"{call.from_user.id}").get())
        text = '''Ссылка на Telegram канал
*В формате https://t.me/channel'''
    elif (call.data if type(call) is types.CallbackQuery else call.text) == 'number_n':
        await start_poll_tg(call, state, flag=True)
    else:
        if is_number((call.data if type(call) is types.CallbackQuery else call.text)) == True:
            await state.update_data(number=call.text)
            Bloger(f"{call.from_user.id}").record(call.text)
        else:
            await number_wrong(call)
            return
    text = '''Ссылка на Telegram канал
*В формате https://t.me/channel'''
    markup = await back_keyboard('Отменить регистрацию')
    await call.answer(text=text, reply_markup=markup)
    await state.set_state(TG.Link.state)


async def tg_number_wait(message: types.Message, state: FSMContext):
    if message.text == "Да✅":
        await state.update_data(number=Bloger(f"{message.from_user.id}").get())
        text = '''Ссылка на Telegram канал
*В формате https://t.me/channel'''
    else:
        await start_poll_tg(message, state, flag=True)
        await state.set_state(TG.Number.state)
        return
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(TG.Link.state)


async def tg_link(message: types.Message, state: FSMContext):
    ''' Запоминает ссылку на tg и спрашивает тематику'''
    if is_link(message.text) == True:
        await state.update_data(link=message.text)
        await state.update_data(topic=[])
        lst = get_config(flag=True)
        text = 'Выберите тематики, подходящие под ваш блог:'
        markup = await topic_keyboard(lst)
        await message.answer(text=text, reply_markup=markup)
        await state.set_state(TG.Topic.state)
    else:
        await number_wrong(message, number=False)


async def tg_topic_choose(message: types.Message, state: FSMContext):
    ''' Обрабатывает выбор тематики tg'''
    if message.data.split('_')[1] == 'Другое (указать в примечании)':
        text = 'Укажите тематику одним сообщением'
        await state.set_state(TG.Topic_another.state)
        await message.message.edit_text(text=text)
        return
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(message.data.split('_')[1])
    await state.update_data(topic=lst)
    text = f'''Тематика: {message.data.split('_')[1]} добавлена!
Желаете выбрать еще тематику?'''
    markup = await topic_keyboard_2()
    await message.message.edit_text(text=text, reply_markup=markup)


async def tg_topic_another(message: types.Message, state: FSMContext):
    ''' Обрабатывает выбор тематики - другое'''
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(message.text)
    await state.update_data(topic=lst)
    text = f'''Тематика: {message.text} добавлена!
Желаете выбрать еще тематику?'''
    markup = await topic_keyboard_2()
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(TG.Topic.state)


async def tg_topic_choose_2(message: types.Message, state: FSMContext):
    ''' обрабатывает клавиатуры выбора новой тематики ил закончить выбор '''
    if message.data == 'topic_start':
        lst = get_config(flag=True)
        text = 'Выберите тематику Вашего контента:'
        markup = await topic_keyboard(lst)
        await message.message.edit_text(text=text, reply_markup=markup)
        return
    elif message.data == 'topic_end':
        lst = await state.get_data()
        lst = lst['topic']
        lst = ', '.join(lst)
        await state.update_data(topic=lst)
        markup = await back_keyboard('Отменить регистрацию')
    text = f'''Введите количество Ваших подписчиков'''
    await message.message.edit_text(text=text, reply_markup=markup)
    await state.set_state(TG.Subs.state)


async def tg_subs(message: types.Message, state: FSMContext):
    ''' Запоминает количество подписчиков и post view'''
    await state.update_data(subs=message.text)
    text = 'Среднее количество просмотров'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(TG.Post_views.state)


async def tg_post_view(message: types.Message, state: FSMContext):
    ''' Запоминает post view и Post'''
    await state.update_data(description=message.text)
    text = 'Средняя стоимость размещения поста 1/24'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(TG.Post.state)


async def tg_post(message: types.Message, state: FSMContext):
    ''' Запоминает post и country'''
    await state.update_data(city=message.text)
    text = '''Укажите вашу страну и город'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(TG.Country.state)


async def tg_country(message: types.Message, state: FSMContext):
    ''' Запоминает country и desc'''
    await state.update_data(stories_scope=message.text)
    text = 'Краткое описание блога \n*Опишите, что Вы транслируете в блоге'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(TG.Description.state)


async def tg_description(message: types.Message, state: FSMContext):
    ''' Запоминает desc и спрашивает статистику '''
    await state.update_data(stories=message.text)
    text = '''Ссылка на статистику 
*Ссылка на любой удобный для Вас диск, содержащий статистику аудитории по гендеру, возрасту, географии. '''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(TG.Statistic.state)


async def tg_statistic(message: types.Message, state: FSMContext):
    ''' Запоминает статистику, заканчивает регистрацию'''
    if is_link(message.text) == True:
        await state.update_data(statistic=message.text)
        text = '✅ Благодарим за интерес к сотрудничеству! С вами свяжутся в ближайшее время наши специалисты '
        await message.answer(text=text)
        spreadsheet = client.open_by_key(spreadsheet_bloger_id)
        sheet = spreadsheet.get_worksheet(3)
        num = len(sheet.col_values(1)) + 1
        data = await state.get_data()
        data = list(data.values())
        cell_list = sheet.range(f'A{num}:AQ{num}')
        cell_index = [0, 1, 2, 3, 4, 5, 10, 12, 20, 23, 25]
        for i, val in enumerate(cell_index):
            cell_list[val].value = data[i]
        cell_list.pop(33)
        cell_list.pop(22)
        cell_list.pop(8)
        sheet.update_cells(cell_list)
        await state.finish()
        await start_again(message)
    else:
        await number_wrong(message, number=False)


# НАЧАЛО ОПРОСА DZ
async def start_poll_dz(message: types.Message, state: FSMContext, flag=None):
    ''' Начало опроса блогера dz, Number '''
    await state.set_state(DZ.Number.state)
    await state.update_data(username=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)
    if Bloger(str(message.from_user.id)).check():
        num = Bloger(str(message.from_user.id)).get()
        text = f'Использовать номер {num}?'
        markup = await number_keyboard()
        await state.set_state(DZ.Wait.state)
    else:
        # Запросить номер
        text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = await back_keyboard('Отменить регистрацию')
    if flag:
        text = 'Напишите свой новый номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = types.ReplyKeyboardRemove()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


async def dz_number(call: types.CallbackQuery, state: FSMContext):
    ''' Запоминает number и спрашивает Link'''
    if (call.data if type(call) is types.CallbackQuery else call.text) == 'number_y':
        await state.update_data(number=Bloger(f"{call.from_user.id}").get())
        text = '''Ссылка на страницу Дзен'''
    elif (call.data if type(call) is types.CallbackQuery else call.text) == 'number_n':
        await start_poll_dz(call, state, flag=True)
    else:
        if is_number((call.data if type(call) is types.CallbackQuery else call.text)) == True:
            await state.update_data(number=call.text)
            Bloger(f"{call.from_user.id}").record(call.text)
        else:
            await number_wrong(call)
            return
    text = '''Ссылка на страницу Дзен'''
    await call.answer(text=text)
    await state.set_state(DZ.Link.state)


async def dz_number_wait(message: types.Message, state: FSMContext):
    if message.text == "Да✅":
        await state.update_data(number=Bloger(f"{message.from_user.id}").get())
        text = '''Ссылка на страницу Дзен'''
    else:
        await start_poll_dz(message, state, flag=True)
        await state.set_state(DZ.Number.state)
        return
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(DZ.Link.state)


async def dz_link(message: types.Message, state: FSMContext):
    ''' Запоминает ссылку на dz и спрашивает тематику'''
    if is_link(message.text) == True:
        await state.update_data(link=message.text)
        await state.update_data(topic=[])
        lst = get_config(flag=True)
        text = 'Выберите тематики, подходящие под ваш блог:'
        markup = await topic_keyboard(lst)
        await message.answer(text=text, reply_markup=markup)
        await state.set_state(DZ.Topic.state)
    else:
        await number_wrong(message, number=False)


async def dz_topic_choose(message: types.Message, state: FSMContext):
    ''' Обрабатывает выбор тематики dz'''
    if message.data.split('_')[1] == 'Другое (указать в примечании)':
        text = 'Укажите тематику одним сообщением'
        await state.set_state(DZ.Topic_another.state)
        await message.message.edit_text(text=text)
        return
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(message.data.split('_')[1])
    await state.update_data(topic=lst)
    text = f'''Тематика: {message.data.split('_')[1]} добавлена!
Желаете выбрать еще тематику?'''
    markup = await topic_keyboard_2()
    await message.message.edit_text(text=text, reply_markup=markup)


async def dz_topic_another(message: types.Message, state: FSMContext):
    ''' Обрабатывает выбор тематики - другое'''
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(message.text)
    await state.update_data(topic=lst)
    text = f'''Тематика: {message.text} добавлена!
Желаете выбрать еще тематику?'''
    markup = await topic_keyboard_2()
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(DZ.Topic.state)


async def dz_topic_choose_2(message: types.Message, state: FSMContext):
    ''' обрабатывает клавиатуры выбора новой тематики ил закончить выбор '''
    if message.data == 'topic_start':
        lst = get_config(flag=True)
        text = 'Выберите тематику Вашего контента:'
        markup = await topic_keyboard(lst)
        await message.message.edit_text(text=text, reply_markup=markup)
        return
    elif message.data == 'topic_end':
        lst = await state.get_data()
        lst = lst['topic']
        lst = ', '.join(lst)
        await state.update_data(topic=lst)
        markup = await back_keyboard('Отменить регистрацию')
    text = f'''Введите количество Ваших подписчиков'''
    await message.message.edit_text(text=text, reply_markup=markup)
    await state.set_state(DZ.Subs.state)


async def dz_subs(message: types.Message, state: FSMContext):
    ''' Запоминает количество подписчиков и post view'''
    await state.update_data(subs=message.text)
    text = 'Среднее количество просмотров постов'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(DZ.Post_views.state)


async def dz_post_view(message: types.Message, state: FSMContext):
    ''' Запоминает post view и Post'''
    await state.update_data(description=message.text)
    text = 'Средняя стоимость размещения поста'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(DZ.Post.state)


async def dz_post(message: types.Message, state: FSMContext):
    ''' Запоминает post и desc'''
    await state.update_data(stories_scope=message.text)
    text = 'Краткое описание блога \n*Опишите, что Вы транслируете в блоге'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(DZ.Description.state)


async def dz_description(message: types.Message, state: FSMContext):
    ''' Запоминает desc и спрашивает статистику '''
    await state.update_data(stories=message.text)
    text = '''Ссылка на статистику 
*Ссылка на любой удобный для Вас диск, содержащий статистику аудитории по гендеру, возрасту, географии. '''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(DZ.Statistic.state)


async def dz_statistic(message: types.Message, state: FSMContext):
    ''' Запоминает статистику, заканчивает регистрацию'''
    if is_link(message.text) == True:
        await state.update_data(statistic=message.text)
        text = '✅ Благодарим за интерес к сотрудничеству! С вами свяжутся в ближайшее время наши специалисты '
        await message.answer(text=text)
        spreadsheet = client.open_by_key(spreadsheet_bloger_id)
        sheet = spreadsheet.get_worksheet(4)
        num = len(sheet.col_values(1)) + 1
        data = await state.get_data()
        data = list(data.values())
        cell_list = sheet.range(f'A{num}:AQ{num}')
        cell_index = [0, 1, 2, 3, 4, 5, 6, 8, 18, 20]
        for i, val in enumerate(cell_index):
            cell_list[val].value = data[i]
        cell_list.pop(28)
        cell_list.pop(21)
        cell_list.pop(17)
        sheet.update_cells(cell_list)
        await state.finish()
        await start_again(message)
    else:
        await number_wrong(message, number=False)


# НАЧАЛО ОПРОСА ДРУГОЕ
async def start_poll_another(message: types.Message, state: FSMContext, flag=None):
    ''' Начало опроса блогера another, Number '''
    await state.set_state(Another.Number.state)
    await state.update_data(username=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)
    if Bloger(str(message.from_user.id)).check():
        num = Bloger(str(message.from_user.id)).get()
        text = f'Использовать номер {num}?'
        markup = await number_keyboard()
        await state.set_state(Another.Wait.state)
    else:
        # Запросить номер
        text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = await back_keyboard('Отменить регистрацию')
    if flag:
        text = 'Напишите свой новый номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = types.ReplyKeyboardRemove()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


async def another_number(call: types.CallbackQuery, state: FSMContext):
    ''' Запоминает number и спрашивает Link'''
    if (call.data if type(call) is types.CallbackQuery else call.text) == 'number_y':
        await state.update_data(number=Bloger(f"{call.from_user.id}").get())
        text = '''Ссылка на страницу Вашего блога'''
    elif (call.data if type(call) is types.CallbackQuery else call.text) == 'number_n':
        await start_poll_another(call, state, flag=True)
    else:
        if is_number((call.data if type(call) is types.CallbackQuery else call.text)) == True:
            await state.update_data(number=call.text)
            Bloger(f"{call.from_user.id}").record(call.text)
        else:
            await number_wrong(call)
            return
    text = '''Ссылка на страницу Вашего блога'''
    await call.answer(text=text)
    await state.set_state(Another.Link.state)


async def another_number_wait(message: types.Message, state: FSMContext):
    if message.text == "Да✅":
        await state.update_data(number=Bloger(f"{message.from_user.id}").get())
        text = '''Ссылка на страницу Вашего блога'''
    else:
        await start_poll_another(message, state, flag=True)
        await state.set_state(Another.Number.state)
        return
    await message.answer(text=text, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Another.Link.state)


async def another_link(message: types.Message, state: FSMContext):
    ''' Запоминает ссылку на another и спрашивает тематику'''
    if is_link(message.text) == True:
        await state.update_data(link=message.text)
        await state.update_data(topic=[])
        lst = get_config(flag=True)
        text = 'Выберите тематики, подходящие под ваш блог:'
        markup = await topic_keyboard(lst)
        await message.answer(text=text, reply_markup=markup)
        await state.set_state(Another.Topic.state)
    else:
        await number_wrong(message, number=False)


async def another_topic_choose(message: types.Message, state: FSMContext):
    ''' Обрабатывает выбор тематики another'''
    if message.data.split('_')[1] == 'Другое (указать в примечании)':
        text = 'Укажите тематику одним сообщением'
        await state.set_state(Another.Topic_another.state)
        await message.message.edit_text(text=text)
        return
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(message.data.split('_')[1])
    await state.update_data(topic=lst)
    text = f'''Тематика: {message.data.split('_')[1]} добавлена!
Желаете выбрать еще тематику?'''
    markup = await topic_keyboard_2()
    await message.message.edit_text(text=text, reply_markup=markup)


async def another_topic_another(message: types.Message, state: FSMContext):
    ''' Обрабатывает выбор тематики - другое'''
    lst = await state.get_data()
    lst = lst['topic']
    lst.append(message.text)
    await state.update_data(topic=lst)
    text = f'''Тематика: {message.text} добавлена!
Желаете выбрать еще тематику?'''
    markup = await topic_keyboard_2()
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(Another.Topic.state)


async def another_topic_choose_2(message: types.Message, state: FSMContext):
    ''' обрабатывает клавиатуры выбора новой тематики ил закончить выбор '''
    if message.data == 'topic_start':
        lst = get_config(flag=True)
        text = 'Выберите тематику Вашего контента:'
        markup = await topic_keyboard(lst)
        await message.message.edit_text(text=text, reply_markup=markup)
        return
    elif message.data == 'topic_end':
        lst = await state.get_data()
        lst = lst['topic']
        lst = ', '.join(lst)
        await state.update_data(topic=lst)
        markup = await back_keyboard('Отменить регистрацию')
    text = f'''Введите количество Ваших подписчиков'''
    await message.message.edit_text(text=text, reply_markup=markup)
    await state.set_state(Another.Subs.state)


async def another_subs(message: types.Message, state: FSMContext):
    ''' Запоминает количество подписчиков и post view'''
    await state.update_data(subs=message.text)
    text = 'Среднее количество просмотров публикации (пост, видео или другое)'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(Another.Post_views.state)


async def another_post_view(message: types.Message, state: FSMContext):
    ''' Запоминает post view и Post'''
    await state.update_data(description=message.text)
    text = 'Средняя стоимость размещения публикации'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(Another.Post.state)


async def another_post(message: types.Message, state: FSMContext):
    ''' Запоминает post и desc'''
    await state.update_data(stories_scope=message.text)
    text = 'Краткое описание блога \n*Опишите, что Вы транслируете в блоге'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(Another.Description.state)


async def another_description(message: types.Message, state: FSMContext):
    ''' Запоминает desc и спрашивает статистику '''
    await state.update_data(stories=message.text)
    text = '''Ссылка на статистику 
*Ссылка на любой удобный для Вас диск, содержащий статистику аудитории по гендеру, возрасту, географии. '''
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text=text, reply_markup=markup)
    await state.set_state(Another.Statistic.state)


async def another_statistic(message: types.Message, state: FSMContext):
    ''' Запоминает статистику, заканчивает регистрацию'''
    if is_link(message.text) == True:
        await state.update_data(statistic=message.text)
        text = '✅ Благодарим за интерес к сотрудничеству! С вами свяжутся в ближайшее время наши специалисты '
        await message.answer(text=text)
        spreadsheet = client.open_by_key(spreadsheet_bloger_id)
        sheet = spreadsheet.get_worksheet(5)
        num = len(sheet.col_values(1)) + 1
        data = await state.get_data()
        data = list(data.values())
        cell_list = sheet.range(f'A{num}:AQ{num}')
        cell_index = [0, 1, 2, 3, 4, 5, 6, 8, 18, 20]
        for i, val in enumerate(cell_index):
            cell_list[val].value = data[i]
        cell_list.pop(28)
        cell_list.pop(21)
        cell_list.pop(17)
        sheet.update_cells(cell_list)
        await state.finish()
        await start_again(message)
    else:
        await number_wrong(message, number=False)


# КОНТАКТЫ
async def contacts(call: types.CallbackQuery):
    text = '''Telegram: @era_agency_info
Самый оперативный способ связи  

Сайт: bloggers.era-agency.ru
E-mail: info@era-agency.ru

График работы: 
Понедельник - Пятница / 10:00 - 19:00

По срочным запросам вне графика работы:
WhatsApp: +7 (993) 338-78-28'''
    markup = await back_keyboard('Закрыть')
    await call.bot.send_message(call.from_user.id, text=text, reply_markup=markup)


# РЕГИСТРАЦИЯ ХЕНДЛЕРОВ
def registration_handlers(dp: Dispatcher):
    # Commands
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(work_write, commands=['work'])
    dp.register_message_handler(start, text=['старт'])
    dp.register_callback_query_handler(back_start, state='*', text='start')
    # dp.register_message_handler(k, commands=['k'])
    # NEW ONES
    # back
    dp.register_callback_query_handler(back, state='*', text='back')
    # хочу попасть в ЕРА
    dp.register_message_handler(soc_media_name, state=SocMedia.Name)
    dp.register_callback_query_handler(soc_media_sm, state=SocMedia.SM)
    dp.register_message_handler(soc_media_link, state=SocMedia.Link)
    dp.register_message_handler(soc_media_subs, state=SocMedia.Subs)
    dp.register_message_handler(soc_media_city, state=SocMedia.City)
    dp.register_message_handler(soc_media_geo1, state=SocMedia.Geo1)
    dp.register_message_handler(soc_media_geo2, state=SocMedia.Geo2)
    dp.register_callback_query_handler(soc_media_topic, state=SocMedia.Topic, text_startswith='Topic')
    dp.register_callback_query_handler(soc_media_topic_2, state=SocMedia.Topic, text_startswith='topic')
    dp.register_message_handler(soc_media_topic_another, state=SocMedia.Topic_another)
    dp.register_message_handler(soc_media_description, state=SocMedia.Description)
    dp.register_callback_query_handler(soc_media_description2, text='registr_end')
    # manager
    dp.register_callback_query_handler(manager_new_start, text='manager')
    dp.register_message_handler(manager_new_name, state=Manager_new.Name)
    dp.register_message_handler(manager_new_count, state=Manager_new.Count)
    dp.register_message_handler(manager_new_company, state=Manager_new.Company)
    dp.register_callback_query_handler(manager_new_company, state=Manager_new.Company)
    dp.register_message_handler(manager_new_link, state=Manager_new.Link)
    dp.register_callback_query_handler(manager_new_link, state=Manager_new.Link)
    dp.register_callback_query_handler(manager_new_q, state=Manager_new.Q)
    # work
    dp.register_message_handler(work_pass, state=Work_write.Pass)
    dp.register_message_handler(work_text, state=Work_write.Text)
    # work profile
    dp.register_callback_query_handler(work_profile_start, text="work_profile")
    dp.register_message_handler(work_name, state=Work.Name)
    dp.register_message_handler(work_post, state=Work.Post)
    dp.register_message_handler(work_exp, state=Work.Exp)
    dp.register_message_handler(work_skills, state=Work.Skills)
    dp.register_message_handler(work_reason, state=Work.Reason)
    dp.register_message_handler(work_age, state=Work.Age)
    dp.register_message_handler(work_load, state=Work.Load)
    dp.register_message_handler(work_linkResume, state=Work.Link_resume)
    dp.register_callback_query_handler(work_linkResume, state=Work.Link_resume)
    dp.register_message_handler(work_linkCase, state=Work.Link_case)
    dp.register_callback_query_handler(work_linkCase, state=Work.Link_case)
    # for_clients
    dp.register_callback_query_handler(clients_start, text='for_clients')
    dp.register_callback_query_handler(clients_name, state=Client.Name)
    dp.register_message_handler(clients_company, state=Client.Company)
    dp.register_message_handler(clients_post, state=Client.Post)
    dp.register_callback_query_handler(clients_post, state=Client.Post)
    dp.register_message_handler(clients_site, state=Client.Site)
    dp.register_callback_query_handler(clients_site, state=Client.Site)
    dp.register_message_handler(clients_reason, state=Client.Reason)
    dp.register_callback_query_handler(clients_reason, state=Client.Reason)
    dp.register_message_handler(clients_type, state=Client.Type)
    dp.register_message_handler(clients_end, state=Client.End)
    dp.register_callback_query_handler(clients_end, state=Client.End)


    # Callbacks
    dp.register_callback_query_handler(start_poll_col, text='colab_start')
    dp.register_callback_query_handler(start_Work, text='work')
    # dp.register_callback_query_handler(collaboration, text='collaboration')
    dp.register_callback_query_handler(start_poll_barter, text='barter')
    dp.register_callback_query_handler(start_soc_media, text='bloger')
    dp.register_callback_query_handler(start_poll_inst, text='Instagram')
    dp.register_callback_query_handler(start_poll_yt, text='YT')
    dp.register_callback_query_handler(start_poll_vk, text='VK')
    dp.register_callback_query_handler(start_poll_tg, text='TG')
    dp.register_callback_query_handler(start_poll_dz, text='Дзен')
    dp.register_callback_query_handler(start_poll_another, text='Другое')
    dp.register_callback_query_handler(start_ExcConract, text='exclusive_conract')
    # States
    # Бартер
    dp.register_message_handler(barter_name, state=Barter.Name)
    dp.register_message_handler(barter_number, state=Barter.Number)
    dp.register_message_handler(barter_link, state=Barter.Link)
    dp.register_message_handler(barter_subs, state=Barter.Subs)
    dp.register_message_handler(barter_city, state=Barter.City)
    dp.register_message_handler(barter_city, state=Barter.City)
    dp.register_message_handler(barter_offer, state=Barter.Offer)
    # Менеджер
    dp.register_message_handler(manager_number, state=Manager.Number)
    dp.register_message_handler(manager_name, state=Manager.Name)
    dp.register_message_handler(manager_link, state=Manager.Link)
    dp.register_callback_query_handler(manager_exclusive, state=Manager.Exclusive)
    dp.register_message_handler(manager_exclusive_links, state=Manager.Exclusive_links)
    dp.register_message_handler(manager_q, state=Manager.Q)
    # Сотрудничество
    dp.register_message_handler(colab_name, state=Colab.Name)
    dp.register_message_handler(colab_post, state=Colab.Post)
    dp.register_callback_query_handler(colab_post, state=Colab.Post)
    dp.register_message_handler(colab_company, state=Colab.Company)
    dp.register_callback_query_handler(colab_company, state=Colab.Company)
    dp.register_callback_query_handler(colab_reason, state=Colab.Reason)
    dp.register_message_handler(colab_reason, state=Colab.Reason)
    # Instagram
    dp.register_message_handler(inst_number, state=Instagram.Number)
    dp.register_message_handler(inst_number_wait, state=Instagram.Wait)
    dp.register_message_handler(inst_link, state=Instagram.Link)
    dp.register_callback_query_handler(inst_topic_choose, state=Instagram.Topic, text_startswith='Topic')
    dp.register_callback_query_handler(inst_topic_choose_2, state=Instagram.Topic, text_startswith='topic')
    dp.register_message_handler(inst_topic_another, state=Instagram.Topic_another)
    dp.register_message_handler(inst_subs, state=Instagram.Subs)
    dp.register_message_handler(inst_descroption, state=Instagram.Description)
    dp.register_message_handler(inst_city, state=Instagram.City)
    dp.register_message_handler(inst_stories, state=Instagram.Stories)
    dp.register_message_handler(inst_stories_scope, state=Instagram.Stories_scope)
    dp.register_message_handler(inst_reels, state=Instagram.Reels)
    dp.register_message_handler(inst_reels_scope, state=Instagram.Reels_scope)
    dp.register_message_handler(inst_statistic, state=Instagram.Statistic)
    # YouTube
    dp.register_message_handler(yt_number, state=YT.Number)
    dp.register_message_handler(yt_number_wait, state=YT.Wait)
    dp.register_message_handler(yt_link, state=YT.Link)
    dp.register_callback_query_handler(yt_topic_choose, state=YT.Topic, text_startswith='Topic')
    dp.register_callback_query_handler(yt_topic_choose_2, state=YT.Topic, text_startswith='topic')
    dp.register_message_handler(yt_topic_another, state=YT.Topic_another)
    dp.register_message_handler(yt_subs, state=YT.Subs)
    dp.register_message_handler(yt_descroption, state=YT.Description)
    dp.register_message_handler(yt_country, state=YT.Country)
    dp.register_callback_query_handler(yt_questions_shorts, state=YT.Question_shotrs)
    dp.register_message_handler(yt_shorts, state=YT.Shorts)
    dp.register_message_handler(yt_shorts_views, state=YT.Shorts_views)
    dp.register_message_handler(yt_video, state=YT.Video)
    dp.register_message_handler(yt_video_views, state=YT.Video_views)
    dp.register_message_handler(yt_statistic, state=YT.Statistic)
    # VK
    dp.register_message_handler(vk_number, state=VK.Number)
    dp.register_message_handler(vk_number_wait, state=VK.Wait)
    dp.register_message_handler(vk_link, state=VK.Link)
    dp.register_callback_query_handler(vk_topic_choose, state=VK.Topic, text_startswith='Topic')
    dp.register_callback_query_handler(vk_topic_choose_2, state=VK.Topic, text_startswith='topic')
    dp.register_message_handler(vk_topic_another, state=VK.Topic_another)
    dp.register_message_handler(vk_subs, state=VK.Subs)
    dp.register_message_handler(vk_descroption, state=VK.Description)
    dp.register_message_handler(vk_country, state=VK.Country)
    dp.register_callback_query_handler(vk_questions_clips, state=VK.Question_shotrs)
    dp.register_message_handler(vk_post, state=VK.Post)
    dp.register_message_handler(vk_post_views, state=VK.Post_views)
    dp.register_message_handler(vk_clip, state=VK.Clip)
    dp.register_message_handler(vk_clip_views, state=VK.Clip_views)
    dp.register_message_handler(vk_statistic, state=VK.Statistic)
    # TG
    dp.register_message_handler(tg_number, state=TG.Number)
    dp.register_message_handler(tg_number_wait, state=TG.Wait)
    dp.register_message_handler(tg_link, state=TG.Link)
    dp.register_callback_query_handler(tg_topic_choose, state=TG.Topic, text_startswith='Topic')
    dp.register_callback_query_handler(tg_topic_choose_2, state=TG.Topic, text_startswith='topic')
    dp.register_message_handler(tg_topic_another, state=TG.Topic_another)
    dp.register_message_handler(tg_subs, state=TG.Subs)
    dp.register_message_handler(tg_post_view, state=TG.Post_views)
    dp.register_message_handler(tg_post, state=TG.Post)
    dp.register_message_handler(tg_country, state=TG.Country)
    dp.register_message_handler(tg_description, state=TG.Description)
    dp.register_message_handler(tg_statistic, state=TG.Statistic)
    # Dzen
    dp.register_message_handler(dz_number, state=DZ.Number)
    dp.register_message_handler(dz_number_wait, state=DZ.Wait)
    dp.register_message_handler(dz_link, state=DZ.Link)
    dp.register_callback_query_handler(dz_topic_choose, state=DZ.Topic, text_startswith='Topic')
    dp.register_callback_query_handler(dz_topic_choose_2, state=DZ.Topic, text_startswith='topic')
    dp.register_message_handler(dz_topic_another, state=DZ.Topic_another)
    dp.register_message_handler(dz_subs, state=DZ.Subs)
    dp.register_message_handler(dz_post_view, state=DZ.Post_views)
    dp.register_message_handler(dz_post, state=DZ.Post)
    dp.register_message_handler(dz_description, state=DZ.Description)
    dp.register_message_handler(dz_statistic, state=DZ.Statistic)
    # Another
    dp.register_message_handler(another_number, state=Another.Number)
    dp.register_message_handler(another_number_wait, state=Another.Wait)
    dp.register_message_handler(another_link, state=Another.Link)
    dp.register_callback_query_handler(another_topic_choose, state=Another.Topic, text_startswith='Topic')
    dp.register_callback_query_handler(another_topic_choose_2, state=Another.Topic, text_startswith='topic')
    dp.register_message_handler(another_topic_another, state=Another.Topic_another)
    dp.register_message_handler(another_subs, state=Another.Subs)
    dp.register_message_handler(another_post_view, state=Another.Post_views)
    dp.register_message_handler(another_post, state=Another.Post)
    dp.register_message_handler(another_description, state=Another.Description)
    dp.register_message_handler(another_statistic, state=Another.Statistic)
    # Контакты
    dp.register_callback_query_handler(contacts, text_startswith='contacts')

