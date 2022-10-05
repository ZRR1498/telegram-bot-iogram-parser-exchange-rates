from aiogram import Bot, Dispatcher, executor, types
from config import token
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime
from aiogram.dispatcher.filters import Text


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Приветствуем в нашем сервисе курса валют!")
    start_buttons = ["Курсы всех валют", "Курсы основных валют", "Курсы всех криптовалют", "ТОП роста криптовалют"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Выберите категорию ниже:", reply_markup=keyboard)



@dp.message_handler(Text(equals="Курсы всех валют"))
async def get_all_rates(message: types.Message):
    url_currency = 'https://www.cbr.ru/currency_base/daily'

    dict_curr = {}

    page = requests.get(url_currency, headers={'User-Agent': UserAgent().chrome})

    soup = BeautifulSoup(page.text, "html.parser")
    all_value = soup.findAll('table', class_='data')
    line = str(all_value[0]).split('\n')

    for i in range(8, len(line)):
        if line[i] == '<tr>':
            filter_news = []

            for j in range(i, i + 4):
                filter_news.append(line[j + 2].strip('<td></h>th>'))
                i += 1

            date = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
            filter_news.append(date)
            dict_curr[filter_news[2]] = {'Индекс': filter_news[0], 'Единиц': filter_news[1], 'Курс': filter_news[3],
                                         'Текущее время': filter_news[4]}

    for k, v in dict_curr.items():
        rates = f"<b>{k}</b>: \n" \
                f"Курс: {v['Курс']} [руб.~{v['Единиц']}] \n" \
                f"{v['Текущее время']}"

        await message.answer(rates)


@dp.message_handler(Text(equals="Курсы основных валют"))
async def get_all_rates(message: types.Message):
    url_currency = 'https://www.cbr.ru/currency_base/daily'

    dict_curr = {}

    page = requests.get(url_currency, headers={'User-Agent': UserAgent().chrome})

    soup = BeautifulSoup(page.text, "html.parser")
    all_value = soup.findAll('table', class_='data')
    line = str(all_value[0]).split('\n')

    for i in range(8, len(line)):
        if line[i] == '<tr>':
            filter_news = []

            for j in range(i, i + 4):
                filter_news.append(line[j + 2].strip('<td></h>th>'))
                i += 1

            date = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
            filter_news.append(date)

            top_rates = ['Армянских драмов', 'Белорусских рублей', 'Доллар США', 'Евро', 'Казахстанских тенге',
                         'Китайских юаней', 'Турецких лир', 'Украинских гривен',
                         'Фунт стерлингов Соединенного королевства']

            if filter_news[2] in top_rates:
                dict_curr[filter_news[2]] = {'Индекс': filter_news[0], 'Единиц': filter_news[1], 'Курс': filter_news[3],
                                             'Текущее время': filter_news[4]}

    for k, v in dict_curr.items():
        rates = f"<b>{k}</b>: \n" \
                f"Курс: {v['Курс']} [руб.~{v['Единиц']}] \n" \
                f"{v['Текущее время']}"

        await message.answer(rates)


@dp.message_handler(Text(equals="Курсы всех криптовалют"))
async def get_all_rates(message: types.Message):
    arr_value = {}

    for k in range(1, 4):
        url_crypto = f'https://myfin.by/crypto-rates?page={k}'

        page = requests.get(url_crypto, headers={'User-Agent': UserAgent().chrome})
        soup = BeautifulSoup(page.text, "html.parser")
        all_value = soup.findAll('tbody', class_="table-body")
        line = str(all_value[0]).split('\n')

        for i in range(len(line)):
            if line[i] == '<tr class="odd">' or line[i] == '<tr class="even">':
                first_name = line[i + 1].split('">')[-2].split('</a')[0]
                last_name = line[i + 1].split('">')[-1].split('</')[0]
                value = line[i + 2].split('/td><td>')[1].split('<div')[0][:-2]
                capitalization = line[i + 2].split('xs">')[1].split('</td')[0][:-1].replace(' ', '')
                per_change = line[i + 2].split('</span></td><td>')[-2].split('">')[-1][:-1]
                date = datetime.now().strftime('%H:%M:%S %d-%m-%Y')

                if capitalization == 'N/':
                    capitalization = 'N/A'

                arr_value[first_name] = {'Индекс': last_name, 'Стоимость': value, 'Изменение цены': per_change,
                                         'Капитализация': capitalization, 'Время': date}

    for k, v in arr_value.items():
        rates = f"<b>{k} : {v['Индекс']}</b> \n" \
                f"Стоимость: {v['Стоимость']} $ : <u>{v['Изменение цены']} %</u> \n" \
                f"Капитализация: {v['Капитализация']} $\n" \
                f"{v['Время']}"

        await message.answer(rates)


@dp.message_handler(Text(equals="ТОП роста криптовалют"))
async def get_all_rates(message: types.Message):
    arr_value = {}
    arr_per_change = []

    for k in range(1, 4):
        url_crypto = f'https://myfin.by/crypto-rates?page={k}'

        page = requests.get(url_crypto, headers={'User-Agent': UserAgent().chrome})
        soup = BeautifulSoup(page.text, "html.parser")
        all_value = soup.findAll('tbody', class_="table-body")
        line = str(all_value[0]).split('\n')



        for i in range(len(line)):
            if line[i] == '<tr class="odd">' or line[i] == '<tr class="even">':
                first_name = line[i + 1].split('">')[-2].split('</a')[0]
                last_name = line[i + 1].split('">')[-1].split('</')[0]
                value = line[i + 2].split('/td><td>')[1].split('<div')[0][:-2]
                capitalization = line[i + 2].split('xs">')[1].split('</td')[0][:-1].replace(' ', '')
                per_change = line[i + 2].split('</span></td><td>')[-2].split('">')[-1][:-1]
                date = datetime.now().strftime('%H:%M:%S %d-%m-%Y')

                if capitalization == 'N/':
                    capitalization = 'N/A'

                arr_value[first_name] = {'Индекс': last_name, 'Стоимость': value, 'Изменение цены': per_change,
                                         'Капитализация': capitalization, 'Время': date}

                if per_change[0] == '+':
                    arr_per_change.append(per_change)

    arr_per_change.sort(reverse=True)

    for k, v in sorted(arr_value.items(), key=lambda v: v[1]['Изменение цены'], reverse=True):
        if v['Изменение цены'] in arr_per_change[:7]:
            rates = f"<b>{k} : {v['Индекс']}</b> \n" \
                    f"Стоимость: {v['Стоимость']} $ : <u>{v['Изменение цены']} %</u> \n" \
                    f"Капитализация: {v['Капитализация']} $\n" \
                    f"{v['Время']}"

            await message.answer(rates)

if __name__ == '__main__':
    executor.start_polling(dp)