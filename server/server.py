import os
import requests
from flask import Flask, request, send_from_directory
from helpers.exceptions import HTTPBadRequest, HTTPNotFound
import io
import sys
from os.path import basename
from zipfile import ZipFile

UPLOAD_FOLDER = './'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)


def allowed_file(filename):
    return True
    # return '.' in filename and \
    #        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/send_zip/", methods=["GET"])
def send_zip():
    with ZipFile('files.zip', 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(UPLOAD_FOLDER):
            if 'helpers' not in folderName and '.git' not in folderName:
                zipObj.write(folderName)
                for filename in filenames:
                    if filename != 'files.zip':
                        zipObj.write(os.path.join(folderName, filename))
    # os.remove()
    return send_from_directory(UPLOAD_FOLDER, 'files.zip', as_attachment=True)

def connect():
    from requests import get

    ip = get('https://api.ipify.org').text
    
    # r = requests.post(f'http://{sys.argv[3]}/connect', data={'ip': sys.argv[1], 'port': str(sys.argv[2])})
    r = requests.post(f'http://{sys.argv[3]}/connect', data={'ip': ip, 'port': str(sys.argv[2])})
    print(r.content[:100])
    if r.content == b'':
        return
    file = io.BytesIO(r.content)
    with open('files.zip','wb') as out: ## Open temporary file as bytes
        out.write(file.read())
    with ZipFile('files.zip', 'r') as zipObj:
        # Extract all the contents of zip file in current directory
        zipObj.extractall()
connect()



# same for touch just send empty data
@app.route("/files/<path:path>", methods=["POST"])
def upload_file(path):
    filename = os.path.basename(path)
    print('path',path, 'filename', filename)
    if filename and allowed_file(filename):
        try:
            with open(os.path.join(UPLOAD_FOLDER, path), "wb") as fp:
                fp.write(request.data)
            return "", 201
        except Exception as err:
            raise HTTPNotFound(
                message="You did something wrong try again or contact Yusuf"
                        "the problem: {}".format(err)
            )
    return HTTPBadRequest(
        message='no file send or file format is not supported')


@app.route("/files/<path:path>",  methods=["GET"])
def send_file(path):
    """send a file to namenode"""
    return send_from_directory(UPLOAD_FOLDER, path, as_attachment=True)

@app.route("/check_up/",  methods=["GET"])
def check_up():
    """check the server is up"""
    return ('up', 200)


@app.route("/command/",  methods=["POST"])
def command():
    """Run command"""
    print('#'+str(request.data)[2:-1]+'###############')
    os.system(str(request.data)[2:-1])
    return ('', 204)



@app.route("/files/<path:path>",  methods=["DELETE"])
def delete_file(path):
    """delete a file"""
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, path))
    except:
        HTTPNotFound(
            message="You did something wrong try again or contact Yusuf"
        )

# path from root
# if you want to create hi dir put rootfolder/.../hi
@app.route("/mkdir/<path:path>",  methods=["PUT"])
def mkdir(path):
    try:
        os.mkdir(os.path.join(UPLOAD_FOLDER, path))
    except:
        HTTPNotFound(
            message="You did something wrong try again or contact Yusuf"
                    "The problem may acquired"
                    " because {} is wrong path".format(path)
        )


@app.route("/dir/<path:path>",  methods=["DELETE"])
def delete_dir(path):
    """delete a file"""
    try:
        os.rmdir(os.path.join(UPLOAD_FOLDER, path))
    except:
        HTTPNotFound(
            message="You did something wrong try again or contact Yusuf"
        )

if __name__ == '__main__':
    app.run(host=sys.argv[1], port=int(sys.argv[2]), debug=True)