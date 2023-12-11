# By default the output only shows failures
# to see all output use the -s option, e.g.:
#   pytest -s file.py

import requests
import pytest

host = 'http://127.0.0.1:8081'

def test_1_get():
    url = host+"/ping"
    res = requests.get(url)
    print("RESPONSE:", res.status_code)
    print("RESPONSE:", res.json)
    print("RESPONSE:", res.text)
    assert res.status_code == 200

def test_2_post():
    url = host+"/accounts"
    data = {"name":"string"}
    res = requests.post(url, json=data)
    print("RESPONSE:", res.json())
    assert res.status_code == 200
