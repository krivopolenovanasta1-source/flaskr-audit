def test_home_page_available(client):
    # проверка доступности главной страницы
    response = client.get("/")
    assert response.status_code == 200


def test_login_page_available(client):
    # проверка доступности страницы авторизации
    response = client.get("/auth/login")
    assert response.status_code == 200


def test_protected_page_requires_login(client):
    # проверка ограничения доступа без авторизации
    response = client.get("/create")
    assert response.status_code == 302
    assert "/auth/login" in response.headers["Location"]


def test_unknown_page(client):
    # проверка обработки несуществующего адреса
    response = client.get("/unknown-page")
    assert response.status_code == 404
