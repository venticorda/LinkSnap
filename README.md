# Проект LinkSnap

Проект LinkSnap представляет собой сервис для генерации коротких ссылок и получения оригинальных ссылок по их идентификаторам.

## Как запустить проект

Установить [uv](https://docs.astral.sh/uv/):

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Или через [PyPI](https://pypi.org/project/uv/):

```bash
# pip.
pip install uv
```

```bash
# pipx.
pipx install uv
```

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:venticorda/LinkSnap.git
```

```bash
cd LinkSnap
```

Создайте свой .env. Есть пример в env_example.


Запустить проект:
```bash
uv run python -m flask run   
```
## Использованные технологии
В проекте использовались следующие технологии:
- [Python 3.9.11](https://www.python.org/)
- [Flask 2.0.2](https://flask.palletsprojects.com/en/2.0.x/installation/#)

## Автор: 
[Даниил Варлащенко](https://github.com/venticorda)
***