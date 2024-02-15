from http import HTTPStatus

from flask import jsonify, request, url_for

from settings import MAX_LEN_SHORT, REGEX_SHORT

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route("/api/id/", methods=("POST",))
def create_url():
    """
    Создает новую короткую ссылку на основе предоставленного URL.
    Входные данные:
    - url: обязательное поле, представляющее оригинальную ссылку
    - custom_id (опционально): пользовательский идентификатор короткой ссылки
    """
    data = request.get_json()

    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса", HTTPStatus.BAD_REQUEST)
    if "url" not in data:
        raise InvalidAPIUsage(
            '"url" является обязательным полем!', HTTPStatus.BAD_REQUEST
        )

    if (
        "custom_id" in data
        and data["custom_id"] is not None
        and data["custom_id"].strip()
    ):
        if (
            len(data["custom_id"]) > MAX_LEN_SHORT
            or REGEX_SHORT.search(data["custom_id"]) is None
        ):
            raise InvalidAPIUsage(
                "Указано недопустимое имя для короткой ссылки", HTTPStatus.BAD_REQUEST
            )
    else:
        short = get_unique_short_id()
        data["custom_id"] = short

    if URLMap.query.filter_by(short=data["custom_id"]).first() is not None:
        raise InvalidAPIUsage(
            "Предложенный вариант короткой ссылки уже существует.",
            HTTPStatus.BAD_REQUEST,
        )

    url = URLMap(original=data["url"], short=data["custom_id"])
    db.session.add(url)
    db.session.commit()

    return (
        jsonify(
            {
                "url": url.to_dict()["original"],
                "short_link": url_for("index_view", _external=True)
                + url.to_dict()["short"],
            }
        ),
        HTTPStatus.CREATED,
    )


@app.route("/api/id/<string:short_id>/", methods=("GET",))
def get_url(short_id):
    """
    Получает оригинальную ссылку по заданному короткому идентификатору.
    Входные данные:
    - short_id: обязательное поле, представляющее короткий идентификатор ссылки
    """
    short_url = URLMap.query.filter_by(short=short_id).first()
    if short_url is None:
        raise InvalidAPIUsage("Указанный id не найден", HTTPStatus.NOT_FOUND)
    return jsonify({"url": short_url.to_dict()["original"]}), HTTPStatus.OK
