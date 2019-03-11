#  -*- encoding: utf-8 -*-

import logging
import traceback

import requests

from app.clients.telegram import TelegramClient
from app.common.constants_and_variables import AppVariables


class TelegramResource(object):

    def __init__(self):
        self.telegram_client = TelegramClient()
        self.api_send_message = self.telegram_client.api_send_message()
        self.app_variables = AppVariables()

    def send_message(self, chat_id, message, parse_mode='Markdown', disable_web_page_preview=True,
                     disable_notification=False, reply_markup=None):
        data = {
            'chat_id': chat_id,
            'text': '{message}'.format(message=message),
            'parse_mode': parse_mode,
            'disable_web_page_preview': disable_web_page_preview,
            'disable_notification': disable_notification,
            'reply_markup': reply_markup
        }
        try:
            logging.info("Sending message: {message}".format(message=data))
            response = requests.post(self.api_send_message, data=data)
            logging.info("Response status code: {status_code}".format(status_code=response.status_code))
        except Exception:
            logging.error("Something went wrong. Exception: {exception}".format(exception=traceback.format_exc()))

    def shadow_message(self, message, parse_mode='Markdown', disable_web_page_preview=True, disable_notification=False,
                       reply_markup=None):
        if self.app_variables.shadow_mode:
            data = {
                'chat_id': '{chat_id}'.format(chat_id=self.app_variables.shadow_mode_chat_id),
                'text': '{message}'.format(message=message),
                'parse_mode': parse_mode,
                'disable_web_page_preview': disable_web_page_preview,
                'disable_notification': disable_notification,
                'reply_markup': reply_markup
            }
            try:
                logging.info("Shadowing message: {message}".format(message=data))
                response = requests.post(self.api_send_message, data=data)
                logging.info("Response status code: {status_code}".format(status_code=response.status_code))
            except Exception:
                logging.error("Something went wrong. Exception: {exception}".format(exception=traceback.format_exc()))
        else:
            logging.info("Shadow mode is disabled.")