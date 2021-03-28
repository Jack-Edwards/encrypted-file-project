from pathlib import Path
from modules import settings
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import shutil
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

def delete_stale_files():
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    files = File.query.filter(File.created <= one_day_ago).all()
    for file in files:
        print(f'Deleting file: {file.id}')
        print(f'Created: {file.created}')
        print(f'Now: {datetime.utcnow()}')
        file_dir = os.path.join(app.config['crypter_config']['PATH']['Files'], file.id)
        try:
            shutil.rmtree(file_dir)
        except FileNotFoundError:
            continue
        db.session.delete(file)

    if (len(files) > 0):
        db.session.commit()

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(delete_stale_files, 'interval', minutes=5)
scheduler.start()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

from routes import file_routes, metrics_routes
app.register_blueprint(file_routes, url_prefix='/file')
app.register_blueprint(metrics_routes, url_prefix='/metrics')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=False)
