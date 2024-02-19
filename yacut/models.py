from datetime import datetime

from settings import API_FIELDS, MAX_LEN_SHORT
from yacut import db


class URLMap(db.Model):
    """
    Модель для отображения оригинальной и короткой ссылок в базе данных.
    """
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False, unique=True)
    short = db.Column(db.String(MAX_LEN_SHORT), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """
        Преобразует объект URLMap в словарь.
        """
        return dict(
            original=self.original,
            short=self.short,
        )

    def from_dict(self, data):
        """
        Заполняет объект URLMap данными из словаря.
        """
        for api_field, db_field in API_FIELDS.items():
            if api_field in data:
                setattr(self, db_field, data[api_field])
