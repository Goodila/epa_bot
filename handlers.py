import os
from aiogram import types, Dispatcher, types
from keyboards import start_keyboard, colab_keyboard, manager_keyboard, bloger_keyboard, number_keyboard
from keyboards import topic_keyboard, topic_keyboard_2, back_keyboard, reels_keyboard
from aiogram.dispatcher import FSMContext
from states import Work, Barter, Manager, Colab, Instagram, YT, VK, TG, DZ, Another
from funcs import get_config, Bloger, is_link, is_number
import time
from asyncio import sleep

#работа с гугл таблицами
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


async def number_wrong(message, number=True, text2='К сожалению, Вы прислали ссылку неверного формата. Повторно укажите сылку в формате "https://somesite.ru"'):
    text = 'Вы ввели номер неверного формата. Пожалуйства, следуйте формату +7***-***-**-**. \nВведите номер телефона повторно'
    if number == False:
        text=text2
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)


async def start(message: types.Message):
    text = '''Приветствую! На связи бот Единого Рекламного Агентства ЕРА ✌🏻

С моей помощью Вы можете: 
✏️ заполнить данные, чтобы попасть в базу блогеров ЕРА и получать рекламные предложения
✏️ подать анкету , если хотите работать у нас в компании

В разделе сотрудничество:
✏️ заполнить заявку на сотрудничество если ты менеджер блогеров
✏️ заполнить заявку-предложение о сотрудничестве с ЕРА
✏️ заполнить заявку на получение уведомлений о бесплатных PR-событиях и мероприятиях  для блогеров

'''
    markup = await start_keyboard()
    if isinstance(message, types.Message):
        await message.answer(text=text, reply_markup=markup)
    elif isinstance(message, types.CallbackQuery):
        await message.message.edit_text(text=text, reply_markup=markup)



async def start_again(message: types.Message):
    text = '''Вы закончили регистрацию! Можете продолжить работу с нашим ботом в других разделах. '''
    markup = await start_keyboard()
    await message.answer(text=text, reply_markup=markup)


async def back_start(message: types.Message, state: FSMContext):
    ''' старт после отмены регистрации'''
    await state.finish()
    await start(message)


async def help(message: types.Message):
    await message.answer('help')


async def me(message: types.Message):
    print(message)
    

async def start_poll_work(message: types.Message, state: FSMContext):
    ''' Начало опроса по анкете на работу, номер телефона '''
    await state.set_state(Work.Number.state)
    await state.update_data(username=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)
    text = '''Для заполнения анкеты на трудоустройство следуйте инструкциям:
    \nНапишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'''
    markup = await back_keyboard('Назад')
    await message.message.edit_text(text, reply_markup=markup)


async def work_number(message: types.Message, state: FSMContext):
    ''' Запоминает номер телефона, спрашивает имя'''
    if is_number(message.text) == True:
        await state.update_data(number=message.text)
        text = 'Впишите свое полное ФИО'
        await state.set_state(Work.Name.state)
        markup = await back_keyboard('Отменить регистрацию')
        await message.answer(text, reply_markup=markup)
    else:
        text = 'Вы ввели номер неверного формата. Пожалуйства, следуйте формату +7***-***-**-**. \nВведите номер телефона повторно'
        markup = await back_keyboard('Отменить регистрацию')
        await message.answer(text, reply_markup=markup)



async def work_name(message: types.Message, state: FSMContext):
    ''' Запоминает имя, спрашивает возраст'''
    await state.update_data(name=message.text)
    text = 'Напишите свой возраст'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Work.Age.state)


async def work_age(message: types.Message, state: FSMContext):
    ''' Запоминает возраст, спрашивает должность'''
    await state.update_data(age=message.text)
    text = 'Напишите желаемую должность в компании'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Work.Post.state)


async def work_post(message: types.Message, state: FSMContext):
    ''' Запоминает должность, спрашивает Hard & Soft Skills '''
    await state.update_data(post=message.text)
    text = 'Напишите Ваши Hard и Soft skills одним сообщением'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Work.Why.state)


async def work_why(message: types.Message, state: FSMContext):
    ''' Запоминает hard & soft, почему именно ЕРА'''
    await state.update_data(why=message.text)
    text = 'Почему Вы выбрали именно ЕРА для трудоустройства?'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Work.Know_from.state)


