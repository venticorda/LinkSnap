import os
import re
import string


class Config(object):
    """
    Конфигурационные параметры приложения.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI", default="sqlite:///db.sqlite3"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")


MAX_LEN_SHORT = 16
AUTO_LEN_SHORT = 6
REGEX_SHORT = re.compile(r"^[A-Za-z0-9]+$")

API_FIELDS = {"url": "original", "custom_id": "short"}

CHAR_SET = string.ascii_letters + string.digits
