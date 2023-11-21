from aiogram import Bot, Dispatcher, types
import asyncio
from aiogram.filters import CommandStart,  Command
from aiogram.types import InputFile
import requests
import matplotlib.pyplot as plt
import numpy as np
import os
import mpmath
import math


Bot_token = '6805987386:AAEYrzVkVv4ZR1hhKz5PSVMScHrW8_XBoxk'
bot = Bot(Bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_command(message: types.Message):
    await message.answer(text=f'Здорова, тупенький: {message.from_user.username}')


@dp.message(Command('help'))
async def help_command(message: types.Message):
    await message.answer(text='''
Могу решать уравнения и неравенства, а также рисовать графики.
Вот правила ввода данных: 
- знак степени - ^
- знак умножения - *
- знак деления - /
- квадратный корень - ^1/2
- синус - sin
- косинус - cos
- тангенс - tan
- котангенс - cot
- знак больше - >
- знак меньше - <''')


@dp.message(Command('solve'))
async def solve_command(message: types.Message):
    await message.answer(text='Введи уравнение/неравенство')



global query
query = ''

global query_for_plot
query_for_plot = ''

global results_str
results_str = []


def solve_math():
    global query
    global query_for_plot
    global results_str

    query = 'solve ' + query
    query_for_plot = query

    AppID_full = 'G39592-5E4JX9R2AK'

    query = query.replace('x', 'щ')


    response = requests.get(f'http://api.wolframalpha.com/v2/query',
                            params={
                                'appid': AppID_full,
                                'input': query
                            })
    output = response.text



    serching_for_answers = output.split('       ')
    final = []
    for el in serching_for_answers:
        if 'alt=' in el and 'щ' in el and 'solve' not in el:
            final.append(el.strip())



    #printing the answer
    results_str = []
    for line in final:
        line = line.strip('alt=').replace('&lt;', '<').replace('&gt;', '>').\
            replace('sqrt', '√').replace('щ', 'x')
        results_str.append(line)
    return results_str




def plot():
    global query_for_plot
    global results_str

    #меняем аутпут для задания функции
    query_for_plot = query_for_plot.replace('^', '**').strip('solve').replace('cos', 'mpmath.cos'). \
        replace('tan', 'mpmath.tan').replace('cot', 'mpmath.cot').replace(' sin', 'math.sin')


    query_before_ = ''
    query_after_ = ''
    if '=' in query_for_plot:
        for i in query_for_plot[:query_for_plot.index('=')]:
            if i != '=':
                query_before_ += i


        for i in query_for_plot[query_for_plot.index('='):]:
            if i != '=':
                query_after_ += i


    xs = []

    for x in results_str:
        if '=' in x and '±' not in x:
            xs.append(x[x.index('=') + 1:].strip("'").strip('...'))
        elif '=' in x and '±' in x:
            xs.append(x[x.index('=') + 1:].strip("'").strip('...').replace('±', '').strip(' '))
            xs.append(x[x.index('=') + 1:].strip("'").strip('...').replace('±', '').strip(' '))
            xs[0] = '-' + xs[0]
            xs[1] = ' ' + xs[1]
        elif '≈' in x:
            xs.append(x[x.index('≈') + 1:].strip("'").strip('...'))

    results_float = []
    for i in xs:

        if '√' in i:

            if len(i.split('√'))>2:
                pass

            else:

                if len(i.split('√')[0]) == 1:
                    i = i.replace('√', 'math.sqrt')
                    results_float.append(eval(i))

                elif isinstance(int(i[i.index('√')-2]), int):
                    i = i.split('√')
                    i = '* math.sqrt'.join(i)
                    results_float.append(eval(i))

                else:
                    i = i.replace('√', 'math.sqrt')
                    results_float.append(eval(i))
        else:
            results_float.append(eval(i))


    global  x_max
    x_max = 3

    global  x_min
    x_min = -3

    def max_min_x():
        global x_max
        global x_min

        try:
            if 'sin' in query or 'cos' in query or 'tan' in query or 'cot' in query:
                x_max = 1
                x_min = -1
            elif '>' in query or '<' in query:
                pass
            elif len(results_float) < 1:
                pass
            else:
                x_max = (max(results_float))
                x_min = (min(results_float))
            return x_min, x_max
        except NameError:
            return -1


    max_min_x()


        #переводим str в function
    def str_to_func(string):
        return lambda x: eval(string)


    if '=' in ''.join(results_str) or '≈' in ''.join(results_str):
        func_before = str_to_func(query_before_)
        func_after = str_to_func(query_after_)

            #строим графики
        xlist1 = np.linspace(x_min-1, x_max+1, num=100)
        ylist1 = [func_before(x) for x in xlist1]

        plt.plot(xlist1, ylist1)

        xlist2 = np.linspace(x_min-1, x_max+1, num=100)
        ylist2 = [func_after(x) for x in xlist2]

        plt.axvline(x=0, c="black", label="x=0")
        plt.axhline(y=0, c="black", label="y=0")

        plt.plot(xlist2, ylist2)

        plt.title(query.replace('щ', 'x').strip('solve'))
        plt.savefig("plot.png")
        plt.clf()





@dp.message()
async def solve(message: types.Message):
    global query
    global query_for_plot

    query = str(message.text)
    query_for_plot = query
    answer = str('\n\n'.join(solve_math())).replace("'", '')
    plot()

    if os.path.isfile("plot.png"):

        photo_path = ('/Users/romanzavarzin/PycharmProjects/math_tg_bot/plot.png')
        await message.answer(text=answer)
        await message.reply_photo(photo=types.FSInputFile(path=photo_path))
        os.remove("/Users/romanzavarzin/PycharmProjects/math_tg_bot/plot.png")

    else:
        await message.answer(text=answer)



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())




