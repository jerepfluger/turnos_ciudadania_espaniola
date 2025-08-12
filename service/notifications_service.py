import json
import os
from os import environ as env

import requests
from dotenv import load_dotenv

from constants.common import ERRORS
from constants.notifications.common import NOTIFICATIONS_CHANNELS_TO_URL_PATH, TELEGRAM, SLACK
from exceptions.exceptions import UnknownNotificationChannel
from helpers.logger import logger

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv('.env')


def build_telegram_token_and_channel_id():
    telegram_token = os.getenv('TELEGRAM_TOKEN', '')
    if not telegram_token:
        telegram_token = env['TELEGRAM_TOKEN']
    telegram_channel_id = os.getenv('TELEGRAM_CHANNEL_ID', '')
    if not telegram_channel_id:
        telegram_channel_id = env['TELEGRAM_CHANNEL_ID']
    return telegram_token, telegram_channel_id
2

class NotificationsService:
    def __init__(self):
        self.slack_url = "https://hooks.slack.com/services/T08CWSL07SM/"
        self.telegram_url = "https://api.telegram.org/bot{token}/sendMessage"

    def post_notification(self, engine, message, channel=None):
        if engine == TELEGRAM:
            return self.post_telegram_notification(message)
        if engine == SLACK:
            return self.post_slack_notification(message, channel)

        raise NotImplementedError(f"Unknown notification engine {engine}")

    def post_telegram_notification(self, message):
        logger.info(f"Sending Telegram message")
        telegram_token, telegram_channel_id = build_telegram_token_and_channel_id()
        url = self.telegram_url.format(token=telegram_token)

        payload = {
            "chat_id": telegram_channel_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            raise Exception(response.text)

        logger.info(f"Telegram message sent successfully to channel {telegram_channel_id}!")
        return

    def post_slack_notification(self, message, channel):
        service_path = NOTIFICATIONS_CHANNELS_TO_URL_PATH.get(channel)
        if not service_path:
            logger.info(f"Slack notification channel {channel} not found")
            raise UnknownNotificationChannel(f"Unknown notification channel for key: {channel}")

        logger.info(f"Sending message to Slack channel {channel}")
        payload = json.dumps({"text": message})
        headers = {"Content-Type": "application/json"}

        response = requests.post(f'{self.slack_url}{service_path}', data=payload, headers=headers)
        if response.status_code != 200:
            raise Exception(response.text)

        logger.info(f"Slack message sent successfully!")
        return


if __name__ == '__main__':
    NotificationsService().post_notification(TELEGRAM, '<!here> Testing', ERRORS)
