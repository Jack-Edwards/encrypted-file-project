from flask import Flask, \
    render_template, \
    request, \
    redirect, \
    url_for, \
    send_file
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path
import os
from io import BytesIO
from modules import settings, util
from modules.crypto import SymmetricCrypto
from base64 import b64encode, b64decode

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


# Create the DB file
db.create_all()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/file/upload', methods=['POST'])
def file_upload():
    file_from_request = request.files['files']
    key = request.form.get('key')

    # Filename must be safe
    safe_filename = secure_filename(file_from_request.filename)
    if not util.is_valid_filename(safe_filename):
        return redirect(url_for('index'))

    # Encrypt the file bytes
    file_bytes = file_from_request.read()
    crypto = SymmetricCrypto(key.encode())
    encrypted_bytes = crypto.encrypt(file_bytes)

    # Create a database entity
    file = File(safe_filename)
    db.session.add(file)
    db.session.commit()

    # Make a directory for the file
    file_dir = os.path.join(config['PATH']['FILES'], file.id)
    os.mkdir(file_dir)

    with open(os.path.join(file_dir, safe_filename), 'wb') as f:
        f.write(encrypted_bytes)

    return render_template('fileDetails.html',
                            file_id=file.id,
                            decrypt_key=key,
                            decrypt_iv=b64encode(crypto.iv).decode('utf-8'))


@app.route('/file/download', methods=['POST'])
def file_download():
    file_id = request.form.get('fileId')
    decrypt_key = request.form.get('key').encode()
    decrypt_iv = b64decode(request.form.get('iv'))
    file = File.query.filter_by(id=file_id).first()
    file_path = os.path.join(config['PATH']['FILES'], file.id, file.name)
    with open(file_path, 'rb') as f:
        crypto = SymmetricCrypto(decrypt_key, decrypt_iv)
        decrypted_bytes = crypto.decrypt(f.read())
        return_bytes = BytesIO(decrypted_bytes)
        return send_file(return_bytes, as_attachment=True, attachment_filename=file.name)


if __name__ == '__main__':
    app.run(debug=True)
