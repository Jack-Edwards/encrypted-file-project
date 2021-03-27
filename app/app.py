from pathlib import Path
from modules import settings, disk
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

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
app.config['crypter_config'] = config

db = SQLAlchemy(app)
from entities import File
db.create_all()
app.config['database'] = db

@app.route('/', methods=['GET'])
def index():
    gb_allocated = int(app.config['crypter_config']['APP']['StorageLimit'])
    storage_path = app.config['crypter_config']['PATH']['Files']

    bytes_allocated = gb_allocated * 1024 * 1024 * 1024

    bytes_remaining = disk.bytes_remaining_in_cloud_storage(storage_path, bytes_allocated)
    percent_remaining = round(100 * (bytes_remaining / bytes_allocated), 0)

    nice_bytes_remaining = disk.bytes_to_nice_string(bytes_remaining)

    return render_template('index.html',
                            percentDiskRemaining=percent_remaining,
                            bytesDiskRemaining=nice_bytes_remaining,
                            bytesDiskAllocated=f'{round(gb_allocated, 2)} GB')

from routes import file_routes
app.register_blueprint(file_routes, url_prefix='/file')

if __name__ == '__main__':
    app.run(debug=True)
