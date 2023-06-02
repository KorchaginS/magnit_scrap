import csv

from bot_data import token

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
import time
from main import getData

bot = Bot(token=token,parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

goodsList = []
count = 0

@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Показать скидки']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Привет! Что ищем?', reply_markup=keyboard)

@dp.message_handler(Text(equals='Показать скидки'))
async def get_discounts(message: types.Message):
    await message.answer('Please wait...')

    #getData()

    with open('data.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)

        global goodsList

        goodsList = []
        first = True
        for row in reader:
            if first:
                first = False
                continue

            if len(row) == 0:
                continue

            tempDict ={
                'Name':row[0],
                'OldPrice':row[1],
                'CurrentPrice':row[2],
                'DiscountPercent':row[3],
                'EndDate':row[4]
            }
            goodsList.append(tempDict)



    global count
    count = 0
    for item in goodsList:
        count += 1
        card = f'{item["Name"]}\n' \
               f'{hbold("Скидка: ")}{item["DiscountPercent"]}%\n' \
               f'{hbold("Старая цена: ")}₽{item["OldPrice"]}🔥\n' \
               f'{hbold("Новая цена: ")}₽{item["CurrentPrice"]}🔥\n' \
               f'{hbold("Дата окончания: ")}{item["EndDate"]}🔥'

        if count == 10:
            start_buttons = ['Показать скидки', 'Далее']
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*start_buttons)
            await message.answer(card, reply_markup = keyboard)
            break

        await message.answer(card)




@dp.message_handler(Text(equals='Далее'))
async def get_discounts(message: types.Message):
    global count

    for x in range(10):
        count += 1
        card = f'{goodsList[count]["Name"]}\n' \
               f'{hbold("Скидка: ")}{goodsList[count]["DiscountPercent"]}%\n' \
               f'{hbold("Старая цена: ")}${goodsList[count]["OldPrice"]}🔥' \
               f'{hbold("Новая цена: ")}${goodsList[count]["CurrentPrice"]}🔥' \
               f'{hbold("Дата окончания: ")}${goodsList[count]["EndDate"]}🔥'
        await message.answer(card)

        if count == len(goodsList):
            start_buttons = ['Показать скидки']
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*start_buttons)
            await message.answer("Скидки кончились!", reply_markup = keyboard)


def main():
    executor.start_polling(dp)

if __name__ == '__main__':
    main()