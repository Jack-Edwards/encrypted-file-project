from base64 import b64encode
import os
from flask import request, render_template, current_app
from werkzeug.utils import secure_filename

from modules import util
from modules.crypto import AES_EAX
from . import file_routes
from entities import File

@file_routes.route('/upload', methods=['POST'])
def upload():
    database = current_app.config['database']

    file_from_request = request.files['files']
    original_key = request.form.get('key')
    padded_key = original_key.ljust(32, '=')[:32]

    # Filename must be safe
    safe_filename = secure_filename(file_from_request.filename)
    if not util.is_valid_filename(safe_filename):
        return redirect(url_for('index'))

    # Encrypt the file bytes
    file_bytes = file_from_request.read()
    crypto = AES_EAX(padded_key.encode())
    ciphertext, tag = crypto.encrypt_and_digest(file_bytes)

    # Create a database entity
    file = File(safe_filename)
    file.nonce = b64encode(crypto.nonce).decode('utf-8')
    file.tag = b64encode(tag).decode('utf-8')
    database.session.add(file)
    database.session.commit()

    # Make a directory for the file
    file_dir = os.path.join(current_app.config['crypter_config']['PATH']['FILES'], file.id)
    os.mkdir(file_dir)

    with open(os.path.join(file_dir, safe_filename), 'wb') as f:
        f.write(ciphertext)

    return render_template('fileDetails.html',
                            file_id=file.id,
                            decrypt_key=original_key)