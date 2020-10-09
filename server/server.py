import os

from flask import Flask, request
from werkzeug.utils import secure_filename
from .helpers.exceptions import HTTPBadRequest

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



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5041, debug=True)