import json
from dataclasses import dataclass
from aiogram.utils.markdown import hlink
from aiogram.dispatcher import FSMContext
from aiogram import types
import validators
import phonenumbers

@dataclass
class Config:
    token: str
    admins: list
    bot_id: int



def get_config(flag=None):
    if flag:
        config = json.load(open("config.txt", "r",encoding='utf-8'))
        return config['TOPICS']
    else:
        config = json.load(open("config.txt", "r", encoding='utf-8'))
        return Config(token=config['TOKEN'], admins=config['ADMIN_ID'], bot_id=config['BOT_ID'])



    
class Bloger:
    def __init__(self, id: str):
        self.id = id
    
    def check(self):
        with open('blogers.json', 'r+') as f:
            blogers = json.load(f)
            print(f"Проверка наличия id {self.id} в базе")
            return self.id in blogers.keys()

    def record(self, number: str):
        with open('blogers.json', 'r') as f:
            blogers = json.load(f)
            blogers[self.id] = number
        with open('blogers.json', 'w') as f:
            json.dump(blogers, f, indent=4)
        print(f"Запись id {self.id} в базу - успешно")

    def get(self):
        with open('blogers.json', 'r') as f:
            blogers = json.load(f)
            print(f"Получение номера по id {self.id} из базы")
            return blogers[self.id]
        

def is_link(url):
    return validators.url(url)


def is_number(number):
    try:
        res = phonenumbers.parse(number, "RU")
    except:
        return False
    if res.country_code == 7 and len(str(res.national_number)) == 10:
        return True
    else:
        return False



        
# async def events_fomer(events_data: list):
#     '''формирует список мероприятий в текст'''
#     res = ''
#     for event in events_data:
#         text = f'''{event[0]}. {event[1]}
# Тема: {event[2]}
# Место: {event[3]}
# Время: {event[4]}
# Дата: {event[5]}
# Программа: {event[6]}

# '''     
#         res += text
#     res += 'Чтобы начать регистрацию на мероприятие, нажмите на него здесь 👇'
#     return res 