from flask import Flask, \
    render_template, \
    request, \
    redirect, \
    url_for, \
    send_file, \
    jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import os

import settings
import util

# Load settings
this_file = Path(__file__)
app_directory = this_file.parent.absolute()
project_directory = app_directory.parent.absolute()
config = settings.load_from_file(project_directory, 'settings.ini')


# Prepare Flask
app = Flask(__name__)
app.secret_key = config['APP']['SecretKey']
app.config['SQLALCHEMY_DATABASE_URI'] = config['PATH']['Database']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Prepare the database
db = SQLAlchemy(app)
from entities import File


#  Create the DB file
db.create_all()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/file/upload', methods=['POST'])
def file_upload():
    file_from_request = request.files['file']
    safe_filename = secure_filename(file_from_request.filename)

    if not util.is_valid_filename(safe_filename):
        return redirect(url_for('index'))

    # Add the file details to the database
    file = File(safe_filename)
    db.session.add(file)
    try:
        file_dir = os.path.join(config['PATH']['FILES'], file.id)
        os.mkdir(file_dir)
        file_from_request.save(os.path.join(file_dir, safe_filename))
    except:
        db.session.delete(file)
    finally:
        db.session.commit()

    return render_template('fileDetails.html',
                            file_id=file.id,
                            file_name=file.name,
                            file_created=file.created)


@app.route('/file/download', methods=['POST'])
def file_download():
    file_id = request.form.get('fileId')
    file = File.query.filter_by(id=file_id).first()
    file_directory = os.path.join(config['PATH']['FILES'], file.id)
    for found in os.listdir(file_directory):
        file_path = os.path.join(file_directory, found)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            print(file_path)
            return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
