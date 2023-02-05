import random

from aiogram.types import Message
from loader import dp


max_total = 150
total = []


@dp.message_handler(commands=['start'])
async def mes_start(message: Message):
    global total
    for duel in total:
        if message.from_user.id == duel[0]:
            await message.answer('Ты уже начал игру! Играй давай!')
            break
    else:
        await message.answer(f'Привет, {message.from_user.full_name} '
                             f'Мы будем играть в конфеты. Бери от 1 до 28...')
        my_game = [message.from_user.id,
                   message.from_user.first_name, max_total]
        total.append(my_game)


@dp.message_handler(commands=['set'])
async def mes_set(message: Message):
    global total
    global max_total
    name = message.from_user.first_name
    count = message.text.split()[1]
    if count.isdigit():
        max_total = int(count)
        await message.answer(f'Конфет теперь будет: {max_total} ')
    else:
        await message.answer(f'{name}, введите цифрами')


@dp.message_handler(commands=['help'])
async def mes_help(message: Message):
    await message.answer(f'Для начала игры введите команду "/start"\n '
                         f'Для того чтобы поменять количество конфет, введите команду "/set кол-во конфет(по умолчанию 150 шт.)"\n '
                         f'Для выхода из программы во время игры, введите команду "exit"')
    print(message.from_user.id)


@dp.message_handler()
async def game(message: Message):
    global total
    for duel in total:
        if message.from_user.id == duel[0]:
            count = message.text
            if count.isdigit() and 0 < int(count) < 29:
                duel[2] -= int(count)
                if await check_win(message, 'Ты', duel):
                    return True
                await message.answer(f'{duel[1]} взял {count} конфет и на столе осталось {duel[2]} конфет\n'
                                     f' Теперь ход бота...')
                bot_take = random.randint(1, 28) if duel[2] > 28 else duel[2]
                duel[2] -= bot_take
                if await check_win(message, 'Бот', duel):
                    return True
                await message.answer(f'Бот взял {bot_take} конфет и на столе осталось {duel[2]}\n'
                                     f'Теперь твой ход...')
            elif message.text == 'exit':
                 total.remove(duel)
                 return True
            else:
                await message.answer(f'Введите число от 1 до 28')


async def check_win(message: Message, win: str, duel: list):
    if duel[2] <= 0:
        await message.answer(f'{win} победил! Поздравляю!')
        total.remove(duel)
        return True
    return False
