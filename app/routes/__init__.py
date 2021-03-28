from flask import Blueprint

file_routes = Blueprint('file_routes', __name__)
metrics_routes = Blueprint('metrics_routes', __name__)

from .upload import *
from .download import *
from .metrics import *