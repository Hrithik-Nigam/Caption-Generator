from flask import Flask, flash, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
from Capgen import generate

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        cwd=os.getcwd()
        img_path=cwd+"\\static\\uploads\\" +file.filename
        result=generate(img_path)
        return render_template('index.html', filename=filename, output=result)


@app.route('/display/<filename>')
def display_image(filename):
    
    return redirect(url_for('static', filename='uploads/' + filename))

if __name__ == "__main__":
    app.run()