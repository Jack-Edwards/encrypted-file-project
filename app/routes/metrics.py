from flask import jsonify, current_app

from modules import disk

from . import metrics_routes

@metrics_routes.route('/space', methods=['GET'])
def get_space():
    gb_allocated = int(current_app.config['crypter_config']['APP']['StorageLimit'])
    storage_path = current_app.config['crypter_config']['PATH']['Files']

    bytes_allocated = gb_allocated * 1024 * 1024 * 1024

    bytes_remaining = disk.bytes_remaining_in_cloud_storage(storage_path, bytes_allocated)
    percent_remaining = round(100 * (bytes_remaining / bytes_allocated), 0)

    nice_bytes_remaining = disk.bytes_to_nice_string(bytes_remaining)

    return jsonify({
        'success': True,
        'percent_remaining': percent_remaining,
        'bytes_remaining': nice_bytes_remaining,
        'bytes_allocated': f'{round(gb_allocated, 2)} GB'
    })