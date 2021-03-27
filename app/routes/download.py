from base64 import b64decode
from io import BytesIO
import os
from flask import request, send_file, current_app

from modules.crypto import AES_EAX
from entities import File
from . import file_routes

@file_routes.route('/download', methods=['POST'])
def file_download():
    #database = current_app.config['database']

    file_id = request.form.get('fileId')
    original_key = request.form.get('key')
    padded_key = original_key.ljust(32, '=')[:32]

    file = File.query.filter_by(id=file_id).first()
    file_path = os.path.join(current_app.config['crypter_config']['PATH']['FILES'], file.id, file.name)

    with open(file_path, 'rb') as f:
        crypto = AES_EAX(padded_key.encode(), b64decode(file.nonce))
        plaintext = crypto.decrypt_and_verify(f.read(), b64decode(file.tag))
        if (plaintext):
            return_bytes = BytesIO(plaintext)
            return send_file(return_bytes, as_attachment=True, attachment_filename=file.name)
        else:
            return "Decrypt error"