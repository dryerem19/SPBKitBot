import requests
from bs4 import BeautifulSoup

url = "http://www.spbkit.edu.ru/index.php?option=com_timetable&Itemid=82#gruppi-11"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
           'Accept': 'application/json, text/javascript, */*; q=0.01'}

def get_shedule(day: str):
    """get shedule.
    
    :param code: code day.
    :type day: int
    """
    s = f"📚 Расписание на {day} \n\n"

    code: int = 0
    if day == "понедельник":
        code = 0
    if day == "вторник":
        code = 1
    if day == "среда":
        code = 2
    if day == "четверг":
        code = 3
    if day == "пятница":
        code = 4
    if day == "суббота":
        code = 5

    page = requests.get(url, headers=headers)
    encoding = page.encoding if "charset" in page.headers.get("content-type", "").lower() else None
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding=encoding)

    group = soup.find(id="gruppi-11") # get need group
    days_tabs = group.find_all("ul", class_="ui-tabs-nav") # get all days tabs

    # get url day
    days = []
    for i in days_tabs[0].find_all("a", href=True):
        days.append(i["href"].replace("#", ""))

    # get shedule
    day_shedule = group.find(id=days[code])

    k = 1 
    for i, time in enumerate(day_shedule.find_all("i")):
        for j, lesson in enumerate(day_shedule.find_all("b")):
            if i % 2 != 0 and j == i and lesson.text != "":
                s += f' - {time.text}\n\n'
            elif j == i and i % 2 == 0:
                if lesson.text != "":
                    s += f'{str(k)}. {lesson.text} \n - {time.text}\n'
                else: s += f'{str(k)}. пары нет\n\n'
                k += 1
    return s