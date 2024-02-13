from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp
from settings import MAX_LEN_SHORT, REGEX_SHORT

class URLForm(FlaskForm):
    """
    Форма для ввода URL и создания короткой ссылки.
    """
    original_link = URLField(
        "Введите ссылку",
        validators=(
            DataRequired(message="Обязательное поле"),
            URL(message="Неправильная ссылка"),
        ),
    )
    custom_id = StringField(
        "Введите короткую ссылку",
        validators=(
            Length(
                max=MAX_LEN_SHORT,
                message=f"Длина ссылки не должна превышать {MAX_LEN_SHORT} символов",
            ),
            Optional(),
            Regexp(
                regex=REGEX_SHORT,
                message="Указано недопустимое имя для короткой ссылки",
            ),
        ),
    )
    submit = SubmitField("Сократить")
    