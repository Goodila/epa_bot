from aiogram.dispatcher.filters.state import StatesGroup, State


QUESTIONS = [
    "ФИО",
    "Ваш возраст",
    "Ваш телефон в формате +79995557700",
    "Город",
    "Род деятельности",
    "Ссылки на Ваши социальные сети (количество не ограничено)",
    "Общее количество подписчиков",
    "Почему вы хотите посетить межрегиональный конгресс Новых Медиа?",
    "Откуда вы о нем узнали?",
    "Хотели бы вы стать резидентом АНО \"Ресурсный Центр Новых Медиа?\"",
    "Чем вы можете быть полезны АНО \"Ресурсному Центру Новых Медиа?\"",
    "Что бы Вы хотели получить от мероприятия и «Ресурсного Центра Новых Медиа»",
    "Благодарю Вас за ответы! Можете оставить ваши предложения, пожелания или вопросы, нам важно мнение каждого."
]


class Work(StatesGroup):
    Number = State()
    Name = State()
    Age = State()
    Post = State()
    Why = State()
    Know_from = State()
    Link_resume = State()
    Link_case = State()
    Load = State()


class Barter(StatesGroup):
    Name = State()
    Number = State()
    Link = State()
    Subs = State()
    City = State()


class Manager(StatesGroup):
    Number = State()
    Name = State()
    Link = State()
    Q = State()
    

class Colab(StatesGroup):
    Name = State()
    Post = State()
    Company = State()
    Reason = State()
    Number = State()
    

class Instagram(StatesGroup):
    Number = State()
    Wait = State()
    Link = State()
    Topic = State()
    Topic_another = State()
    Subs = State()
    Description = State()
    City = State()
    Stories = State()
    Stories_scope = State()
    Reels = State()
    Reels_scope = State()
    Statistic = State()


class YT(StatesGroup):
    Number = State()
    Wait = State()
    Link = State()
    Topic = State()
    Topic_another = State()
    Subs = State()
    Description = State()
    Country = State()
    Shorts = State()
    Shorts_views = State()
    Video = State()
    Video_views = State()
    Statistic = State()


class VK(StatesGroup):
    Number = State()
    Wait = State()
    Link = State()
    Topic = State()
    Topic_another = State()
    Subs = State()
    Description = State()
    Country = State()
    Post = State()
    Post_views = State()
    Clip = State()
    Clip_views = State()
    Statistic = State()
    

class TG(StatesGroup):
    Number = State()
    Wait = State()
    Link = State()
    Topic = State()
    Topic_another = State()
    Subs = State()
    Post_views = State()
    Post = State()
    Country = State()
    Description = State()
    Statistic = State()
    

    
class DZ(StatesGroup):
    Number = State()
    Wait = State()
    Link = State()
    Topic = State()
    Topic_another = State()
    Subs = State()
    Post_views = State()
    Post = State()
    Description = State()
    Statistic = State()
    