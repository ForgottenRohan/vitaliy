from aiogram import Bot, Dispatcher, types
from config import bot_token, admins, channels, statuses
from main import collect_on, collect_links, count
import asyncio
import datetime as dt
from scheduler.asyncio import scheduler

bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message()
async def start(message: types.Message):
    if message.text == '/start':
        if message.chat.id in admins:
            kb = [
                    [types.KeyboardButton(text="Запуск | Отключение")],
                    [types.KeyboardButton(text="Число ссылок")]
                ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await bot.send_message(message.chat.id, 'Здаров!', reply_markup=keyboard)
        else:
            await bot.send_message(message.chat.id, 'Ты не админ, не могу ничем помочь. Сорян(')
    elif message.text == 'Число ссылок':
        # await bot.send_message(message.chat.id, 'Функция недоступна на данный момент!')
        if message.chat.id in admins:
            try:
                count_ = count()
                await bot.send_message(message.chat.id, f'Число ссылок на данный момент: {count_}')
            except Exception:
                await bot.send_message(message.chat.id, f'Число ссылок на данный момент неизвестно!\nПриношу свои извинения!')
        else:
            await bot.send_message(message.chat.id, 'Ты не админ, не могу ничем помочь. Сорян(')
    elif message.text == 'Запуск | Отключение':
        status = statuses
        if message.chat.id in admins:
            if status == True:
                await bot.send_message(message.chat.id, f'Автопостинг: Deactive')
                Fals()
            else:
                await bot.send_message(message.chat.id, f'Автопостинг: Active')
                Tru()
                await activation()

        else:
            await bot.send_message(message.chat.id, 'Ты не админ, не могу ничем помочь. Сорян(')
async def activation():
    schedule = scheduler.Scheduler()

    schedule.cyclic(dt.timedelta(minutes=2), active)
    schedule.daily(dt.time(), collect_links)
    while True:
        await asyncio.sleep(1)

            

async def active():
    if statuses == True:
        image = collect_on()
        for channel in channels:
            await bot.send_photo(channel, image)
    
def Fals():
    global statuses
    statuses = False
    
def Tru():
    global statuses
    statuses = True

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

