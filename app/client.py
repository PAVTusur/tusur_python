import requests

r = requests.get("http://localhost:6000/")
print(r.status_code)
print(r.text)
r = requests.get("http://localhost:6000/info")
print(r.status_code)
print(r.text)