async def work_know_from(message: types.Message, state: FSMContext):
    ''' Запоминает почему ЕРА, спрашивает резюме'''
    await state.update_data(know_from=message.text)
    text='Пришлите ссылку на Ваше резюме'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Work.Link_resume.state)


async def work_resume(message: types.Message, state: FSMContext):
    ''' Запоминает резюме, спрашивает кейсы'''
    if is_link(message.text) == True:
        await state.update_data(resume=message.text)
        text = 'Ссылка на кейсы.\n*Впишите ссылку или впишите "нет"'
        markup = await back_keyboard('Отменить регистрацию')
        await message.answer(text, reply_markup=markup)
        await state.set_state(Work.Link_case.state)
    else:
        text='К сожалению, Вы прислали ссылку неверного формата. Повторно укажите сылку в формате "https://somesite.ru"'
        markup = await back_keyboard('Отменить регистрацию')
        await message.answer(text, reply_markup=markup)


async def work_case(message: types.Message, state: FSMContext):
    ''' запоминает кейсы, спрашивает про загруженность '''
    await state.update_data(case=message.text)
    text = 'Текущая степень загруженности (учеба, другая работа, разница во времени с МСК)'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Work.Load.state)


async def work_load(message: types.Message, state: FSMContext):
    ''' Запоминает load, заканчивает регистрацию'''
    await state.update_data(load=message.text)
    text = '✅ Благодарим за интерес к сотрудничеству! С вами свяжутся в ближайшее время наши специалисты '
    await message.answer(text=text)
    spreadsheet = client.open_by_key(spreadsheet_era_id)
    sheet = spreadsheet.get_worksheet(0)  
    data = await state.get_data()
    sheet.append_row(list(data.values()))
    await state.finish()
    await start_again(message)


async def collaboration(message: types.Message):
    text = '''Приветствую Вас в разделе "Сотрудничество"

    ✏️Пройдя краткую регистрацию в разделе "Бартер", Вы сможете бесплатно посещать разного рода мероприятия.

    ✏️Зарегистрируетесь как менеджер блогеров, и мы свяжемся с Вами для сотрудничества, получив всю необходимую информацию
    
    ✏️ По иным вопросам сотрудничетсва, нажмите на кнопку "Сотрудничество с ЕРА".'''
    markup = await colab_keyboard()
    await message.bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=markup)


#НАЧАЛО ОПРОСА БАРТЕР
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
        text='К сожалению, Вы прислали ссылку неверного формата. Повторно укажите сылку в формате "https://somesite.ru"'
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


#НАЧАЛО ОПРОСА МЕНЕДЖЕР
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
        text = 'Есть ли блогеры у Вас на эксклюзивном сотрудничестве и/или те у кого вы вы непосредственно PR.'
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


#НАЧАЛО ОПРОСА СОТРУДНИЧЕСТВО 
async def start_poll_col(message: types.Message, state: FSMContext):
    ''' Начало опроса по сотрудничеству, Name '''
    await state.set_state(Colab.Name.state)
    await state.update_data(username=message.from_user.username)
    await state.update_data(user_id=message.from_user.id)
    text = '''Для оставления заявки на сотрудничество следуйте инструкциям:
    \nВпишите свое полное имя.'''
    markup = await back_keyboard('Отменить регистрацию')
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


async def colab_name(message: types.Message, state: FSMContext):
    ''' Запоминает name и спрашивает post'''
    await state.update_data(name=message.text)
    text = 'Ваша должность'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Colab.Post.state)


async def colab_post(message: types.Message, state: FSMContext):
    ''' Запоминает post и спрашивает company'''
    await state.update_data(post=message.text)
    text = 'Название Вашей компании'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Colab.Company.state)


async def colab_company(message: types.Message, state: FSMContext):
    ''' Запоминает company и спрашивает reason'''
    await state.update_data(company=message.text)
    text = 'Причина Вашего обращения (как Вы хотите с нами сотрудничать). Напишите одним сообщением'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Colab.Reason.state)


