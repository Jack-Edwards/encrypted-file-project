from pathlib import Path
from modules import settings
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
    gb_allocated = float(app.config['crypter_config']['APP']['StorageLimit'])
    
    bytes_used = 0
    start_path = app.config['crypter_config']['PATH']['Files']
    for path, dirs, files in os.walk(start_path):
        for f in files:
            fp = os.path.join(path, f)
            bytes_used += os.path.getsize(fp)

    bytes_allocated = gb_allocated * 1024 * 1024 * 1024
    percent_remaining = 100 - (100 * (bytes_used / bytes_allocated))
    bytes_remaining = bytes_allocated - bytes_used

    labels = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    label_index = 0
    while (bytes_remaining > 1024):
        bytes_remaining /= 1024
        label_index += 1

    return render_template('index.html',
                            percentDiskRemaining=round(percent_remaining, 1),
                            bytesDiskRemaining=f'{round(bytes_remaining, 2)} {labels[label_index]}',
                            bytesDiskAllocated=f'{round(gb_allocated, 2)} GB')

from routes import file_routes
app.register_blueprint(file_routes, url_prefix='/file')

if __name__ == '__main__':
    app.run(debug=True)
