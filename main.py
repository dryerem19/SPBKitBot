# -*- coding: utf-8 -*-
"""
:authors: dryerem19
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2019 dryerem19
"""

import configparser
import logging
import os

from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import keyboard as key
from Func import KitFile, Func

from scripts import shedule


class SPBKitHelper:
    """Класс для запуска бота (https://vk.com/spbkit01)
    :param group_token: Токен бота.
    :type group_token: str 
    :param group_id: id бота.
    :type group_id: str
    :param api: версия api, которую использует бот.
    :type api: str
    :param current_path: путь, по которому запущен main.py.
    :type current_path: str
    :param admin_id: id странички адмтинистратора.
    :type admin_id: str
    """ 

    def __init__(self, group_token: str, group_id: str, api: str, current_path: str, admin_id: list) -> None:
        self.token = group_token
        self.id = group_id
        self.api = api
        self.path = current_path
        self.admin = admin_id

        logging.basicConfig(filename="helper.log", encoding="utf-8", level=logging.DEBUG)
        self.logger = logging.getLogger("helper")

    def start(self) -> None:
        """Запустить LongPoll сессию"""

        try:
            vk_session = VkApi(token = self.token, api_version = self.api)
            self.vk = vk_session.get_api()
            self.longpoll = VkBotLongPoll(vk_session, group_id = self.id)
            self.logger.debug("[*] - Session started successfully")
            self.listen()
        except Exception as e:
            self.logger.debug("[*] - Session started error")
            self.logger.debug("[*] - Exception: "+ repr(e))
        
    def listen(self):
        """Слушает LongPoll сервер на предмет сообщений от пользователя"""
        self.logger.debug("[*] - Started listen server...")

        student: str = None
        for self.event in self.longpoll.listen():
            if self.event.type == VkBotEventType.MESSAGE_NEW and self.event.from_user:
                from_id: str = dict(self.event.message).get("from_id")
                message: str = dict(self.event.message).get("text").lower()

                self.logger.debug(f"[*] - New message from id: {from_id}")
                self.logger.debug(f"[*] - Message: {message}")

                if message == "start" or message == "старт":
                    self.send_message("test message", key.main_page())
                    self.logger.debug(f"[*] - The bot sent the main keyboard to the user: {from_id}")

                if message == "расписание занятий":
                    self.send_message("Отлично! А теперь выбирай день недели :)", key.shedule_page())
                    self.logger.debug(f"[*] - The bot sent the shedule keyboard to the user: {from_id}")

                if message == "понедельник" or message == "вторник" or message == "среда" \
                    or message == "четверг" or message == "пятница" or message == "суббота":
                    self.send_message(shedule.get_shedule(message), key.shedule_page())
                    self.logger.debug(f"[*] - The bot sent the shedule on a {message} to the user: {from_id}")

                if message == "назад":
                    self.send_message("Вы снова на главной, что желаете?", key.main_page())
                    self.logger.debug(f"[*] - The bot sent the main page to the user: {from_id}")
                
                if message == "домашнее задание":
                    self.send_message("Ой, этот раздел находится в доработке, приходи позже", key.main_page())
                    self.logger.debug(f"[*] - The user {from_id} tried to access the homework section")

                if message == "полезные материалы":
                    self.send_message("О, здесь достаточно полезная информация :)", key.materials_page())
                    self.logger.debug(f"[*] - The bot sent the materials page to the user: {from_id}")

                if message == "ссылки на сайты":
                    self.send_message(Func.get_urls(self.path), key.materials_page())
                    self.logger.debug(f"[*] - The bot sent the url to the user: {from_id}")

                if message == "e-mail преподавателей":
                    self.send_message(Func.get_email(self.path), key.materials_page())
                    self.logger.debug(f"[*] - The bot sent the e-mail to the user: {from_id}")

                if message == "админ":
                    if from_id in self.admin:
                        self.send_message("Хорошего дня!", key.admin_page())
                        self.logger.debug(f"[*] - The admin {from_id} tried to access the admin section")
                    else:
                        self.send_message("Ээээй, прохода нет", key.main_page())
                        self.logger.debug(f"[*] - The user {from_id} tried to access the admin section")

                if message == "добавить запись":
                    if from_id in self.admin:
                        self.send_message("Первая партия", key.list_add_1())
                        self.send_message("Вторая партия", key.list_add_2())
                        self.send_message("Третья партия", key.list_add_3())
                        self.logger.debug(f"[*] - The admin {from_id} tried to access the add_record section")
                    else:
                        self.send_message("Ээээй, прохода нет", key.main_page())
                        self.logger.debug(f"[*] - The user {from_id} tried to access the add_record section")

                if message == "одна пара" or message == "две пары" or message == "три пары" or message == "четыре пары":
                    if student != None:
                        self.send_message(Func.add_record_in_table(student, self.path, message), key.main_page())
                        self.logger.debug("[*] - Success writing to table")
                    else:
                        self.send_message("Не удалось получить имя студента", key.count_lessons())
                        self.logger.debug("[*] - Failure trying to get student name, student is None")

            elif self.event.type == VkBotEventType.MESSAGE_EVENT:
                student = self.event.obj.payload.get("type")
                self.send_callback_message("Сколько пропустил студент?", key.count_lessons())
                self.logger.debug(f"[*] - The bot sent the count_lessons page to the admin")

                      
    def send_message(self, message: str, keyboard: str) -> None:
        """Отправить сообщение пользователю.

        :param message: Сообщение, которое будет отправлено.
        :type message: str
        :param keyboard: клавиатура.
        :type message: str
        """

        self.vk.messages.send(
            user_id=self.event.obj.message["from_id"],
            random_id=get_random_id(),
            peer_id=self.event.obj.message["from_id"],
            keyboard=keyboard,
            message=message)   

    def send_callback_message(self, message: str, keyboard: str) -> None:
        """Отправить сообщение пользователю через callback кнопку.

        :param message: Сообщение, которое будет отправлено.
        :type message: str
        :param keyboard: клавиатура.
        :type message: str
        """
        self.vk.messages.send(
            user_id=self.event.obj.user_id,
            random_id=get_random_id(),
            peer_id=self.event.obj.peer_id,
            keyboard=keyboard,
            message=message)              


def main():
    """
    Точка входа в приложение
    """

    print("[*] - Bot Running...")
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Читаем конфигурационный файл
    config = configparser.ConfigParser()
    config.read("auth.ini")

    # Аутентификационные данные
    token = config.get("Auth", "token")
    ids = config.get("Auth", "id")
    api = config.get("Auth", "api")

    # ID Администраторов
    admin_id = []
    with open(os.path.join(current_path, "admin/admin.txt"), "r", encoding="utf8") as admin:
        for line in admin: 
            admin_id.append(int(line))

    # Запускаем бота
    bot = SPBKitHelper(token, ids, api, current_path, admin_id)
    bot.start()

    print("[*] - Bot stopped")

if __name__ == "__main__":
    main()



