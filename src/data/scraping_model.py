from data.database import db
from datetime import datetime

class ScrapingResult(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    status = db.Column(db.String(20), nullable=False, default='pending')
    result = db.Column(db.PickleType, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())