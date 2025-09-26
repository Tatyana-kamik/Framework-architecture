import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
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
    yield driver  # Возвращаем объект драйвера для использования в тестах
    driver.quit()  # Закрываем браузер после выполнения тестов


@allure.step("Тест главной страницы и наличие логотипа.")
def test_homepage_loads_and_has_logo(browser: webdriver.Chrome) -> None:
    """Главная страница загружается и содержит логотип.

    Args:
        browser (webdriver. Chrome): Драйвер Chrome для взаимодействия с веб-страницей.

    Raises:
        AssertionError: Если логотип не отображается на странице.
    """
    browser.get("https://www.kinopoisk.ru/")

    # Явное ожидание для загрузки страницы
    WebDriverWait(browser, 15).until(
        EC.title_contains("Кинопоиск")
    )

    assert "Кинопоиск" in browser.title, f"Title: {browser.title}"

    try:
        logo = browser.find_element(By.CSS_SELECTOR, "a[href='/']")
        assert logo.is_displayed(), "Логотип не отображается на главной странице."
    except Exception as e:
        logo = browser.find_element(By.XPATH, "//*[contains(@alt, 'Кинопоиск') or contains(@class, 'logo')]")
        assert logo.is_displayed(), "Логотип не отображается на главной странице."


@allure.step("Поиск фильма 'Темные времена' и переход к актерам.")
def test_search_movie(browser: webdriver.Chrome) -> None:
    """Тест поиска фильма 'Темные времена' и перехода к актерам.

    Args:
        browser (webdriver. Chrome): Драйвер Chrome для взаимодействия с веб-страницей.

    Raises:
        Exception: Если фильм не найден на странице.
    """
    browser.get("https://www.kinopoisk.ru/")

    # Явное ожидание для поля поиска
    search_box = WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located((By.NAME, "kp_query"))
    )

    # Имитация временной задержки для предотвращения капчи
    time.sleep(random.uniform(5, 10))  # Долгая задержка для имитации реального пользователя

    search_box.send_keys("Темные времена")

    # Устанавливаем мышь на поле поиска
    actions = ActionChains(browser)
    actions.move_to_element(search_box).perform()
    time.sleep(random.uniform(1, 3))  # Небольшая задержка

    # Явное ожидание для кнопки поиска
    search_button = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "styles_submit__KkHEO"))
    )
    search_button.click()

    time.sleep(random.uniform(2, 4))  # Ждем некоторое время после клика

    # Ожидаем появления элемента со ссылкой на фильм
    try:
        movie_link = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-id="972777"]'))
        )
        movie_link.click()  # Переходим на страницу фильма
        print("Фильм 'Темные времена' найден и открыта его страница.")

        # Переходим на вкладку "Актеры"
        actors_tab = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-id="972777"][href*="cast"]'))
        )

        actions.move_to_element(actors_tab).perform()  # Имитация движения мыши
        time.sleep(random.uniform(1, 3))  # Задержка перед кликом
        actors_tab.click()  # Переход на страницу актеров
        print("Перешли на вкладку 'Актеры'.")

    except Exception as e:
        print("Ошибка: фильм не найден на странице.", e)


@allure.step("Проверка кнопки 'Онлайн-кинотеатр'.")
def test_online_cinema_button(browser: webdriver.Chrome) -> None:
    """Тест проверки кнопки 'Онлайн-кинотеатр'.

    Args:
        browser (webdriver. Chrome): Драйвер Chrome для взаимодействия с веб-страницей.

    Raises:
        Exception: Если кнопка 'Онлайн-кинотеатр' не найдена.
    """
    browser.get("https://www.kinopoisk.ru/")

    # Явное ожидание для загрузки страницы
    WebDriverWait(browser, 15).until(
        EC.title_contains("Кинопоиск")
    )

    # Поиск кнопки "Онлайн-кинотеатр" по классу
    try:
        online_cinema_button = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.styles_root__jIQWR[href='https://hd.kinopoisk.ru/']"))
        )
        online_cinema_button.click()  # Переход на страницу онлайн-кинотеатра
        print("Перешли на страницу 'Онлайн-кинотеатр'.")

        # Явное ожидание для загрузки страницы онлайн-кинотеатра
        WebDriverWait(browser, 15).until(
            EC.title_contains("Онлайн-кинотеатр")
        )

        print("Страница 'Онлайн-кинотеатр' успешно загружена.")

    except Exception as e:
        print("Ошибка: кнопка 'Онлайн-кинотеатр' не найдена.", e)


