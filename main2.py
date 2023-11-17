import requests
import json

AppID_full = 'G39592-5E4JX9R2AK'
query = str(input())

response = requests.get(f'http://api.wolframalpha.com/v2/query',
                        params={
                            'appid': AppID_full,
                            'input': query
                        })
output = response.text
split_Results_output = output.split("Results'\n")
print(split_Results_output)
split_Results_output.pop(0)
serching_for_answers = split_Results_output[0].split('       ')

final = []
for el in range(len(serching_for_answers)):
    if "alt='x =" in serching_for_answers[el]:
        final.append(serching_for_answers[el].strip('alt=').strip("'"))

for answer in final:
    print(answer)
