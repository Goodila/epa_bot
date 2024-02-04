from aiogram.dispatcher.filters.state import StatesGroup, State

class SocMedia(StatesGroup):
    Name = State()
    SM = State()
    Link = State()
    Subs = State()
    City = State()
    Geo1 = State()
    Geo2 = State()
    Topic = State()
    Topic_another = State()
    Description = State()


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
    Offer = State()
    City = State()


class Manager(StatesGroup):
    Number = State()
    Name = State()
    Link = State()
    Exclusive = State()
    Exclusive_links = State()
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
    Question_shotrs = State()
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
    Question_shotrs = State()
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


class Another(StatesGroup):
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
    