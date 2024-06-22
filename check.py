from datetime import datetime

import json
import os
import requests
import telegram
import asyncio
from dotenv import load_dotenv

load_dotenv()

spot_api_url = 'https://spot.photoprintit.com/spotapi/orderInfo/forShop'

config_number = os.getenv('config_number')
shop_id = os.getenv('shop_id')
order_id = os.getenv('order_id')
bot_token = os.getenv('bot_token')
chat_id = os.getenv('chat_id')

bot = telegram.Bot(token=bot_token)
# Get the directory of the current script
project_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(project_directory, 'order_status.json')


async def send_message(chat_id, state_text, current_time):
    text = '{state} ({time})'.format(
        state=state_text,
        time=current_time
    )

    async with bot:
        await bot.send_message(text=text, chat_id=chat_id)


def fetch_order_status():
    response = requests.get(
        spot_api_url,
        params={
            'config': config_number,
            'shop': shop_id,
            'order': order_id
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
        },
    )

    response_json = response.json()
    state_code = response_json['subOrders'][0]['stateCode']
    state_text = response_json['subOrders'][0]['stateText']

    return {'stateCode': state_code, 'stateText': state_text}


def read_previous_response(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return None


def write_response_to_file(file_path, response):
    with open(file_path, 'w') as file:
        json.dump(response, file)


async def main():
    new_response = fetch_order_status()
    current_time = datetime.now().strftime('%d.%m. %H:%M')

    previous_response = read_previous_response(file_path)

    # Previous reponse is present
    if previous_response:
        # Check if the state code has changed
        if new_response['stateCode'] != previous_response['stateCode']:
            await send_message(
                chat_id=chat_id,
                state_text=new_response['stateText'],
                current_time=current_time
            )
    # No order state has been checked before, send a message
    else:
        await send_message(
            chat_id=chat_id,
            state_text=new_response['stateText'],
            current_time=current_time
        )

    write_response_to_file(file_path, new_response)

if __name__ == '__main__':
    asyncio.run(main())
