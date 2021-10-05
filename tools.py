import requests
from typing import Union
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
           'Accept': 'application/json, text/javascript, */*; q=0.01'}

url_replacements: str = 'http://spbcoit.ru:30001/replacements/api/fetch-rep?ts=1633371722763'
url_shedule = "http://www.spbkit.edu.ru/index.php?option=com_timetable&Itemid=82#gruppi-19"


def get_shedule(day: str) -> str:
    """get shedule.
    
    :param code: code day.
    :type day: int
    """

    if type(day) is not str:
        raise ValueError('The day must be a str')

    s = f"📚 Расписание на {day} \n\n"

    code: int = 0
    if day == "понедельник":
        code = 0
    if day == "вторник":
        code = 1
    if day == "среда":
        s = "📚 Расписание на среду \n\n"
        code = 2
    if day == "четверг":
        code = 3
    if day == "пятница":
        s = "📚 Расписание на пятницу \n\n"
        code = 4
    if day == "суббота":
        s = "📚 Расписание на субботу \n\n"
        code = 5

    page = requests.get(url_shedule, headers=headers)
    encoding = page.encoding if "charset" in page.headers.get("content-type", "").lower() else None
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding=encoding)

    group = soup.find(id="gruppi-19") # get need group
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
                k += 1
    return s


def get_replacements(group: str = '01') -> Union[str, None]:
    """Returns a formatted string - a list of academic subjects 
    that have been replaced by other subjects for the specified group.
    return None if replacements is not find.
    
    :param group: group number for which replacements should be obtained.
    :type group: str.
    :return: str or None if replacements is not find
    """

    if type(group) is not str:
        raise ValueError('The type must be a str')
    
    page = requests.get(url_replacements, headers=headers)
    encoding = page.encoding if "charset" in page.headers.get("content-type", "").lower() else None
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding=encoding)

    table: list = []
    find: bool = False
    tr = soup.find_all('tr')
    for item_tr in tr:
        row: list = []
        if item_tr.find('td').attrs['class'][0] == 'section' and item_tr.text == group:
            find = True #  replacements found
            continue

        if find:
            if item_tr.find('td').attrs['class'][0] != 'content':
                break
            else:
                #  add each column in the row at row list
                for item_td in item_tr:
                    row.append(item_td.text)

        if row:
            table.append(row) #  if row is not empty - put row in table

    if find is False: #  replacements is not find
        return 'Замен в расписании не найдено!'

    result: str = ''
    header: list = table[0] # first row this is table header 
    for row in table:
        if row is header:
            continue
        
        for i in range(len(row)):
            result += f'{header[i]}: {row[i]}\n'
        result += '\n'

    return result


if __name__ == '__main__':
    """TESTS"""

    print(get_replacements()) #  None [05.10.2021]
    print(get_replacements('205')) # return result [05.10.2021]