from auth import TELEGRAM_BOT_CHATID, TELEGRAM_BOT_TOKEN
import requests


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        self.response = {}

    def telegram_bot_sendtext(self, bot_message):
        """Sends the text message passed as parameter to the telegram bot.
        Returns the response code"""
        params = {
                "chat_id": TELEGRAM_BOT_CHATID,
                "text": bot_message,
                "parse_mode": "MARKDOWN",
                }
        url = "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage"
        response = requests.get(url, params=params)
        response.raise_for_status()
        self.response = response.json()
        return response.json()
