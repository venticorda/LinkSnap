import random
from flask import flash, redirect, render_template, url_for
from settings import AUTO_LEN_SHORT, CHAR_SET
from . import app, db
from .forms import URLForm
from .models import URLMap

def get_unique_short_id(symbols=CHAR_SET, length=AUTO_LEN_SHORT):
    """
    Генерирует уникальный короткий идентификатор для ссылки.
    """
    result = "".join(random.choices(symbols, k=length))
    while URLMap.query.filter_by(short=result).first():
        result = "".join(random.choices(symbols, k=length))
    return result

@app.route("/", methods=["GET", "POST"])
def index_view():
    """
    Отображает форму для ввода URL и создания короткой ссылки.
    """
    form = URLForm()
    if form.validate_on_submit():
        original = form.original_link.data
        custom_id = form.custom_id.data
        if URLMap.query.filter_by(short=custom_id).first():
            flash("Предложенный вариант короткой ссылки уже существует.")
            return render_template("main.html", form=form)
        if form.custom_id.data is None or not form.custom_id.data.strip():
            custom_id = get_unique_short_id()
        else:
            custom_id = form.custom_id.data
        url_map = URLMap(original=original, short=custom_id)
        db.session.add(url_map)
        db.session.commit()
        short_url = url_for("redirect_view", short_id=url_map.short, _external=True)
        return render_template("main.html", form=form, short_url=short_url)
    return render_template("main.html", form=form)

@app.route("/<string:short_id>", methods=["GET"])
def redirect_view(short_id):
    """
    Перенаправляет короткую ссылку на оригинальный URL.
    """
    url_mapping = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(url_mapping.original)
