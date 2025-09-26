import requests
import pytest
from data import token
import allure

# URL для обращения к API
BASE_URL_MOVIE = "https://kinopoiskapiunofficial.tech/api/v2.2/films/{}"
BASE_URL_COLLECTIONS = "https://kinopoiskapiunofficial.tech/api/v2.2/films/collections"
BASE_URL_FILTERS = "https://kinopoiskapiunofficial.tech/api/v2.2/films"

# Заголовки с токеном для авторизации
HEADERS = {
    'Content-Type': 'application/json',
    'X-API-KEY': token
}

@allure.step("Поиск фильма по ID")
def test_search_movie_by_id():
    """Проверяет, что поиск фильма по ID возвращает статус код 200.

    Input:
        movie_id (int): ID фильма для поиска, в данном случае 301.

    Output:
        Проверка статуса ответа (200).
    """
    movie_id = 301
    response = requests.get(BASE_URL_MOVIE.format(movie_id), headers=HEADERS)

    # Проверка статуса ответа на 200
    assert response.status_code == 200, "Status code should be 200"


@allure.step("Поиск фильмов по подборкам")
def test_search_movies_by_collection():
    """Проверяет, что поиск фильмов по подборкам возвращает статус код 200.

    Input:
        params (dict): Параметры запроса для поиска фильмов по подборкам.

    Output:
        Проверка статуса ответа (200).
    """
    params = {
        'type': 'FAMILY',
        'page': 1
    }
    response = requests.get(BASE_URL_COLLECTIONS, headers=HEADERS, params=params)

    # Проверка статуса ответа на 200
    assert response.status_code == 200, "Status code should be 200"


@allure.step("Поиск фильмов по фильтрам")
def test_search_movies_by_filters():
    """Проверяет, что поиск фильмов по фильтрам возвращает статус код 200.

    Input:
        params (dict): Параметры запроса для фильтрации фильмов.

    Output:
        Проверка статуса ответа (200).
    """
    params = {
        'countries': 34,
        'genres': 18,
        'order': 'RATING',
        'type': 'FILM',
        'ratingFrom': 5,
        'ratingTo': 10,
        'yearFrom': 2000,
        'yearTo': 2024,
        'page': 1
    }
    response = requests.get(BASE_URL_FILTERS, headers=HEADERS, params=params)

    # Проверка статуса ответа на 200
    assert response.status_code == 200, "Status code should be 200"


@allure.step("Поиск фильма с невалидным ID")
def test_search_movie_with_invalid_id():
    """Проверяет, что поиск фильма с невалидным ID возвращает статус код, отличный от 200.

    Input:
        invalid_movie_id (int): Невалидный ID фильма для поиска.

    Output:
        Проверка, что статус код не равен 200.
    """
    invalid_movie_id = 7569911  # Замените на ID, который точно не существует
    response = requests.get(BASE_URL_MOVIE.format(invalid_movie_id), headers=HEADERS)

    # Проверка, что статус код не равен 200 (например, 404)
    assert response.status_code != 200, "Status code should not be 200 for invalid movie ID"


@allure.step("Поиск фильма без токена")
def test_search_movie_without_token():
    """Проверяет, что поиск фильма без токена возвращает статус код, отличный от 200.

    Input:
        movie_id (int): ID фильма для поиска, в данном случае 301.

    Output:
        Проверка, что статус код не равен 200.
    """
    movie_id = 301
    response = requests.get(BASE_URL_MOVIE.format(movie_id))  # Без заголовка с токеном

    # Проверка, что статус код не равен 200 (например, 403 или 401)
    assert response.status_code != 200, "Status code should not be 200 without token"


# Запуск тестов при вызове pytest
if __name__ == "__main__":
    pytest.main()