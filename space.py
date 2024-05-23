import socket
import webbrowser
import pyqrcode
import os
from flask import Flask, render_template, request, jsonify, redirect
from werkzeug.utils import secure_filename

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 8000))
IP = "http://" + s.getsockname()[0] + ":" + str(8000)
link = IP
url = pyqrcode.create(link)
url.svg("./static/files/myqr.svg", scale=8)
webbrowser.open(IP)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), './static/')

images = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'svg']


def is_image(filename):
    return '.' in filename and filename.rsplit(".", 1)[1].lower()

def gen():
    pictures = []
    files = []
    for file in os.listdir("./static/"):
        if file == "files": 
            continue
        if is_image(file) in images:
            pictures.append(file)
        else:
            files.append(file)
    return [files, pictures]





#FLask

@app.route("/")
def index():
    #return render_template("index.html", pictures=os.listdir("./static/images"), files=os.listdir("./static/files"))
    gen()
    return render_template("index.html", pictures=gen()[1], files=gen()[0], address=IP)

#Uploading Files

@app.route("/upload", methods=["GET", "POST"])
def upload_media():
    if request.method == "POST":
        file = request.files.getlist("file[]")
        if file == '':
            return jsonify({'error': 'file not provided'}), 400
        elif file:
            for f in file:
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect("/")
    # else:
        #return redirect(url_for("/"), code=307)

app.run(host="0.0.0.0", port=8000)
