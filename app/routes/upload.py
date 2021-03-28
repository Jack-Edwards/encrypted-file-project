from base64 import b64encode
import os
import secrets
from flask import request, render_template, current_app, jsonify
from werkzeug.utils import secure_filename

from modules import util, disk
from modules.crypto import AES_EAX
from . import file_routes
from entities import File

@file_routes.route('/upload', methods=['POST'])
def upload():
    storage_path = current_app.config['crypter_config']['PATH']['Files']
    gb_allocated = int(current_app.config['crypter_config']['APP']['StorageLimit'])
    bytes_allocated = gb_allocated * 1024 * 1024 * 1024
    bytes_remaining_in_cloud = disk.bytes_remaining_in_cloud_storage(storage_path, bytes_allocated)

    file_from_request = request.files['files']

    # Filename must be safe
    safe_filename = secure_filename(file_from_request.filename)
    if not util.is_valid_filename(safe_filename):
        return jsonfiy({
            'success': False,
            'message': 'Invalid filename'
        })

    # Must have enough space to store the file on the server
    file_bytes = file_from_request.read()
    if len(file_bytes) >= bytes_remaining_in_cloud:
        return jsonify({
            'success': False,
            'message': 'Not enough space on server'
        })

    # Encrypt the bytes
    key = secrets.token_bytes(32)
    b64_key = b64encode(key).decode('utf-8')
    crypto = AES_EAX(key)
    ciphertext, tag = crypto.encrypt_and_digest(file_bytes)

    # Create a database entity
    database = current_app.config['database']
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

    return jsonify({
        'success': True,
        'file_id': file.id,
        'decrypt_key': b64_key
    })