import time
import math
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Список ссылок для параметризации
LINKS = [
    "https://stepik.org/lesson/236895/step/1",
    "https://stepik.org/lesson/236896/step/1",
    "https://stepik.org/lesson/236897/step/1",
    "https://stepik.org/lesson/236898/step/1",
    "https://stepik.org/lesson/236899/step/1",
    "https://stepik.org/lesson/236903/step/1",
    "https://stepik.org/lesson/236904/step/1",
    "https://stepik.org/lesson/236905/step/1"
]

EMAIL = "valeriyalat56@gmail.com"
PASSWORD = "POIU0987poiu"


@pytest.fixture(scope="function")
def browser():
    print("\nstart browser for test..")
    browser = webdriver.Chrome()
    yield browser
    print("\nquit browser..")
    browser.quit()


@pytest.mark.parametrize('link', LINKS)
def test_aliens_message(browser, link):
    browser.get(link)

    # --- Авторизация ---
    login_link = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Войти"))
    )
    login_link.click()

    email_field = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "id_login_email"))
    )
    email_field.send_keys(EMAIL)

    password_field = browser.find_element(By.ID, "id_login_password")
    password_field.send_keys(PASSWORD)

    submit_button = browser.find_element(By.CSS_SELECTOR, "button.btn-success")
    submit_button.click()

    # --- Небольшая пауза, чтобы страница перезагрузилась после входа ---
    time.sleep(3)

    # --- Ввод правильного ответа ---
    answer_field = WebDriverWait(browser, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea"))
    )
    answer_field.clear()  # поле перед вводом должно быть пустым
    answer = str(math.log(int(time.time())))
    answer_field.send_keys(answer)

    # --- Нажимаем "Отправить" ---
    submit_button = browser.find_element(By.CSS_SELECTOR, "button.submit-submission")
    submit_button.click()

    # --- Ждём фидбек и проверяем текст ---
    feedback_element = WebDriverWait(browser, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "pre.smart-hints__hint"))
    )
    feedback_text = feedback_element.text

    assert feedback_text == "Correct!", \
        f"Ожидался 'Correct!', но получен: '{feedback_text}'"
