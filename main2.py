import requests
import matplotlib.pyplot as plt
import numpy as np
from selenium import webdriver

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
if  "<pod title='Result'" in output:
    split_Results_output = output.split("<pod title='Result'\n")
elif "<pod title='Results'" in output:
    split_Results_output = output.split("<pod title='Results'\n")



split_Results_output.pop(0)
serching_for_answers = split_Results_output[0].split('       ')


final = []
for el in range(len(serching_for_answers)):
    if 'щ' in serching_for_answers[el]:
        final.append(serching_for_answers[el])



#printing the answer
for line in final:
    if 'alt=' in line and 'щ' in line:
        line = line.strip('alt=')
        line = line.replace('&lt;', '<')
        line = line.replace('sqrt', '√')
        line = line.replace('щ', 'x')
        print(line)

#меняем инпут для задания функции
query_for_plot = query_for_plot.replace('^', '**').strip('solve ')


query_before_ = ''
for i in query_for_plot[:query_for_plot.index('=')]:
    if i != '=':
        query_before_ += i


query_after_ = ''

for i in query_for_plot[query_for_plot.index('='):]:
    if i != '=':
        query_after_ += i

#переводим str в function
def str_to_func(string):
    return lambda x: eval(string)


func_before = str_to_func(query_before_)
func_after = str_to_func(query_after_)

#строим графики
xlist1 = np.linspace(-2, 2, num=100)
ylist1 = [func_before(x) for x in xlist1]

plt.plot(xlist1, ylist1)


xlist2 = np.linspace(-2, 2, num=100)
ylist2 = [func_after(x) for x in xlist2]

plt.plot(xlist2, ylist2)

plt.title(query_for_plot)

plt.axvline(x=0, c="black", label="x=0")
plt.axhline(y=0, c="black", label="y=0")

plt.show()
