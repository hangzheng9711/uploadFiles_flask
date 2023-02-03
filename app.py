from flask import Flask, flash, redirect, render_template, request, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/Users/zhenghang/Desktop/CSCI599/uploadFiles/files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST', 'GET'])
def index():
    entries = os.listdir('/Users/zhenghang/Desktop/CSCI599/uploadFiles/files')
    return render_template("index.html", entries = entries)

@app.route('/uploader', methods=['POST', 'GET'])
def uploader():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('uploadUnsuccessful.html')
        file = request.files['file']

        if file.filename == '':
            return render_template('uploadUnsuccessful.html')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('upload.html')

        return render_template('uploadUnsuccessful.html')

    else:
        return render_template('upload.html')

@app.route('/files/<name>')
def files(name):
    return send_from_directory('/Users/zhenghang/Desktop/CSCI599/uploadFiles/files', name, as_attachment=True)

@app.route('/views/<name>')
def views(name):
    return send_from_directory('/Users/zhenghang/Desktop/CSCI599/uploadFiles/files', name, as_attachment=False)

if __name__ == '__main__':
    app.run()