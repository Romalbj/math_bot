import requests
import wolframalpha

client = wolframalpha.Client('G39592-5E4JX9R2AK')

input1 = str(input())
res = client.query(input1)
output = next(res.results).text
print(output)