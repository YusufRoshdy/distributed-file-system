import requests

def upload():
    with open('helpers/exceptions.py') as fp:
        content = fp.read()

    requests.post(
        '{}/files/newdata.txt'.format("http://127.0.0.1:5041"), data=content
    )

def download():
    response = requests.get(
        '{}/files/newdata.txt'.format("http://127.0.0.1:5041")
    )
    with open('./testdata.txt', "wb") as fp:
        fp.write(response.content)


download()