async def colab_reason(message: types.Message, state: FSMContext):
    ''' Запоминает reason и спрашивает number'''
    await state.update_data(reason=message.text)
    text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
    markup = await back_keyboard('Отменить регистрацию')
    await message.answer(text, reply_markup=markup)
    await state.set_state(Colab.Number.state)


async def colab_number(message: types.Message, state: FSMContext):
    ''' Запоминает номер, заканчивает регистрацию'''
    if is_number(message.text) == True:
        await state.update_data(number=message.text)
        text = '✅ Благодарим за интерес к сотрудничеству! С вами свяжутся в ближайшее время наши специалисты '
        await message.answer(text=text)
        spreadsheet = client.open_by_key(spreadsheet_era_id)
        sheet = spreadsheet.get_worksheet(3)  
        data = await state.get_data()
        sheet.append_row(list(data.values()))
        await state.finish()
        await start_again(message)
    else:
        await number_wrong(message)


#НАЧАЛО ОПРОСА БЛОГЕР
async def start_poll_bloger(message: types.Message, state: FSMContext):
    ''' Выбераем соцсеть для регистрации '''
    text = '''Выберите социальную сеть со своим блогом
    (после заполенения информации об одном, можно будет добавить другие социальные сети)'''
    markup = await bloger_keyboard()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


#НАЧАЛО ОПРОСА INSTAGRM
async def start_poll_inst(message: types.Message, state: FSMContext, flag = None):
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
        #Запросить номер    
        text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = await back_keyboard('Отменить регистрацию')
    if flag:
        text = 'Напишите свой новый номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup =  types.ReplyKeyboardRemove()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


async def inst_number(call: types.CallbackQuery, state: FSMContext):
    ''' Запоминает number и спрашивает Link'''
    if (call.data if type(call) is types.CallbackQuery else call.text) == 'number_y':
        await state.update_data(number=Bloger(f"{call.from_user.id}").get())
        text = 'Отправьте ссылку на Ваш Instagram'
    elif (call.data if type(call) is types.CallbackQuery else call.text) == 'number_n':
        await start_poll_inst(call, state, flag = True)
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
        await start_poll_inst(message, state, flag = True)
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
        await number_wrong(message, number=False, text2='К сожалению, Вы прислали ссылку неверного формата. Повторно укажите сылку в формате "https://somesite.ru"')


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
        num=len(sheet.col_values(1)) + 1
        data = await state.get_data()
        data = list(data.values())
        cell_list = sheet.range(f'A{num}:AQ{num}')  
        cell_index = [0,1,2,3,4,5,10,11,18,19,27,28,33]
        for i, val in enumerate(cell_index):
            cell_list[val].value = data[i]
        cell_list.pop(9)
        sheet.update_cells(cell_list)
        await state.finish()
        await start_again(message)
    else:
        await number_wrong(message, number=False)


#НАЧАЛО ОПРОСА YOUTUBE
async def start_poll_yt(message: types.Message, state: FSMContext, flag = None):
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
        #Запросить номер    
        text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = await back_keyboard('Отменить регистрацию')
    if flag:
        text = 'Напишите свой новый номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup =  types.ReplyKeyboardRemove()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


async def yt_number(call: types.CallbackQuery, state: FSMContext):
    ''' Запоминает number и спрашивает Link'''
    if (call.data if type(call) is types.CallbackQuery else call.text) == 'number_y':
        await state.update_data(number=Bloger(f"{call.from_user.id}").get())
        text = 'Ссылка на YouTube канал \n*В формате https://www.youtube.com/channel'
    elif (call.data if type(call) is types.CallbackQuery else call.text) == 'number_n':
        await start_poll_yt(call, state, flag = True)
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
        await start_poll_yt(message, state, flag = True)
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
        num=len(sheet.col_values(1)) + 1
        data = await state.get_data()
        data = list(data.values())
        cell_list = sheet.range(f'A{num}:AQ{num}')  
        cell_index = [0,1,2,3,4,5,10,12,16,17,22,23,31]
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


#НАЧАЛО ОПРОСА VK
async def start_poll_vk(message: types.Message, state: FSMContext, flag = None):
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
        #Запросить номер    
        text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = await back_keyboard('Отменить регистрацию')
    if flag:
        text = 'Напишите свой новый номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup =  types.ReplyKeyboardRemove()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