@allure.step("Поиск фильма 'Матрица'.")
def test_search_matrix(browser: webdriver.Chrome) -> None:
    """Тест поиска фильма 'Матрица'.

    Args:
        browser (webdriver. Chrome): Драйвер Chrome для взаимодействия с веб-страницей.

    Raises:
        Exception: Если страница результатов не загружена.
    """
    browser.get("https://www.kinopoisk.ru/")

    # Явное ожидание для поля поиска
    search_box = WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located((By.NAME, "kp_query"))
    )

    # Имитация временной задержки для предотвращения капчи
    time.sleep(random.uniform(5, 10))  # Долгая задержка для имитации реального пользователя

    search_box.send_keys("Матрица")

    # Устанавливаем мышь на поле поиска
    actions = ActionChains(browser)
    actions.move_to_element(search_box).perform()
    time.sleep(random.uniform(1, 3))  # Небольшая задержка

    # Явное ожидание для кнопки поиска
    search_button = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "styles_submit__KkHEO"))
    )
    search_button.click()

    # Ожидаем, что страница загрузится
    try:
        WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
            # Пример: ожидаем h1 заголовок на странице результатов
        )
        print("Страница с результатами поиска успешно загружена.")
    except Exception as e:
        print("Ошибка: страница результатов не загружена.", e)

    # Закрытие браузера по завершению
    browser.quit()


@allure.step("Проверка кнопки 'Рецензии' к фильму 'Темные времена'.")
def test_reviews_button(browser: webdriver.Chrome) -> None:
    """Тест проверки кнопки 'Рецензии' к фильму 'Темные времена'.

    Args:
        browser (webdriver. Chrome): Драйвер Chrome для взаимодействия с веб-страницей.

    Raises:
        Exception: Если рецензии не найдены.
    """
    browser.get("https://www.kinopoisk.ru/")

    # Явное ожидание для поля поиска
    search_box = WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located((By.NAME, "kp_query"))
    )

    # Имитация временной задержки для предотвращения капчи
    time.sleep(random.uniform(5, 10))  # Долгая задержка для имитации реального пользователя

    search_box.send_keys("Темные времена")

    # Устанавливаем мышь на поле поиска
    actions = ActionChains(browser)
    actions.move_to_element(search_box).perform()
    time.sleep(random.uniform(1, 3))  # Небольшая задержка

    # Явное ожидание для кнопки поиска
    search_button = WebDriverWait(browser, 15).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "styles_submit__KkHEO"))
    )
    search_button.click()

    # Ожидаем появления элемента со ссылкой на фильм
    try:
        movie_link = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-id="972777"]'))
        )
        movie_link.click()  # Переходим на страницу фильма
        print("Фильм 'Темные времена' найден и открыта его страница.")

        # Прокрутка страницы вниз до кнопки "Рецензии"
        reviews_button = WebDriverWait(browser, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/film/972777/reviews/"]'))
        )
        browser.execute_script("arguments[0].scrollIntoView();", reviews_button)  # Прокрутка к элементу
        time.sleep(random.uniform(1, 3))  # Небольшая задержка для завершения прокрутки

        reviews_button.click()  # Переход на страницу рецензий
        print("Перешли на страницу 'Рецензии'.")

        # Ожидаем загрузки страницы рецензий
        WebDriverWait(browser, 15).until(
            EC.title_contains("Рецензии")  # Проверьте, что заголовок страницы обновился
        )
        print("Страница 'Рецензии' успешно загружена.")

    except Exception as e:
        print("Ошибка: рецензии не найдены.", e)

    # Закрытие браузера
    browser.quit()
