# coding=utf-8
# __author__ = 'Mio'
from datetime import datetime

from sanic_manager.settings import db
from sqlalchemy import DateTime, Column


class App(db.Model):
    __tablename__ = 'apps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    version = db.Column(db.Integer)
    platform = db.Column(db.String(20))
    is_latest = db.Column(db.Boolean, default=False, index=True)

    creator = db.Column(db.String(50))

    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '{}<{}>'.format(self.nickname, self.id)

    def json_format(self):
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "is_latest": self.is_latest
        }
