from flask import Blueprint

file_routes = Blueprint('file_routes', __name__)

from .upload import *
from .download import *