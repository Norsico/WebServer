import requests

response = requests.get('http://127.0.0.1:6006/api', params={'age': "10", 'name': "zs"})

print(response)
