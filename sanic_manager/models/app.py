# coding=utf-8
# __author__ = 'Mio'
from sanic_manager.settings import db, app
from sanic_manager.utils.gtz import datetime_2_isoformat, utc_now_dt


class App(db.Model):
    __tablename__ = 'apps'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    version = db.Column(db.Integer)
    platform = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=False, index=True)
    file = db.Column(db.String(50))

    creator = db.Column(db.String(50))

    create_at = db.Column(db.DateTime(timezone=True), default=utc_now_dt)
    update_at = db.Column(db.DateTime(timezone=True), default=utc_now_dt, onupdate=utc_now_dt)

    _idx_name_version_platform_unique = db.Index('idx_name_version_platform_unique', 'name', 'version', 'platform', unique=True)

    def __repr__(self):
        return '{}<{}>'.format(self.name, self.id)

    def json_format(self):
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "platform": self.platform,
            "is_active": self.is_active,
            # 不支持历史下载
            "file": app.url_for('static', name='uploads', filename=self.file),
            # "file": self.file,
            "create_at": datetime_2_isoformat(self.create_at) if self.create_at else None
        }
