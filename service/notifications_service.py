import json
import os
from os import environ as env

import requests
from dotenv import load_dotenv

from helpers.logger import logger

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(os.path.dirname(ROOT_PATH), '.env'))


class NotificationsService:
    def __init__(self):
        self.telegram_url = "https://api.telegram.org/bot{token}/sendMessage"

    def post_notification(self, user, message):
        logger.info(f"Sending Telegram message")
        telegram_token = build_telegram_token_and_channel_id()
        chat_id = get_chat_id_by_user(user)
        url = self.telegram_url.format(token=telegram_token)

        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            raise Exception(response.text)

        logger.info(f"Telegram message sent successfully to user {user}!")
        return


def build_telegram_token_and_channel_id():
    return os.getenv('TELEGRAM_TOKEN', '') or env.get('TELEGRAM_TOKEN', '')


def get_chat_id_by_user(user):
    full_chat_id = f'{user.upper()}_CHAT_ID'
    return os.getenv(full_chat_id, '') or env.get(full_chat_id, '')


def get_bot_messages_updates():
    url = 'https://api.telegram.org/bot{}/getUpdates'
    response = requests.get(url.format(build_telegram_token_and_channel_id()))
    if response.status_code != 200:
        raise Exception(response.text)
    messages = json.loads(response.content)
    users = {}
    for message in messages['result']:
        first_name = message.get('message', {}).get('chat', {}).get('first_name', '')
        last_name = message.get('message', {}).get('chat', {}).get('last_name', '')
        chat_id = message.get('message', {}).get('chat', {}).get('id', '')
        if not first_name or not last_name or not chat_id:
            continue
        if chat_id not in users:
            users[chat_id] = f"{first_name} {last_name}"

    logger.info(f"Full list of user that have interacted with the bot are: {users}")
