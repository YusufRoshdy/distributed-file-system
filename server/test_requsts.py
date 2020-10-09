import requests

with open('helpers/exceptions.py') as fp:
    content = fp.read()

response = requests.post(
    '{}/files/newdata.txt'.format("http://127.0.0.1:5041"), data=content
)
