import requests
import matplotlib.pyplot as plt
import numpy as np
import mpmath
from selenium import webdriver
import math

AppID_full = 'G39592-5E4JX9R2AK'
query = str(input())
query_for_plot = query
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
    print(line)


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

#if '=' in results_str or '≈' in ', '.join(results_str):
for x in results_str:
    if '=' in x and '±' not in x:
        xs.append(x[x.index('=') + 1:].strip("'").strip('...'))
    elif '=' in x and '±' in x:# and '√' not in x:
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


    plt.plot(xlist2, ylist2)

    plt.title(query.replace('щ', 'x').strip('solve '))

    plt.axvline(x=0, c="black", label="x=0")
    plt.axhline(y=0, c="black", label="y=0")

    plt.show()







