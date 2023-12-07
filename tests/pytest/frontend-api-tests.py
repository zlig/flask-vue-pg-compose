import requests

host = 'http://127.0.0.1:8081'

# # Make a GET request to the API endpoint
# response = requests.get(url)

# if response.status_code == 200:
#     print(response.json())
# else:
#     print('Error: {0}'.format(response.status_code)) 


import requests
import pytest


def test_1_get():
    url = host+"/ping"
    res = requests.get(url)
    print("RESPONSE:", res.json())
    assert res.status_code == 200

def test_2_put():
    url = host+"/accounts"
    data = {"name":"string"}
    res = requests.post(url, json=data)
    print("RESPONSE:", res.json())
    assert res.status_code == 200
