import requests
from telegram import Bot

TELEGRAM_BOT_TOKEN = '6933080057:AAHdzBeEKtVrRpSx1x9HF4N8GZM1eWDo8N8'
TELEGRAM_GROUP_CHAT_ID = -4139336722  # Replace with your group chat ID

# async def send_telegram_message(message):
#     bot = Bot(token=TELEGRAM_BOT_TOKEN)
#     await bot.send_message(chat_id=TELEGRAM_GROUP_CHAT_ID, text=message)


def send_telegram_message(message): 
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_GROUP_CHAT_ID}&text={message}"
    print(requests.get(url).json())
 
# # Example usage:
# async def main():
#     await send_telegram_message("Your message here")

# # Run the event loop
# import asyncio
# asyncio.run(main())