from pathlib import Path
from modules import settings
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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
    return render_template('index.html')

from routes import file_routes
app.register_blueprint(file_routes, url_prefix='/file')

if __name__ == '__main__':
    app.run(debug=True)