async def vk_number(call: types.CallbackQuery, state: FSMContext):
    ''' Запоминает number и спрашивает Link'''
    if (call.data if type(call) is types.CallbackQuery else call.text) == 'number_y':
        await state.update_data(number=Bloger(f"{call.from_user.id}").get())
        text = 'Ссылка на страницу Вконтакте'
    elif (call.data if type(call) is types.CallbackQuery else call.text) == 'number_n':
        await start_poll_vk(call, state, flag = True)
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
        await start_poll_vk(message, state, flag = True)
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
        num=len(sheet.col_values(1)) + 1
        data = await state.get_data()
        data = list(data.values())
        cell_list = sheet.range(f'A{num}:AQ{num}')
        cell_index = [0,1,2,3,4,5,9,11,14,16,24,25,33]
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


#НАЧАЛО ОПРОСА TG
async def start_poll_tg(message: types.Message, state: FSMContext, flag = None):
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
        #Запросить номер    
        text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = await back_keyboard('Отменить регистрацию')
    if flag:
        text = 'Напишите свой новый номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup =  types.ReplyKeyboardRemove()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


async def tg_number(call: types.CallbackQuery, state: FSMContext):
    ''' Запоминает number и спрашивает Link'''
    if (call.data if type(call) is types.CallbackQuery else call.text) == 'number_y':
        await state.update_data(number=Bloger(f"{call.from_user.id}").get())
        text = '''Ссылка на Telegram канал
*В формате https://t.me/channel'''
    elif (call.data if type(call) is types.CallbackQuery else call.text) == 'number_n':
        await start_poll_tg(call, state, flag = True)
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
        await start_poll_tg(message, state, flag = True)
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
    text ='''Ссылка на статистику 
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
        num=len(sheet.col_values(1)) + 1
        data = await state.get_data()
        data = list(data.values())
        cell_list = sheet.range(f'A{num}:AQ{num}')
        cell_index = [0,1,2,3,4,5,10,12,20,23,25]
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


#НАЧАЛО ОПРОСА DZ
async def start_poll_dz(message: types.Message, state: FSMContext, flag = None):
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
        #Запросить номер    
        text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = await back_keyboard('Отменить регистрацию')
    if flag:
        text = 'Напишите свой новый номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup =  types.ReplyKeyboardRemove()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


async def dz_number(call: types.CallbackQuery, state: FSMContext):
    ''' Запоминает number и спрашивает Link'''
    if (call.data if type(call) is types.CallbackQuery else call.text) == 'number_y':
        await state.update_data(number=Bloger(f"{call.from_user.id}").get())
        text = '''Ссылка на страницу Дзен'''
    elif (call.data if type(call) is types.CallbackQuery else call.text) == 'number_n':
        await start_poll_dz(call, state, flag = True)
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
        await start_poll_dz(message, state, flag = True)
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
    text ='''Ссылка на статистику 
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
        num=len(sheet.col_values(1)) + 1
        data = await state.get_data()
        data = list(data.values())
        cell_list = sheet.range(f'A{num}:AQ{num}')
        cell_index = [0,1,2,3,4,5,6,8,18,20]
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


#НАЧАЛО ОПРОСА ДРУГОЕ
async def start_poll_another(message: types.Message, state: FSMContext, flag = None):
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
        #Запросить номер    
        text = 'Напишите свой номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup = await back_keyboard('Отменить регистрацию')
    if flag:
        text = 'Напишите свой новый номер телефона, привязанный к WhatsApp в формате +7***-***-**-**'
        markup =  types.ReplyKeyboardRemove()
    await message.bot.send_message(message.from_user.id, text, reply_markup=markup)


