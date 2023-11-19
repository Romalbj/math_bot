import requests


AppID_full = 'G39592-5E4JX9R2AK'
query = str(input())
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




for line in final:
    if 'alt=' in line and 'щ' in line:
        line = line.strip('alt=')
        line = line.replace('&lt;', '<')
        line = line.replace('sqrt', '√')

        line = line.replace('щ', 'x')
        print(line)

