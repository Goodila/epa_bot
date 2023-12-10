import validators
import phonenumbers



def is_link(url):
    return validators.url(url)


def is_number(number):
    res = phonenumbers.parse(number, "RU")
    if res.country_code == 7 and len(str(res.national_number)) == 10:
        return True
    else:
        return False


url1 = "https://www.abstractapi.com/guides/validate-phone-number-python"
url2 = "https://yandex.ru/search/?clid=2437996&text=яндекс+диск&l10n=ru&lr=146"
url3 = "link"

number1 = "+79781897045"
number2 = "89781897045"
number3 = "+4978-189-70-45"


print(is_link(url1))
print(is_link(url2))
print(is_link(url3))
print(is_number(number1))
print(is_number(number2))
print(is_number(number3))
