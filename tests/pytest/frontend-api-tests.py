import requests

url = 'http://127.0.0.1:8081/hi'

# Make a GET request to the API endpoint
response = requests.get(url)

if response.status_code == 200:
    print(response.json())
else:
    print('Error: {0}'.format(response.status_code)) 
      