from datetime import datetime

from . import db

serializer = {'url': 'original',
              'custom_id': 'short'
              }


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False, unique=True)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(

            url=self.original,
            short_link='http://localhost/' + self.short,

        )

    def to_api_get(self):
        return dict(

            url=self.original

        )

    def from_dict(self, data):

        for field in ['url', 'custom_id']:

            if field in data:
                setattr(self, serializer[field], data[field])
