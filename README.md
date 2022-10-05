# telegram-bot-iogram-parser-exchange-rates

This telegram bot provides information about the current quotes of the exchange rates of various currencies of the Central Bank of the Russian Federation.
You can also additionally find out the quotes of cryptocurrency rates and the TOP-7 with the maximum growth rate over the past 24 hours in real time

## Data sources
* The exchange rates: https://www.cbr.ru/currency_base/daily
* The cryptocurrency rates: https://myfin.by/crypto-rates


## Requirements
* Python 3.10;
* iogram
* requests
* bs4

## Installation
Install requirements:

        pip install -r requiremets

Create a database and specify the access parameters in the file:

* `config.py`

Fill in the following fields in file config.py:

token = 'your token'

## Application launch
After setting config-parameters, run the file:

* `tg_bot_exchange_rates.py`
