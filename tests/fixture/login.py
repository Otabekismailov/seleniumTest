import time

import pytest
from selenium.webdriver.common.by import By


@pytest.fixture
def change_language(setup_url):
    data = {
        "left_title_h3": setup_url.find_element(By.XPATH,
                                                '//h3[@class="MuiTypography-root MuiTypography-h3 css-gno8xn"]'),
        "left_desc_p": setup_url.find_element(By.XPATH,
                                              '//p[@class="MuiTypography-root MuiTypography-bodyXl css-a3g2vt"]'),
        "right_title_h3": setup_url.find_element(By.XPATH,
                                                 '//h3[@class="MuiTypography-root MuiTypography-h3 css-xl8q5"]'),
        "right_desc_p": setup_url.find_element(By.XPATH,
                                               '//p[@class="MuiTypography-root MuiTypography-bodyMd css-rdcnql"]'),
        "email_title": setup_url.find_element(By.XPATH,
                                              '//label[@for="email-input"]'),
        "email_input_text": setup_url.find_element(By.ID, 'email-input'),
        "password_title": setup_url.find_element(By.XPATH, '//label[@for="password-input"]'),
        "password_input_text": setup_url.find_element(By.ID, 'password-input'),
        "support_text": setup_url.find_element(By.XPATH,
                                               "//p[@class='MuiTypography-root MuiTypography-body1 css-7bioyt']"),
        "support_description": setup_url.find_element(By.XPATH,
                                                      "//div[@class='MuiBox-root css-1peu053']"),
        "button_enter": setup_url.find_element(By.CLASS_NAME, 'css-5zlwlx'),

    }

    return data


@pytest.fixture
def select_lang(setup_url):
    setup_url.find_element(By.ID, 'demo-customized-button').click()
    time.sleep(2)
    return setup_url


@pytest.fixture
def get_all_languages(select_lang):
    lang_elements = select_lang.find_elements(By.XPATH, '//li[@role="menuitem"]')
    return lang_elements
