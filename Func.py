# -*- coding: utf-8 -*-
"""
:authors: dryerem19
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2019 dryerem19
"""

import os
import json
import datetime

import pygsheets

class KitFile:
    """Возможные типы пути"""

    #: Расписание занятий
    SHEDULE = "json_files/shedule.json"

    #: Список e-mail
    EMAIL = "json_files/email.json"

    #: Список url
    URL = "json_files/urls.json"

    #: Service file 
    SERVICE = "json_files/spbkit-bot-key.json"

class Lastname:
    """Возможные фамилии"""

    AVETYSYAN = "C7"
    BORZUXIN = "C8"
    GENXEL = "C9"
    DYATLOVA = "C10"
    EVDOKIMOV = "C11"
    EGOROV = "C12"
    EREMENKO = "C13"
    IGNATIEVA = "C14"
    KADANCHIK = "C15"
    KORNINSKY = "C16"
    MAKAROV = "C17"
    MAMATOV = "C18"
    MOGUCHEVA = "C19"
    OORZAK = "C20"
    OTMAHOVA = "C21"
    PLIEV = "C22"
    REUTA = "C23"
    SEMKIV = "C24"
    SILKINA = "C25"
    SMELCHAKOVA = "C26"
    SOLOVIEV = "C27"
    TEBENKOV = "C28"
    HAMIDULIN = "C29"
    HOVRAT = "C30"
    CHERNYAKOV = "C31"
    CHIKINEV = "C32"
    SHUBARINA = "C33"

