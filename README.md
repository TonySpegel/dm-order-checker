# DM order checker

DM Drogerie Markt (DM) is a chain of retail stores. 
They offer a wide range of services, including developing analog film. 
To check the status of an order, you can use the following website: 
[Order status DM Fotoparadies](https://www.fotoparadies.de/service/auftragsstatus.html)

The `check.py` script in this repository queries a public endpoint of this website and writes 
the current status to a JSON file if it differs from the previous one or if it has not 
been queried before. It also sends a message using a Telegram bot.

## Configuration and setup 

I'm using the [Pipenv packaging tool](https://pipenv.pypa.io) is used to 
install its dependencies and to manage a virtual environment.
The script expects a `.env` file with the following content:

```env
config_number=000 
shop_id=000
order_id=000
bot_token=000
chat_id=000
```
Replace every `000` with actual values. 
`shop_id` and `order_id` can be taken 
from the envelope of the order.  

`bot_token` and `chat_id` are related 
to sending messages using a Telegram bot.
