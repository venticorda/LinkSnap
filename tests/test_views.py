import pytest

from LinkSnap.models import URLMap

py_url = 'https://www.python.org'


def test_index_form_get(client):
    got = client.get('/')
    assert got.status_code == 200, (
        'GET-запрос к главной странице должен возвращать статус `200`.'
    )
    assert b'form' in got.data, (
        'Добавьте форму в конекст страницы `index`'
    )


def test_index_form_post(client):
    got = client.post('/', data={
        'original_link': py_url,
        'custom_id': 'py',
    })
    assert got.status_code == 200, (
        'При отправке формы главная страница должна возвращать статус `200`'
    )
    unique_id = URLMap.query.filter_by(original=py_url, short='py').first()
    assert unique_id, (
        'После отправки формы в базе данных должна создаваться новая запись.'
    )
    assert '<a href="http://localhost/py"' in got.data.decode('utf-8'), (
        'После отправки формы на главной странице должна отобразиться '
        'созданная ссылка.'
    )


def test_duplicated_url_in_form(client, short_python_url):
    got = client.post('/', data={
        'original_link': py_url,
        'custom_id': 'py',
    }, follow_redirects=True)
    assert (
        'Предложенный вариант короткой ссылки уже существует.'
        in got.data.decode('utf-8')
    ), (
        'Если полученное в запросе короткое имя для ссылки уже занято - на '
        'главной странице после отправки формы должен отобразиться текст '
        '"Предложенный вариант короткой ссылки уже существует."'
    )


def test_get_unique_short_id(client):
    got = client.post('/', data={
        'original_link': py_url,
    })
    assert got.status_code == 200, (
        'При отправке формы без заданного значения короткой ссылки '
        'главная страница должна вернуть статус-код `200`'
    )
    unique_id = URLMap.query.filter_by(original=py_url).first()
    assert unique_id, (
        'При отправке формы без заданного значения короткой ссылки '
        'в базе данных должна создаваться новая запись.'
    )
    assert (
        f'Ваша новая ссылку готова: http://localhost:5000/{unique_id.short}'
    ), (
        'После отправки формы без заданного значения короткой ссылки '
        'на главной странице должна быть отображена созданная ссылка.'
    )


def test_redirect_url(client, short_python_url):
    got = client.get(f'/{short_python_url.short}')
    assert got.status_code == 302, (
        'При перенаправлении по короткому адресу убедитесь, что возвращается '
        'статус-код `302`'
    )
    assert got.location == short_python_url.original, (
        'При перенаправлении по короткому адресу убедитесь в корректности '
        'оригинального адреса'
    )


def test_len_short_id_form(client):
    long_string = (
        'CuriosityisnotasinHarryHoweverfromtimetotimeyoushouldexercisecaution'
    )
    got = client.post('/', data={
        'original_link': py_url,
        'custom_id': long_string,
    })
    assert 'Ваша новая ссылка готова' not in got.data.decode('utf-8'), (
        'Если через форму отправлено имя короткой ссылки длиннее 16 символов '
        '- на странице должно отобразиться сообщение об ошибке.'
    )


def test_len_short_id_autogenerated_view(client):
    client.post('/', data={
        'original_link': py_url,
    })
    unique_id = URLMap.query.filter_by(original=py_url).first()
    assert len(unique_id.short) == 6, (
        'Если в форме не указана короткая ссылка - '
        'должна генерироваться короткая ссылка длинной 6 символов.'
    )


@pytest.mark.parametrize('data', [
    ({'url': py_url, 'custom_id': '.,/!?'}),
    ({'url': py_url, 'custom_id': 'Hodor-Hodor'}),
    ({'url': py_url, 'custom_id': 'h@k$r'}),
    ({'url': py_url, 'custom_id': '$'}),
])
def test_invalid_short_url(data, client):
    client.post('/', data=data)
    unique_id = URLMap.query.filter_by(original=py_url).first()
    assert not unique_id, (
        'В короткой ссылке должно быть разрешено использование строго '
        'определённого набора символов. Обратитесь к тексту задания.'
    )