class Func(object):
    """Этот класс содержит в себе методы приложения"""

    @staticmethod
    def get_email(path: str, file=KitFile.EMAIL) -> str:
        """Получает e-mail адреса преподаватлей.

        :param path: путь текущей директории.
        :type path: str 
        """

        with open(os.path.join(path, file), "r", encoding="utf-8-sig") as email:
            data = json.load(email)   

        string = "E-mail преподавателей\n\n"
        for i in data["teachers"]:
            try:
                string += "👨‍🏫 " + data["teachers"][i]["name"] + "\n" + data["teachers"][i]["mail"] + "\n\n"
            except TypeError:
                continue

        return string


    @staticmethod
    def get_urls(path: str, file=KitFile.URL) -> str:
        """Получает все полезные ссылки.

        :param path: путь текущей директории.
        :type path: str 
        """

        with open(os.path.join(path, file), "r", encoding="utf-8") as url:
            data = json.load(url)   

        string = "Полезные ссылки\n\n"
        for i in data["urls"]:
            try:
                string += "👨‍🏫 " + data["urls"][i]["type"] + "\n" + data["urls"][i]["url"] + "\n\n"
            except TypeError:
                continue

        return string

    @staticmethod
    def get_homework(day: str, path) -> str:
        """Получает домашнее задание.
        
        :param day: День, на который следует получить домашнее задание.
        :type day: str
        :param path: текущая директория.
        :type path: str
        """

        key = "https://docs.google.com/spreadsheets/d/1axnzRILcQ06aqrzZkzWJ7etMQpkuoXiFsSzPYZk9Rps/edit?usp=sharing"

        # authorize
        gc = pygsheets.authorize(service_file=os.path.join(path, KitFile.SERVICE))
        sheets = gc.open_by_url(key)

        # get records
        worksheet = sheets.worksheet()

        # returns strings
        found = "📘 Домашнее задание на "

        records = "" 
        worksheet = ""

        b = 0

        if day == "monday":
            found += "понедельник\n\n"
            worksheet = sheets.worksheet(property='index', value=0)
            records = worksheet.get_all_records(majdim='COLUMN')
            b = 6

        elif day == "tuesday":
            found += "вторник\n\n"
            worksheet = sheets.worksheet(property='index', value=1)
            records = worksheet.get_all_records(majdim='COLUMN')
            b = 4

        elif day == "wednesday":
            found += "среду\n\n"
            worksheet = sheets.worksheet(property='index', value=2)
            records = worksheet.get_all_records(majdim='COLUMN')
            b = 5

        elif day == "thursday":
            found += "четверг\n\n"
            worksheet = sheets.worksheet(property='index', value=3)
            records = worksheet.get_all_records(majdim='COLUMN')
            b = 5

        elif day == "friday":
            found += "пятницу\n\n"
            worksheet = sheets.worksheet(property='index', value=4)
            records = worksheet.get_all_records(majdim='COLUMN')
            b = 6

        elif day == "saturday":
            found += "субботу\n\n"
            worksheet = sheets.worksheet(property='index', value=5)
            records = worksheet.get_all_records(majdim='COLUMN')
            b = 4

        for record in range(2, b):
            cell_a = worksheet.get_value("A" + str(record))
            cell_b = worksheet.get_value("B" + str(record))
            cell_c = worksheet.get_value("C" + str(record))
            if cell_b == '':
                cell_b = "отсутствует запись в таблице ☹️"

            found += cell_a + " - " + cell_b + "\nСрок сдачи: " + cell_c + "\n\n"

        return found

    @staticmethod
    def add_record_in_table(lastname: str, path: str, para: int) -> str:
        """Добавляет запись в табель.
           По умолчанию - максимальное кол-во пар - para
        
        :param lastname: Фамилия ученика.
        :type lastname: str
        :param path: текущая директория.
        :type path: str
        """

        para *= 2

        gc = pygsheets.authorize(service_file=os.path.join(path, KitFile.SERVICE))
        sheets = gc.open_by_url("https://docs.google.com/spreadsheets/d/1LxPQZ8VwG3Acu-TG8Tclr4POjnXcXlhVa2jsa3LP_Go/edit?usp=sharing")

        worksheet = sheets.worksheet(property='index', value=6)

        with open("admin/config.json", "r", encoding="utf8") as config:
            config = json.load(config) # load cell position
            
            h = config[day()]

        if lastname == "avetysyan":
            cell = Lastname.AVETYSYAN.replace(Lastname.AVETYSYAN[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "borzuxin":
            cell = Lastname.BORZUXIN.replace(Lastname.BORZUXIN[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "genhel":
            cell = Lastname.GENXEL.replace(Lastname.GENXEL[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "dyatlova":
            cell = Lastname.DYATLOVA.replace(Lastname.DYATLOVA[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "evdokimov":
            cell = Lastname.EVDOKIMOV.replace(Lastname.EVDOKIMOV[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "egorov":
            cell = Lastname.EGOROV.replace(Lastname.EGOROV[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "eremenko":
            cell = Lastname.EREMENKO.replace(Lastname.EREMENKO[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "ignatieva":
            cell = Lastname.IGNATIEVA.replace(Lastname.IGNATIEVA[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "kadanchik":
            cell = Lastname.KADANCHIK.replace(Lastname.KADANCHIK[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "korninsky":
            cell = Lastname.KORNINSKY.replace(Lastname.KORNINSKY[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "makarov":
            cell = Lastname.MAKAROV.replace(Lastname.MAKAROV[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "mamatov":
            cell = Lastname.MAMATOV.replace(Lastname.MAMATOV[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "mogucheva":
            cell = Lastname.MOGUCHEVA.replace(Lastname.MOGUCHEVA[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "oorzak":
            cell = Lastname.OORZAK.replace(Lastname.OORZAK[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "otmahova":
            cell = Lastname.OTMAHOVA.replace(Lastname.OTMAHOVA[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "pliev":
            cell = Lastname.PLIEV.replace(Lastname.PLIEV[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "reuta":
            cell = Lastname.REUTA.replace(Lastname.REUTA[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "semkiv":
            cell = Lastname.SEMKIV.replace(Lastname.SEMKIV[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "silkina":
            cell = Lastname.SILKINA.replace(Lastname.SILKINA[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "smelchakova":
            cell = Lastname.SMELCHAKOVA.replace(Lastname.SMELCHAKOVA[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "soloviev":
            cell = Lastname.SOLOVIEV.replace(Lastname.SOLOVIEV[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "tebenkov":
            cell = Lastname.TEBENKOV.replace(Lastname.TEBENKOV[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "hamidulin":
            cell = Lastname.HAMIDULIN.replace(Lastname.HAMIDULIN[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "hovrat":
            cell = Lastname.HOVRAT.replace(Lastname.HOVRAT[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "chernyakov":
            cell = Lastname.CHERNYAKOV.replace(Lastname.CHERNYAKOV[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "chykynev":
            cell = Lastname.CHIKINEV.replace(Lastname.CHIKINEV[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "shubarina":
            cell = Lastname.SHUBARINA.replace(Lastname.SHUBARINA[0], h)
            worksheet.update_value(cell, para)

        elif lastname == "unusov":
            cell = Lastname.UNUSOV.replace(Lastname.UNUSOV[0], h)
            worksheet.update_value(cell, para)

        return "Запись успешно добавлена в таблицу"

    @staticmethod
    def get_shedule_canteen(day: str) -> str:
        """Возвращает расписание посещения столовой.
        
        :param day: День, на который следует вернуть расписание.
        :type lastname: str
        """
        pass

    @staticmethod
    def weekday() -> int:
        """Возвращает день недели.
        0 - Понедельник
        6 - Воскресенье
        """

        return datetime.datetime.today().weekday()

def day() -> str:
    """Возвращает сегодняшнее число.

    :return type: str
    """

    return str(datetime.datetime.now().day)