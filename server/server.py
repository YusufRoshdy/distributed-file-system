import os

from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename
from helpers.exceptions import HTTPBadRequest, HTTPNotFound

UPLOAD_FOLDER = './files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/files/<filename>", methods=["POST"])
def upload_file(filename):
    if filename and allowed_file(filename):
        filename = secure_filename(filename)
        with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as fp:
            fp.write(request.data)
        return "", 201

    return HTTPBadRequest(
        message='no file send or file format is not supported')


@app.route("/files/<path:path>",  methods=["GET"])
def send_file(path):
    """send a file to namenode"""
    return send_from_directory(UPLOAD_FOLDER, path, as_attachment=True)


@app.route("/files/<path:path>",  methods=["DELETE"])
def delete_file(path):
    """delete a file"""
    try:
        os.remove(os.path.join(UPLOAD_FOLDER, path))
    except:
        HTTPNotFound(
            message="You did something wrong try again or contact Yusuf"
        )



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5041, debug=True)