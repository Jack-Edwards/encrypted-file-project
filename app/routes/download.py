from base64 import b64decode
from io import BytesIO
import shutil
import os
from flask import request, send_file, current_app, jsonify, render_template

from modules.crypto import AES_EAX
from entities import File
from . import file_routes

@file_routes.route('/download', methods=['POST'])
def file_download():
    database = current_app.config['database']

    file_id = request.form.get('fileId')
    key = b64decode(request.form.get('key'))
    if len(key) != 32:
        return render_template('downloadError.html', reason='decrypt error')

    file = File.query.filter_by(id=file_id).first()

    if file is None:
        return render_template('downloadError.html', reason='not found')

    file_dir = os.path.join(current_app.config['crypter_config']['PATH']['FILES'], file.id)
    file_path = os.path.join(file_dir, file.name)

    crypto = AES_EAX(key, b64decode(file.nonce))

    with open(file_path, 'rb') as f:
        plaintext = crypto.decrypt_and_verify(f.read(), b64decode(file.tag))
        if (plaintext):
            shutil.rmtree(file_dir)
            database.session.delete(file)
            database.session.commit()
            return_bytes = BytesIO(plaintext)
            return send_file(return_bytes, as_attachment=True, attachment_filename=file.name)
        else:
            return render_template('downloadError.html', reason='decrypt error')
