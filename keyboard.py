# -*- coding: utf-8 -*-
"""
:authors: dryerem19
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2019 dryerem19
"""

from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboard(object):
    """В этом классе описаны клавиатуры бота"""

    @staticmethod
    def main_page():
        """Главная клавиатура"""

        keyboard = VkKeyboard(one_time=False, inline=False)

        keyboard.add_button("Расписание занятий", VkKeyboardColor.PRIMARY, {"type": "btn_shedule"})
        keyboard.add_line()
        keyboard.add_button("Домашнее задание", VkKeyboardColor.PRIMARY, {"type": "btn_homework"})
        keyboard.add_button("Полезные материалы", VkKeyboardColor.POSITIVE, {"type": "btn_materials"})
        keyboard.add_line()
        keyboard.add_openlink_button("Посещаемость", "https://docs.google.com/spreadsheets/d/1LxPQZ8VwG3Acu-TG8Tclr4POjnXcXlhVa2jsa3LP_Go/edit?usp=sharing")
        keyboard.add_openlink_button("Замены в расписании", "http://app.fxnode.ru:30001/replacements/view.html")
        keyboard.add_line()
        keyboard.add_button("Админ", VkKeyboardColor.PRIMARY, {"type": "btn_admin"})

        return keyboard.get_keyboard()

    @staticmethod
    def shedule_page():
        """Клавиатура с расписанием"""

        keyboard = VkKeyboard(one_time=False, inline=False)

        keyboard.add_button("Понедельник", VkKeyboardColor.SECONDARY, {"type": "btn_monday_sh"})
        keyboard.add_button("Вторник", VkKeyboardColor.SECONDARY, {"type": "btn_tuesday_sh"})
        keyboard.add_line()
        keyboard.add_button("Среда", VkKeyboardColor.SECONDARY, {"type": "btn_wednesday_sh"})
        keyboard.add_button("Четверг", VkKeyboardColor.SECONDARY, {"type": "btn_thursday_sh"})
        keyboard.add_line()
        keyboard.add_button("Пятница", VkKeyboardColor.SECONDARY, {"type": "btn_friday_sh"})
        keyboard.add_button("Суббота", VkKeyboardColor.SECONDARY, {"type": "btn_saturday_sh"})
        keyboard.add_line()
        keyboard.add_button("Назад", VkKeyboardColor.POSITIVE, {"type": "btn_back_sh"})

        return keyboard.get_keyboard()

    @staticmethod
    def materials_page():
        """Клавиатура с полезными материалами"""

        keyboard = VkKeyboard(one_time=False, inline=False)

        keyboard.add_openlink_button("Записи лекций", "https://vk.com/videos-199418622")
        keyboard.add_line()
        keyboard.add_button("Ссылки на сайты", VkKeyboardColor.SECONDARY, {"type": "url_mat"})
        keyboard.add_line()
        keyboard.add_button("E-mail преподавателей", VkKeyboardColor.SECONDARY, {"type": "mail_mat"})
        keyboard.add_line()
        keyboard.add_button("Назад", VkKeyboardColor.POSITIVE, {"type": "btn_back_mat"})

        return keyboard.get_keyboard()  

    @staticmethod
    def homework_page():
        """Клавиатура с домашним заданием"""

        keyboard = VkKeyboard(one_time=False, inline=False)

        keyboard.add_button("Понедельник", VkKeyboardColor.SECONDARY, {"type": "btn_monday_hm"})
        keyboard.add_button("Вторник", VkKeyboardColor.SECONDARY, {"type": "btn_tuesday_hm"})
        keyboard.add_line()
        keyboard.add_button("Среда", VkKeyboardColor.SECONDARY, {"type": "btn_wednesday_hm"})
        keyboard.add_button("Четверг", VkKeyboardColor.SECONDARY, {"type": "btn_thursday_hm"})
        keyboard.add_line()
        keyboard.add_button("Пятница", VkKeyboardColor.SECONDARY, {"type": "btn_friday_hm"})
        keyboard.add_button("Суббота", VkKeyboardColor.SECONDARY, {"type": "btn_saturday_hm"})
        keyboard.add_line()
        keyboard.add_button("Назад", VkKeyboardColor.POSITIVE, {"type": "btn_back_hm"})

        return keyboard.get_keyboard()

    @staticmethod
    def admin_page():
        """Клавиатура для отметок в табеле прихода"""

        keyboard = VkKeyboard(one_time=False, inline=False)

        keyboard.add_button("Добавить запись", VkKeyboardColor.PRIMARY, {"type": "btn_add"})
        keyboard.add_line()
        keyboard.add_button("Назад", VkKeyboardColor.POSITIVE, {"type": "btn_back"})

        return keyboard.get_keyboard()

    @staticmethod
    def list_add_1():
        """Список учеников группы"""
        keyboard = VkKeyboard(one_time=False, inline=True)

        keyboard.add_callback_button("Аветисян", VkKeyboardColor.SECONDARY, {"type": "avetysyan"})
        keyboard.add_callback_button("Борзухин", VkKeyboardColor.SECONDARY, {"type": "borzuxin"})
        keyboard.add_callback_button("Генхель", VkKeyboardColor.SECONDARY, {"type": "genhel"})
        keyboard.add_line()
        
        keyboard.add_callback_button("Дятлова", VkKeyboardColor.SECONDARY, {"type": "dyatlova"})
        keyboard.add_callback_button("Евдокимов", VkKeyboardColor.SECONDARY, {"type": "evdokimov"})
        keyboard.add_callback_button("Егоров", VkKeyboardColor.SECONDARY, {"type": "egorov"})
        keyboard.add_line()

        
        keyboard.add_callback_button("Еременко", VkKeyboardColor.SECONDARY, {"type": "eremenko"})
        keyboard.add_callback_button("Игнатьева", VkKeyboardColor.SECONDARY, {"type": "ignatieva"})
        keyboard.add_callback_button("Каданчик", VkKeyboardColor.SECONDARY, {"type": "kadanchik"})
        keyboard.add_line()
        keyboard.add_callback_button("Корнинский", VkKeyboardColor.SECONDARY, {"type": "korninsky"})

        return keyboard.get_keyboard()

    @staticmethod
    def list_add_2():
        """Список учеников группы"""

        keyboard = VkKeyboard(one_time=False, inline=True)

        keyboard.add_callback_button("Макаров", VkKeyboardColor.SECONDARY, {"type": "makarov"})
        keyboard.add_callback_button("Маматов", VkKeyboardColor.SECONDARY, {"type": "mamatov"})
        keyboard.add_callback_button("Могучева", VkKeyboardColor.SECONDARY, {"type": "mogucheva"})
        keyboard.add_line()

        keyboard.add_callback_button("Ооржак", VkKeyboardColor.SECONDARY, {"type": "oorzak"})
        keyboard.add_callback_button("Отмахова", VkKeyboardColor.SECONDARY, {"type": "otmahova"})
        keyboard.add_callback_button("Плиев", VkKeyboardColor.SECONDARY, {"type": "pliev"})
        keyboard.add_line()
    
        keyboard.add_callback_button("Реута", VkKeyboardColor.SECONDARY, {"type": "reuta"})
        keyboard.add_callback_button("Семкив", VkKeyboardColor.SECONDARY, {"type": "semkiv"})
        keyboard.add_callback_button("Силкина", VkKeyboardColor.SECONDARY, {"type": "silkina"})
        keyboard.add_callback_button("Смельчакова", VkKeyboardColor.SECONDARY, {"type": "smelchakova"})

        return keyboard.get_keyboard()

    @staticmethod
    def list_add_3():
        """Список учеников группы"""

        keyboard = VkKeyboard(one_time=False, inline=True)


        keyboard.add_callback_button("Соловьев", VkKeyboardColor.SECONDARY, {"type": "soloviev"})
        keyboard.add_callback_button("Тебеньков", VkKeyboardColor.SECONDARY, {"type": "tebenkov"})
        keyboard.add_callback_button("Хамидуллин", VkKeyboardColor.SECONDARY, {"type": "hamidulin"})
        keyboard.add_line()

        keyboard.add_callback_button("Ховрат", VkKeyboardColor.SECONDARY, {"type": "hovrat"})
        keyboard.add_callback_button("Черняков", VkKeyboardColor.SECONDARY, {"type": "chernyakov"})
        keyboard.add_callback_button("Чикинев", VkKeyboardColor.SECONDARY, {"type": "chykynev"})
        keyboard.add_line()
    
        keyboard.add_callback_button("Шубарина", VkKeyboardColor.SECONDARY, {"type": "shubarina"})
        keyboard.add_callback_button("Юнусов", VkKeyboardColor.SECONDARY, {"type": "unusov"})

        return keyboard.get_keyboard()

    @staticmethod
    def list_delete_1():
        """Список учеников группы"""
        keyboard = VkKeyboard(one_time=False, inline=True)

        keyboard.add_callback_button("Аветисян", VkKeyboardColor.SECONDARY, {"type": "avetysyan_del"})
        keyboard.add_callback_button("Борзухин", VkKeyboardColor.SECONDARY, {"type": "borzuxin_del"})
        keyboard.add_callback_button("Генхель", VkKeyboardColor.SECONDARY, {"type": "genhel_del"})
        keyboard.add_line()
        
        keyboard.add_callback_button("Дятлова", VkKeyboardColor.SECONDARY, {"type": "dyatlova_del"})
        keyboard.add_callback_button("Евдокимов", VkKeyboardColor.SECONDARY, {"type": "evdokimov_del"})
        keyboard.add_callback_button("Егоров", VkKeyboardColor.SECONDARY, {"type": "egorov_del"})
        keyboard.add_line()

        
        keyboard.add_callback_button("Еременко", VkKeyboardColor.SECONDARY, {"type": "eremenko_del"})
        keyboard.add_callback_button("Игнатьева", VkKeyboardColor.SECONDARY, {"type": "ignatieva_del"})
        keyboard.add_callback_button("Каданчик", VkKeyboardColor.SECONDARY, {"type": "kadanchik_del"})
        keyboard.add_line()
        keyboard.add_callback_button("Корнинский", VkKeyboardColor.SECONDARY, {"type": "korninsky_del"})

        return keyboard.get_keyboard()

    @staticmethod
    def list_delete_2():
        """Список учеников группы"""

        keyboard = VkKeyboard(one_time=False, inline=True)

        keyboard.add_callback_button("Макаров", VkKeyboardColor.SECONDARY, {"type": "makarov_del"})
        keyboard.add_callback_button("Маматов", VkKeyboardColor.SECONDARY, {"type": "mamatov_del"})
        keyboard.add_callback_button("Могучева", VkKeyboardColor.SECONDARY, {"type": "mogucheva_del"})
        keyboard.add_line()

        keyboard.add_callback_button("Ооржак", VkKeyboardColor.SECONDARY, {"type": "oorzak_del"})
        keyboard.add_callback_button("Отмахова", VkKeyboardColor.SECONDARY, {"type": "otmahova_del"})
        keyboard.add_callback_button("Плиев", VkKeyboardColor.SECONDARY, {"type": "pliev_del"})
        keyboard.add_line()
    
        keyboard.add_callback_button("Реута", VkKeyboardColor.SECONDARY, {"type": "reuta_del"})
        keyboard.add_callback_button("Семкив", VkKeyboardColor.SECONDARY, {"type": "semkiv_del"})
        keyboard.add_callback_button("Силкина", VkKeyboardColor.SECONDARY, {"type": "silkina_del"})
        keyboard.add_callback_button("Смельчакова", VkKeyboardColor.SECONDARY, {"type": "smelchakova_del"})

        return keyboard.get_keyboard()

    @staticmethod
    def list_delete_3():
        """Список учеников группы"""

        keyboard = VkKeyboard(one_time=False, inline=True)

        keyboard.add_callback_button("Соловьев", VkKeyboardColor.SECONDARY, {"type": "soloviev_del"})
        keyboard.add_callback_button("Тебеньков", VkKeyboardColor.SECONDARY, {"type": "tebenkov_del"})
        keyboard.add_callback_button("Хамидуллин", VkKeyboardColor.SECONDARY, {"type": "hamidulin_del"})
        keyboard.add_line()

        keyboard.add_callback_button("Ховрат", VkKeyboardColor.SECONDARY, {"type": "hovrat_del"})
        keyboard.add_callback_button("Черняков", VkKeyboardColor.SECONDARY, {"type": "chernyakov_del"})
        keyboard.add_callback_button("Чикинев", VkKeyboardColor.SECONDARY, {"type": "chykynev_del"})
        keyboard.add_line()
    
        keyboard.add_callback_button("Шубарина", VkKeyboardColor.SECONDARY, {"type": "shubarina_del"})
        keyboard.add_callback_button("Юнусов", VkKeyboardColor.SECONDARY, {"type": "unusov_del"})

        return keyboard.get_keyboard()

    @staticmethod
    def count_lessons():
        """Какая пара."""

        keyboard = VkKeyboard(one_time=False, inline=False)

        keyboard.add_button("Одна пара", VkKeyboardColor.SECONDARY, {"type": "less_one"})
        keyboard.add_line()
        keyboard.add_button("Две пары", VkKeyboardColor.SECONDARY, {"type": "less_two"})
        keyboard.add_line()
        keyboard.add_button("Три пары", VkKeyboardColor.SECONDARY, {"type": "less_three"})
        keyboard.add_line()
        keyboard.add_button("Главная", VkKeyboardColor.PRIMARY, {"type": "btn_back"})

        return keyboard.get_keyboard()