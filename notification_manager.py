from auth import TELEGRAM_BOT_CHATID, TELEGRAM_BOT_TOKEN, EMAIL_FROM, EMAIL_PASS
import requests
import smtplib


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

    def send_email(self, message, emails):
        SMTP_SERVER = "smtp.gmail.com"
        with smtplib.SMTP(SMTP_SERVER) as connection:
            connection.starttls()
            connection.login(user=EMAIL_FROM, password=EMAIL_PASS)
            for email_address in emails:
                connection.sendmail(from_addr=EMAIL_FROM,
                                    to_addrs=email_address, msg=message)
