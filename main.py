# -*- coding: utf-8 -*-
"""
:authors: dryerem19
:license: Apache License, Version 2.0, see LICENSE file
:copyright: (c) 2019 dryerem19
"""

import configparser
import traceback
import logging
import requests
import threading
import json
import os
import sys
import time
import smtplib

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

from vk_api import VkApi
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


from SMTPHandler import BufferingSMTPHandler
from keyboard import Keyboard
from Func import KitFile, Func

from scripts import shedule


class SPBKitHelper(object):
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

        # Создание логгера
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Создание обработчика
        handler = logging.FileHandler("SPBKitBot.log")
        handler.setLevel(logging.DEBUG)

        # Создание форматора
        formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

        # Добавляем форматтер в обработчик
        handler.setFormatter(formatter)

        # Добаляем обработчик в логгер
        self.logger.addHandler(handler)

        with open("admin/admin_smtp.json", "r") as smtp:
            smtp = json.load(smtp)

    def start(self):
        """Запустить LongPoll сессию"""

        vk_session = VkApi(token = self.token, api_version = self.api)
        self.vk = vk_session.get_api()
        self.longpoll = VkBotLongPoll(vk_session, group_id = self.id)
        self.logger.info("Session started...")


    def listen(self):
        """Слушает LongPoll сервер на предмет сообщений от пользователя"""
        btn_enter = "" # inline кнопка нажатая в данный момент

        for self.event in self.longpoll.listen():
            text = "Сколько пар пропустил ученик?"
            self.logger.info("Слушаем сервер...")

            if self.event.type == VkBotEventType.MESSAGE_NEW:
                self.logger.info("MESSAGE_NEW")
                try:
                    btn_type = json.loads(self.event.obj.message["payload"])["type"]
                except KeyError: # Это не кнопка
                    text = "Привет! Я помогу узнать домашнее задание и рапсисание занятий, напомню тебе почту преподавателя и дам ссылку на его сайт. В общем, со мной тебе будет легче и удобней учиться, надеюсь мы сработаемся :)"
                    self.send_message(text, Keyboard.main_page())

                try:
                    if btn_type == "less_one": # Ученик пропустил одну пару
                        self.send_message(Func.add_record_in_table(btn_enter, self.path, 1), Keyboard.main_page())

                    elif btn_type == "less_two": # две пары
                        self.send_message(Func.add_record_in_table(btn_enter, self.path, 2), Keyboard.main_page())

                    elif btn_type == "less_three": # три пары
                        self.send_message(Func.add_record_in_table(btn_enter, self.path, 3), Keyboard.main_page())

                    elif btn_type == "less_four": # четыре пары
                        self.send_message(Func.add_record_in_table(btn_enter, self.path, 4), Keyboard.main_page())
                except UnboundLocalError:
                    pass
                    
                from_id = str(self.event.obj.message["from_id"])
                try:
                    if btn_type == "btn_shedule": # расписание
                        self.send_message("Вы перешли в раздел: Расписание занятий", Keyboard.shedule_page())
                    
                    elif btn_type == "btn_monday_sh":
                        self.send_message(shedule.get_shedule(0), Keyboard.shedule_page())

                    elif btn_type == "btn_tuesday_sh":
                        self.send_message(shedule.get_shedule(1), Keyboard.shedule_page())

                    elif btn_type == "btn_wednesday_sh":
                        self.send_message(shedule.get_shedule(2), Keyboard.shedule_page())

                    elif btn_type == "btn_thursday_sh":
                        self.send_message(shedule.get_shedule(3), Keyboard.shedule_page())

                    elif btn_type == "btn_friday_sh":
                        self.send_message(shedule.get_shedule(4), Keyboard.shedule_page())

                    elif btn_type == "btn_saturday_sh":
                        self.send_message(shedule.get_shedule(5), Keyboard.shedule_page())
                    
                    elif btn_type == "btn_back_sh":
                        self.send_message("Вы перешли в раздел: Главный", Keyboard.main_page())
                
                    elif btn_type == "btn_homework": # домашнее задание
                        self.send_message("Домашнее задание", Keyboard.homework_page())

                    elif btn_type == "btn_monday_hm":
                        self.send_message("Внимание! Время ожидания ~ 30 сек.", Keyboard.homework_page())
                        self.send_message(Func.get_homework("monday", self.path), Keyboard.homework_page())

                    elif btn_type == "btn_tuesday_hm":
                        self.send_message("Внимание! Время ожидания ~ 30 сек.", Keyboard.homework_page())
                        self.send_message(Func.get_homework("tuesday", self.path), Keyboard.homework_page())

                    elif btn_type == "btn_wednesday_hm":
                        self.send_message("Внимание! Время ожидания ~ 30 сек.", Keyboard.homework_page())
                        self.send_message(Func.get_homework("wednesday", self.path),Keyboard.homework_page())

                    elif btn_type == "btn_thursday_hm":
                        self.send_message("Внимание! Время ожидания ~ 30 сек.", Keyboard.homework_page())
                        self.send_message(Func.get_homework("thursday", self.path), Keyboard.homework_page())

                    elif btn_type == "btn_friday_hm":
                        self.send_message("Внимание! Время ожидания ~ 30 сек.", Keyboard.homework_page())
                        self.send_message(Func.get_homework("friday", self.path), Keyboard.homework_page())

                    elif btn_type == "btn_saturday_hm":
                        self.send_message("Внимание! Время ожидания ~ 30 сек.", Keyboard.homework_page())
                        self.send_message(Func.get_homework("saturday", self.path), Keyboard.homework_page())

                    elif btn_type == "btn_back_hm":
                        self.send_message("Главное меню", Keyboard.main_page())

                    elif btn_type == "btn_materials":
                        self.send_message("Полезные материалы", Keyboard.materials_page())

                    elif btn_type == "media_mat":
                        self.send_message("Записи лекций", Keyboard.materials_page())

                    elif btn_type == "url_mat":
                        self.send_message(Func.get_urls(self.path), Keyboard.materials_page())

                    elif btn_type == "mail_mat":
                        self.send_message(Func.get_email(self.path), Keyboard.materials_page())

                    elif btn_type == "btn_back_mat":
                        self.send_message("Главное меню", Keyboard.main_page())

                    elif btn_type == "btn_admin" and from_id in self.admin:
                        self.send_message("Панель администратора", Keyboard.admin_page())

                    elif btn_type == "btn_admin" and from_id not in self.admin:
                        self.send_message("У вас нет прав просматривать этот раздел", Keyboard.main_page())

                    elif btn_type == "btn_add" and from_id in self.admin:
                        text = "Какой ученик отсутствовал на парах?"
                        self.send_message(text, Keyboard.list_add_1())
                        time.sleep(0.3)
                        self.send_message(text, Keyboard.list_add_2())
                        time.sleep(0.3)
                        self.send_message(text, Keyboard.list_add_3())

                    elif btn_type == "less_one":
                        self.send_message(btn_enter + " пропустил одну пару", Keyboard.count_lessons())

                    elif btn_type == "less_two":
                        self.send_message(btn_enter + " пропустил две пары", Keyboard.count_lessons())

                    elif btn_type == "less_three":
                        self.send_message(btn_enter + " пропустил три пары", Keyboard.count_lessons())

                    elif btn_type == "less_four":
                        self.send_message(btn_enter + " пропустил четыре пары", Keyboard.count_lessons())

                    elif btn_type == "btn_back":
                        self.send_message("Главное меню", Keyboard.main_page())

                except UnboundLocalError:
                    pass

            elif self.event.type == VkBotEventType.MESSAGE_EVENT:
                btn_type = self.event.obj.payload.get("type")

                if btn_type == "avetysyan":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "borzuxin":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "genhel":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "dyatlova":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "evdokimov":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "egorov":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "eremenko":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "ignatieva":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "kadanchik":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "korninsky":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "makarov":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "mamatov":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "mogucheva":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "oorzak":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "otmahova":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "pliev":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "reuta":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "semkiv":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "silkina":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "smelchakova":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "soloviev":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "tebenkov":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "hamidulin":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "hovrat":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "chernyakov":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "chykynev":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "shubarina":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                elif btn_type == "unusov":
                    btn_enter = btn_type
                    self.send_callback_message(text, Keyboard.count_lessons())

                      
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
    try:
        print("[*] - Bot Running...")
        current_path = os.path.dirname(os.path.abspath(__file__))

        # send
        recipients = ['mamayma8@gmail.com', 'kirillegorov77@gmail.com']
        msg = MIMEMultipart()
        me = 'mamayma8@gmail.com'
        you = 'mamayma8@gmail.com'
        msg['Subject'] = 'python-bot'
        msg['From'] = me
        msg['To'] = ", ".join(recipients)

        # Читаем конфигурационный файл
        config = configparser.ConfigParser()
        config.read("auth.ini")

        # Аутентификационные данные
        token = config.get("Auth", "group_token")
        ids = config.get("Auth", "group_id")
        api = config.get("Auth", "api_version")

        # ID Администраторов
        admin_id = []
        with open(os.path.join(current_path, "admin.json"), "r", encoding="utf8") as admin:
            admin = json.load(admin)
            
            for i in admin["list_admin"]:
                admin_id.append(admin["list_admin"][i]["id"])

        # Запускаем бота
        bot = SPBKitHelper(token, ids, api, current_path, admin_id)
        bot.start()

        while True:
            try:
                bot.listen()
            except requests.exceptions.ReadTimeout:
                print("[*] - ReadTimeout Exceptions: Reconnect...\n")
                time.sleep(3)
    except Exception as e:
        print(e)
        '''
        with open("log.log", "w") as log:
            log.write(traceback.format_exc())
            log.close()

        with open("log.log", "rb") as f:
            attachment = MIMEBase('application', 'octet-stream')
            attachment.set_payload(f.read())
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', filename="log.log")
            msg.attach(attachment)


        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login('mamayma8@gmail.com','20021977')
        s.sendmail(me, recipients, msg.as_string())
        s.quit()  
        '''     

if __name__ == "__main__":
    main()



