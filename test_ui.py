import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import allure


@pytest.fixture
def browser() -> webdriver.Chrome:
    """
    Фикстура для инициализации драйвера Selenium.
    Returns:
        webdriver.Chrome: Объект Chrome WebDriver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(50)  # Неявное ожидание
    yield driver  # Возвращаем объект драйвера для использования в тестах
    driver.quit()  # Закрываем браузер после выполнения тестов


@allure.title("Проверка главной страницы и наличие логотипа")
@allure.description("Тест главной страницы сайта Кинопоиск, проверяется наличие логотипа.")
@allure.severity(allure.severity_level.NORMAL)
def test_homepage_loads_and_has_logo(browser: webdriver.Chrome) -> None:
    """Главная страница загружается и содержит логотип.
    Args:
        browser (webdriver.Chrome): Драйвер Chrome для взаимодействия с веб-страницей.
    """
    browser.get("https://www.kinopoisk.ru/")

    # Ожидание загрузки страницы
    WebDriverWait(browser, 15).until(EC.title_contains("Кинопоиск"))

    assert "Кинопоиск" in browser.title, f"Title: {browser.title}"

    logo = browser.find_element(By.XPATH, "//*[contains(@alt, 'Кинопоиск') or contains(@class, 'logo')]")
    assert logo.is_displayed(), "Логотип не отображается на главной странице."


@allure.title("Поиск фильма 'Темные времена' и переход к актерам")
@allure.description("Тестирует поиск фильма 'Темные времена' и проверяет переход к актерам на странице результатов.")
@allure.severity(allure.severity_level.NORMAL)
def test_search_movie(browser: webdriver.Chrome) -> None:
    """Тест поиска фильма 'Темные времена' и перехода к актерам.
    Args:
        browser (webdriver.Chrome): Драйвер Chrome для взаимодействия с веб-страницей.
    """
    # Шаг 1: Открываем сайт Кинопоиск
    browser.get("https://www.kinopoisk.ru/")

    # Шаг 2: Находим поле поиска и вводим название фильма
    search_box = WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located((By.NAME, "kp_query"))
    )
    search_box.send_keys("Темные времена")
    search_box.submit()  # Отправка формы поиска

    # Шаг 3: Ожидание загрузки результатов
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Темные времена')]"))
    )

    # Шаг 4: Находим элемент с фильмом
    movie_link = browser.find_element(By.XPATH, "//a[contains(text(), 'Темные времена')]")

    # Шаг 5: Прокрутка страницы вниз, удостоверяясь, что элемент виден
    browser.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - 100);", movie_link)

    # Вариант локатора для вкладки "Актеры"
    actors_tab = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'js-serp-metrika') and contains(@href, 'cast')]"))  # Селектор по классу и href
    )
    actors_tab.click()  # Клик по вкладке актеров

    # Проверка, что пользователь успешно на странице актеров
    assert "Темные времена" in browser.title, "Не удалось перейти на страницу актёров."


@allure.title("Проверка кнопки 'Онлайн-кинотеатр'")
@allure.description("Тестирует доступность кнопки 'Онлайн-кинотеатр'.")
@allure.severity(allure.severity_level.NORMAL)
def test_online_cinema_button(browser: webdriver.Chrome) -> None:
    """Тест проверки кнопки 'Онлайн-кинотеатр'.
    Args:
        browser (webdriver.Chrome): Драйвер Chrome для взаимодействия с веб-страницей.
    """
    # Шаг 1: Открываем сайт Кинопоиск
    browser.get("https://www.kinopoisk.ru/")

    # Шаг 2: Находим кнопку "Онлайн-кинотеатр" и кликаем на нее
    online_cinema_button = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Онлайн-кинотеатр"))  # Стабильный локатор
    )
    online_cinema_button.click()  # Переход на страницу онлайн-кинотеатра

    # Шаг 3: Ожидание загрузки страницы онлайн-кинотеатра
    WebDriverWait(browser, 15).until(
        EC.url_contains("https://hd.kinopoisk.ru/")  # Проверка URL
    )

    # Проверяем, что текущий URL соответствует ожиданию
    assert browser.current_url == "https://hd.kinopoisk.ru/", "Не удалось перейти на страницу 'Онлайн-кинотеатр'."


@allure.title("Поиск фильма 'Матрица'")
@allure.description("Тестирует поиск фильма 'Матрица'.")
@allure.severity(allure.severity_level.NORMAL)
def test_search_matrix(browser: webdriver.Chrome) -> None:
    """Тест поиска фильма 'Матрица'.
    Args:
        browser (webdriver.Chrome): Драйвер Chrome для взаимодействия с веб-страницей.
    """
    browser.get("https://www.kinopoisk.ru/")

    # Шаг 1: Находим поле поиска и вводим название фильма
    search_box = WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located((By.NAME, "kp_query"))
    )
    search_box.send_keys("Матрица")
    search_box.submit()  # Отправка формы поиска

    # Шаг 2: Ожидаем загрузку списка результатов
    WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'search_results')]"))  # Учитываем загрузку интерактивных результатов
    )

    # Шаг 3: Ищем ссылку на фильм "Матрица"
    movie_link = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Матрица')]"))
    )

    assert movie_link.is_displayed(), "Фильм 'Матрица' не найден в результатах поиска."
    movie_link.click()  # Переход к странице фильма

    # Проверка, что заголовок страницы теперь содержит "Матрица"
    assert "Матрица" in browser.title, "Не удалось перейти на страницу фильма 'Матрица'."


@allure.title("Проверка наличия постера для фильма 'Темные времена'")
@allure.description("Тестирует, что постер загружен на странице фильма 'Темные времена'.")
@allure.severity(allure.severity_level.NORMAL)
def test_movie_poster(browser: webdriver.Chrome) -> None:
    """Тест проверки наличия постера для фильма 'Темные времена'.
    Args:
        browser (webdriver.Chrome): Драйвер Chrome для взаимодействия с веб-страницей.
    """
    browser.get("https://www.kinopoisk.ru/")

    # Шаг 1: Находим поле поиска и вводим название фильма
    search_box = WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located((By.NAME, "kp_query"))
    )
    search_box.send_keys("Темные времена")
    search_box.submit()  # Отправка формы поиска

    # Шаг 2: Ожидаем загрузки результата и кликаем на фильм
    movie_link = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Темные времена')]"))
    )
    movie_link.click()  # Переход на страницу фильма

    # Шаг 3: Ожидание загрузки постера
    poster = WebDriverWait(browser, 30).until(
        EC.presence_of_element_located((By.XPATH, "//img[contains(@class, 'film-poster')]"))
    )

    # Проверка, что постер отображается на странице
    assert poster.is_displayed(), "Постер фильма 'Темные времена' не отображается на странице."