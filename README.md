# Проект YaCut

Проект YaCut представляет собой сервис для генерации коротких ссылок и получения оригинальных ссылок по их идентификаторам.

## Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ViaDo1orosa/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Запустить проект:
```
flask run
```
## Использованные технологии
В проекте использовались следующие технологии:
- [Python 3.9.11](https://www.python.org/)
- [Flask 2.0.2](https://flask.palletsprojects.com/en/2.0.x/installation/#)

## Автор: 
[Даниил Варлащенко](https://github.com/ViaDo1orosa)
***