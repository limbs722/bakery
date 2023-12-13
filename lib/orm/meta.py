from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from croft.lib.orm.camel import Camel
from datetime import datetime


class Meta(object):

    @declared_attr
    def __tablename__(cls):
        return Camel()(cls.__name__)

    dbid = Column(Integer, primary_key=True, autoincrement='auto')
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def dict(self):
        return {
           c.name: getattr(self, c.name) for c in self.__table__.columns
        }


def metabase(meta=Meta):

    return declarative_base(cls=meta)
