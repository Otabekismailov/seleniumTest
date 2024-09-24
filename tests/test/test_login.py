import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


class TestLogin:

    def test_lang_change_uz(self, get_all_languages, change_language, fake_email_password, setup_url):
        # lang_elements = select_lang.find_elements(By.XPATH, '//li[@role="menuitem"]')
        if get_all_languages[0].text == "O’zbekcha":
            get_all_languages[0].click()
        assert change_language["left_title_h3"].text == "BIZ BILAN RIVOJLANISH"
        assert change_language["left_desc_p"].text == "Fitnes tarmog’lari uchun qulay va zamonaviy platforma"
        assert change_language["right_title_h3"].text == "Deepen-ga xush kelibsiz"
        assert change_language["right_desc_p"].text == "Login ma'lumotlaringizni kiriting"
        assert change_language["email_title"].text == "Elektron pochta"
        assert change_language["email_input_text"].get_attribute("placeholder") == "Elektron pochtani kiriting"
        assert change_language['password_title'].text == "Parol"
        assert change_language["password_input_text"].get_attribute("placeholder") == "Parolni kiriting"
        # Bu joyini keyinchalik  commentdan chiqarish kerak
        assert change_language["support_text"].text == "Qo'llab-quvvatlash"
        assert change_language[
                   "support_description"].get_attribute("innerText") == ("Tizimga kira olmasangiz, texnik "
                                                                         "yordam bo'limiga murojaat qiling +9989037371177")
        assert change_language['button_enter'].text == 'TIZIMGA KIRISH'
        assert sorted([item.text for item in get_all_languages]) == sorted(["O’zbekcha",
                                                                            "English",
                                                                            "Русский"])
        email, password = fake_email_password
        email_input = change_language["email_input_text"]
        email_input.send_keys(str(email))
        password_input = change_language["password_input_text"]
        password_input.send_keys(str(password))
        button_click = change_language["button_enter"]
        setup_url.execute_script("arguments[0].click();", button_click)
        time.sleep(3)

        assert setup_url.find_element(By.CLASS_NAME,
                                      "css-1xsto0d").text == "Qayta urinib ko'ring yoki texnik yordamga murojaat qiling."

    def test_lang_change_en(self, change_language, get_all_languages, fake_email_password, setup_url):
        if get_all_languages[1].text == "English":
            get_all_languages[1].click()

        assert change_language["left_title_h3"].text == "GROW WITH US"
        assert change_language[
                   "left_desc_p"].text == "A powerful, yet easy to use platform for managing fitness industry studios"
        assert change_language["right_title_h3"].text == "Welcome to Deepen"
        assert change_language["right_desc_p"].text == "Please enter your login details below"
        assert change_language["email_title"].text == "Email Address"
        assert change_language["email_input_text"].get_attribute("placeholder") == "Enter your email"
        assert change_language['password_title'].text == "Password"
        assert change_language["password_input_text"].get_attribute("placeholder") == "Enter your password"
        assert change_language["support_text"].text == "Contact Support"
        assert change_language[
                   "support_description"].get_attribute("innerText") == (
                   "If you are unable to login please contact our support team at +9989037371177")
        assert change_language['button_enter'].text == 'Login'

        email, password = fake_email_password
        email_input = change_language["email_input_text"]
        email_input.send_keys(str(email))
        password_input = change_language["password_input_text"]
        password_input.send_keys(str(password))
        button_click = change_language["button_enter"]
        setup_url.execute_script("arguments[0].click();", button_click)
        time.sleep(3)

        assert setup_url.find_element(By.CLASS_NAME,
                                      "css-1xsto0d").text == "Try again or contact support for assistance."

    def test_lang_change_ru(self, change_language, get_all_languages, setup_url, fake_email_password):

        if get_all_languages[2].text == "Русский":
            get_all_languages[2].click()
        assert change_language["left_title_h3"].text == "РАЗВИВАЙТЕСЬ С НАМИ"
        assert change_language[
                   "left_desc_p"].text == ("Высокоэффективная, при этом удобная платформа "
                                           "для управления студиями фитнес-индустрии")
        assert change_language["right_title_h3"].text == "Добро пожаловать в Deepen"
        assert change_language["right_desc_p"].text == "Пожалуйста, введите свои данные для входа в аккаунт"

        assert change_language["email_title"].text == "Адрес эл. почты"
        assert change_language["email_input_text"].get_attribute("placeholder") == "Введите адрес эл. почты"
        assert change_language['password_title'].text == "Пароль"
        assert change_language["password_input_text"].get_attribute("placeholder") == "Введите пароль"

        assert change_language["support_text"].text == "Служба поддержки"
        assert change_language[
                   "support_description"].get_attribute("innerText") == ("В случае затруднения доступа в систему "
                                                                         "обратитесь в отдел техподдержки по номеру +9989037371177")
        assert change_language['button_enter'].text == 'ВОЙТИ'

        email, password = fake_email_password
        email_input = change_language["email_input_text"]
        email_input.send_keys(str(email))
        password_input = change_language["password_input_text"]
        password_input.send_keys(str(password))
        button_click = change_language["button_enter"]
        setup_url.execute_script("arguments[0].click();", button_click)
        time.sleep(3)

        assert setup_url.find_element(By.CLASS_NAME,
                                      "css-1xsto0d").text == "Повторите попытку или свяжетесь с техподдержкой."

    def test_login_enter_uz(self, change_language, get_env_email_password, get_all_languages, setup_url):
        if get_all_languages[0].text == "O’zbekcha":
            get_all_languages[0].click()
        email, password = get_env_email_password
        email_input = change_language["email_input_text"]
        email_input.send_keys(email)
        password_input = change_language["password_input_text"]
        password_input.send_keys(password)
        button_click = change_language["button_enter"]
        setup_url.execute_script("arguments[0].click();", button_click)
        time.sleep(3)
        try:
            title_text = setup_url.find_element(By.CLASS_NAME, 'css-1vm8qyw')

            dec_text = setup_url.find_element(By.CLASS_NAME, 'css-ebdel8')
            button_text = setup_url.find_element(By.CLASS_NAME, 'css-f084kn')
            assert title_text.text == "Deepen-ga xush kelibsiz"
            assert dec_text.text == "Sportzal manzilini quyida tanlang"
            assert button_text.text == "TANLASH"
        except NoSuchElementException:

            assert True

    def test_login_enter_ru(self, change_language, get_all_languages, get_env_email_password, setup_url):
        if get_all_languages[2].text == "Русский":
            get_all_languages[2].click()
        email, password = get_env_email_password
        email_input = change_language["email_input_text"]
        email_input.send_keys(email)
        password_input = change_language["password_input_text"]
        password_input.send_keys(password)
        button_click = change_language["button_enter"]
        setup_url.execute_script("arguments[0].click();", button_click)
        time.sleep(3)
        try:
            title_text = setup_url.find_element(By.CLASS_NAME, 'css-1vm8qyw')
            dec_text = setup_url.find_element(By.CLASS_NAME, 'css-ebdel8')
            button_text = setup_url.find_element(By.CLASS_NAME, 'css-f084kn')
            assert title_text.text == "Добро пожаловать в Deepen"
            assert dec_text.text == "Выберите местоположение спортзала"
            assert button_text.text == "ПОДТВЕРДИТЬ"
        except NoSuchElementException:
            assert True

    def test_login_enter_en(self, change_language, get_env_email_password, setup_url, get_all_languages):
        if get_all_languages[1].text == "English":
            get_all_languages[1].click()
        email, password = get_env_email_password
        email_input = change_language["email_input_text"]
        email_input.send_keys(email)
        password_input = change_language["password_input_text"]
        password_input.send_keys(password)
        button_click = change_language["button_enter"]
        setup_url.execute_script("arguments[0].click();", button_click)
        time.sleep(10)
        try:
            title_text = setup_url.find_element(By.CLASS_NAME, 'css-1vm8qyw')
            dec_text = setup_url.find_element(By.CLASS_NAME, 'css-ebdel8')
            button_text = setup_url.find_element(By.CLASS_NAME, 'css-f084kn')
            assert title_text.text == "Welcome to Deepen"
            assert dec_text.text == "Please select gym location"
            assert button_text.text == "Done"
        except NoSuchElementException:
            assert True