async def another_number(call: types.CallbackQuery, state: FSMContext):
    ''' Запоминает number и спрашивает Link'''
    if (call.data if type(call) is types.CallbackQuery else call.text) == 'number_y':
        await state.update_data(number=Bloger(f"{call.from_user.id}").get())
        text = '''Ссылка на страницу Вашего блога'''
    elif (call.data if type(call) is types.CallbackQuery else call.text) == 'number_n':
        await start_poll_another(call, state, flag = True)
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
        await start_poll_another(message, state, flag = True)
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
    text ='''Ссылка на статистику 
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
        num=len(sheet.col_values(1)) + 1
        data = await state.get_data()
        data = list(data.values())
        cell_list = sheet.range(f'A{num}:AQ{num}')
        cell_index = [0,1,2,3,4,5,6,8,18,20]
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


#КОНТАКТЫ
async def contacts(call: types.CallbackQuery):
    spreadsheet = client.open_by_key(spreadsheet_era_id)
    sheet = spreadsheet.get_worksheet(4)
    val = sheet.get_all_values()
    text = ''
    for string in val:
        text = text + ((' '.join(string) + '\n') if string != [''] else '\n')
    markup = await back_keyboard('Назад')
    await call.bot.send_message(call.from_user.id, text=text, reply_markup=markup)


#РЕГИСТРАЦИЯ ХЕНДЛЕРОВ
def registration_handlers(dp: Dispatcher):
    #Commands
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(start, text=['старт'])
    dp.register_message_handler(me, text=['me'])
    dp.register_message_handler(start_poll_col, text=['col'])
    #Callbacks
    dp.register_callback_query_handler(start_poll_col, text='colab_start')
    dp.register_callback_query_handler(start_poll_work, text='work')
    dp.register_callback_query_handler(start, text='start')
    dp.register_callback_query_handler(collaboration, text='collaboration')
    dp.register_callback_query_handler(start_poll_barter, text='barter')
    dp.register_callback_query_handler(start_poll_manager, text='manager')
    dp.register_callback_query_handler(start_poll_bloger, text='bloger')
    dp.register_callback_query_handler(start_poll_inst, text='Instagram')
    dp.register_callback_query_handler(start_poll_yt, text='YT')
    dp.register_callback_query_handler(start_poll_vk, text='VK')
    dp.register_callback_query_handler(start_poll_tg, text='TG')
    dp.register_callback_query_handler(start_poll_dz, text='Дзен')
    dp.register_callback_query_handler(start_poll_another, text='Другое')
    dp.register_callback_query_handler(back_start, state='*', text='start')
    #States
        #Хочу работать в ЕРА
    dp.register_message_handler(work_number, state=Work.Number)
    dp.register_message_handler(work_name, state=Work.Name)
    dp.register_message_handler(work_age, state=Work.Age)
    dp.register_message_handler(work_post, state=Work.Post)
    dp.register_message_handler(work_why, state=Work.Why)
    dp.register_message_handler(work_know_from, state=Work.Know_from)
    dp.register_message_handler(work_resume, state=Work.Link_resume)
    dp.register_message_handler(work_case, state=Work.Link_case)
    dp.register_message_handler(work_load, state=Work.Load)
        #Бартер
    dp.register_message_handler(barter_name, state=Barter.Name)
    dp.register_message_handler(barter_number, state=Barter.Number)
    dp.register_message_handler(barter_link, state=Barter.Link)
    dp.register_message_handler(barter_subs, state=Barter.Subs)
    dp.register_message_handler(barter_city, state=Barter.City)
    dp.register_message_handler(barter_city, state=Barter.City)
    dp.register_message_handler(barter_offer, state=Barter.Offer)
        #Менеджер
    dp.register_message_handler(manager_number, state=Manager.Number)
    dp.register_message_handler(manager_name, state=Manager.Name)
    dp.register_message_handler(manager_link, state=Manager.Link)
    dp.register_callback_query_handler(manager_exclusive, state=Manager.Exclusive)
    dp.register_message_handler(manager_exclusive_links, state=Manager.Exclusive_links)
    dp.register_message_handler(manager_q, state=Manager.Q)
        #Сотрудничество
    dp.register_message_handler(colab_name, state=Colab.Name)
    dp.register_message_handler(colab_post, state=Colab.Post)
    dp.register_message_handler(colab_company, state=Colab.Company)
    dp.register_message_handler(colab_reason, state=Colab.Reason)
    dp.register_message_handler(colab_number, state=Colab.Number)
        #Instagram
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
        #YouTube
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
        #VK
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
        #TG
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
        #Dzen
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
        #Another
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
        #Контакты
    dp.register_callback_query_handler(contacts, text_startswith='contacts')

