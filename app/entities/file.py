import base64
import os
import re
import uuid
from datetime import datetime

from app import db


class File(db.Model):
    id: str
    name: str
    nonce: str
    tag: str
    created: datetime

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    nonce = db.Column(db.String, nullable=False)
    tag = db.Column(db.String, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.name = name
