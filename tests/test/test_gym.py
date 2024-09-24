import time
from datetime import datetime

import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from .services import HomePagePathName

moth_uz = {
    1: "Yanvar",
    2: "Fevral",
    3: "Mart",
    4: "Aprel",
    5: "May",
    6: "Iyun",
    7: "Iyul",
    8: "Avgust",
    9: "Sentabr",
    10: "Oktabr",
    11: "Noyabr",
    12: "Dekabr"
}

moth_ru = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь"
}

moth_en = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}


class ServiceTestGym:

    def setup(self, setup_url):
        try:
            send_merchant_name = setup_url.find_element(By.XPATH, "//p[text()='M39']/ancestor::button")
            send_merchant_name.click()
            button_url = setup_url.find_element(By.CLASS_NAME, 'css-f084kn')
            setup_url.execute_script('arguments[0].click();', button_url)
            time.sleep(5)
            path = setup_url.find_elements(By.XPATH, "//li[@class='MuiBox-root css-0']/child::a")
            settings_path = setup_url.find_element(By.XPATH, "//a[@class='active']")
            club_n = ""
            for item in path:
                if HomePagePathName.CLUB == item.get_attribute('href').split('/')[-1]:
                    item.click()
                    club_n = item.text
                    break

            return path, settings_path, club_n
        except NoSuchElementException:
            path = setup_url.find_elements(By.XPATH, "//li[@class='MuiBox-root css-0']/child::a")
            settings_path = setup_url.find_element(By.XPATH, "//ul[@class='MuiBox-root css-1i6zpsk']/following::a")
            club_n = ""
            for item in path:
                if HomePagePathName.CLUB == item.get_attribute('href').split('/')[-1]:
                    item.click()
                    club_n = item.text
                    break
            return path, settings_path, club_n

    def perform_search(self, setup_url, search_text):

        search_input = setup_url.find_element(By.XPATH,
                                              "//input[@class='MuiInputBase-input MuiOutlinedInput-input MuiInputBase-inputAdornedStart css-xhud73']")
        search_input.clear()
        search_input.send_keys(search_text)
        search_input.send_keys(Keys.RETURN)
        time.sleep(2)

    def get_search_result(self, setup_url):

        try:
            return setup_url.find_element(By.XPATH,
                                          "//p[@class='MuiTypography-root MuiTypography-body1 css-2kg9ww']").text
        except NoSuchElementException:
            return "Not Found"

    def clear_button(self, setup_url, action):
        clear_button = setup_url.find_element(By.XPATH, f"//p[text()='{action}']")
        clear_button.click()

    def filter_click_button(self, setup_url, action):
        time.sleep(2)
        click_button = setup_url.find_element(By.XPATH,
                                              f"//button[text()='{action}']")
        setup_url.execute_script('arguments[0].click()', click_button)

    def select_button(self, setup_url, action):
        moth_list = []
        moth = False
        for num in range(1, 13):
            month_dropdown = setup_url.find_element(By.XPATH, f"//p[text()='{action}']/following-sibling::div")
            month_dropdown.click()
            time.sleep(1)
            month_option = setup_url.find_element(By.XPATH, f"//li[@data-value='{str(num)}']")
            month_option.click()
            moth_list.append(month_option.text)

            # BU AGAR MOTH QANAQADUR  MALUMOT BO'LSA MOTH TEKSHIRADI TO'GRIMI YOKI YOQMI
            if self.get_month(setup_url) == num or self.get_month(setup_url):
                moth = True
        return moth, moth_list

    def get_month(self, setup_url):
        try:
            data = setup_url.find_element(By.XPATH,
                                          "//td[@class='MuiTableCell-root MuiTableCell-body MuiTableCell-alignLeft MuiTableCell-sizeMedium css-14hsfip'][4]")
            date_obj = datetime.strptime(data.text, "%d/%m/%Y")
            return date_obj.month
        except NoSuchElementException:
            return True

    def get_year_number(self, setup_url):
        try:
            data = setup_url.find_element(By.XPATH,
                                          "//td[@class='MuiTableCell-root MuiTableCell-body MuiTableCell-alignLeft MuiTableCell-sizeMedium css-14hsfip'][4]")
            date_obj = datetime.strptime(data.text, "%d/%m/%Y")
            return date_obj.year
        except NoSuchElementException:
            return True

    def get_years(self, setup_url, action):
        is_year = False
        for num in range(2020, 2026):
            years = setup_url.find_element(By.XPATH, f"//p[text()='{action}']/following-sibling::div")
            years.click()
            year_option = setup_url.find_element(By.XPATH, f"//li[@data-value='{str(num)}']")
            year_option.click()
            time.sleep(1)
            if self.get_year_number(setup_url) == num or self.get_year_number(setup_url):
                is_year = True
        return is_year

    def get_status(self, setup_url, action):
        setup_url.find_element(By.XPATH, "//div[@role='radiogroup']")
        try:
            active_radio_button = setup_url.find_element(By.XPATH, f"//label/span[contains(text(), '{action}')]")
            active_radio_button.click()
        except NoSuchElementException:
            return False
        time.sleep(2)
        try:
            if setup_url.find_element(By.XPATH, "//div[@class='MuiBox-root css-walian']").text == action:
                return True
            return False
        except NoSuchElementException:
            return True

    def get_common_text(self, setup_url):
        data = {
            # Sportzal
            "header_h3_title": setup_url.find_element(By.XPATH,
                                                      "//h3[@class='MuiTypography-root MuiTypography-h3 css-15xfcdg']").text,
            # ["Sportzal ro’yxati","Ro'yxatdan o'tkazish"]
            "header_button_title": [item.text for item in setup_url.find_elements(By.CLASS_NAME, 'css-tf16iz')],
            # Izlash
            "search_placeholder": setup_url.find_element(By.XPATH,
                                                         "//input[@class='MuiInputBase-input MuiOutlinedInput-input "
                                                         "MuiInputBase-inputAdornedStart css-xhud73']"),
            # Filtrlar
            "filter_text": setup_url.find_element(By.CLASS_NAME, "css-1tm6c2z").text,

            # ["Sportzal nomi","Joylashuvi","Tel. raqami","Yaratilgan sana","Funksiya"]
            "table_header": setup_url.find_elements(By.XPATH,
                                                    "//th[@class='MuiTableCell-root MuiTableCell-head MuiTableCell-sizeSmall css-9ifxpi']/child::p")

        }

        return data

    def get_filter_text_static(self, setup_url):
        text_static = {
            # Filter
            "filter_text": setup_url.find_element(By.XPATH,
                                                  "//h6[@class='MuiTypography-root MuiTypography-h6 css-1nok386']").text,

            # Filter Tozalash
            "clear_filter_text": setup_url.find_element(By.XPATH,
                                                        "//p[@class='MuiTypography-root MuiTypography-body1 css-1bok6jt']").text,

            # Oy
            "filter_month_text": setup_url.find_element(By.XPATH,
                                                        "//p[@class='MuiTypography-root MuiTypography-body1 css-3pcxby']").text,
            # Select input ichadagi So'z
            "filter_select_text": setup_url.find_element(By.XPATH,
                                                         "//p[@class='MuiTypography-root MuiTypography-bodyMd MuiTypography-noWrap css-r3prfo']").text,
            # Yil

            "filter_year_text": setup_url.find_element(By.XPATH,
                                                       "//p[@class='MuiTypography-root MuiTypography-body1 css-kr7nwi']").text,
            # Status Text

            "filter_status_text": setup_url.find_element(By.XPATH,
                                                         "//label[@class='MuiFormLabel-root MuiFormLabel-colorPrimary css-uei7ui']").text,

            # Status Activ and Inactive list
            "filter_active_inactive_text": [item.text for item in setup_url.find_elements(By.XPATH,
                                                                                          "//span[@class='MuiTypography-root MuiTypography-body1 MuiFormControlLabel-label css-2kg9ww']")]
        }

        return text_static


class TestGymUZ(ServiceTestGym):
    @pytest.fixture(autouse=True)
    def setup_login(self, setup_url, change_language, get_env_email_password, get_all_languages):
        if get_all_languages[0].text == "O’zbekcha":
            get_all_languages[0].click()
        time.sleep(1)
        email, password = get_env_email_password
        email_input = change_language["email_input_text"]
        email_input.send_keys(email)
        password_input = change_language["password_input_text"]
        password_input.send_keys(password)
        button_click = change_language["button_enter"]
        setup_url.execute_script("arguments[0].click();", button_click)
        time.sleep(3)
        return self.setup(setup_url)

    def test_search_true(self, setup_url, setup_login):
        path, settings_path, club_n = setup_login
        assert club_n == "Sportzal"
        time.sleep(2)
        self.perform_search(setup_url, "Otabek")
        result = self.get_search_result(setup_url)
        assert result == "Otabek"

    def test_search_false(self, setup_url, setup_login):
        path, settings_path, club_n = setup_login
        assert club_n != "Sp"
        time.sleep(2)
        self.perform_search(setup_url, ",fmfs/fmsfmsfm;")
        assert sorted(self.get_search_result(setup_url)) == sorted("Not Found")

    def test_filter_static_text(self, setup_url):
        self.filter_click_button(setup_url, "Filtrlar")
        time.sleep(2)
        text_static = self.get_filter_text_static(setup_url)
        assert text_static["filter_text"] == 'Filtr'
        assert text_static["clear_filter_text"] == 'Filtrni tozalash'
        assert text_static["filter_month_text"] == 'Oy'
        assert text_static["filter_select_text"] == 'Tanlang'
        assert text_static["filter_year_text"] == 'Yil'
        assert text_static["filter_status_text"] == 'Status'
        assert sorted(text_static["filter_active_inactive_text"]) == sorted(['Faol', 'Nofaol'])

    def test_filter_moth(self, setup_url):
        self.filter_click_button(setup_url, "Filtrlar")
        time.sleep(2)
        moth, moth_list = self.select_button(setup_url, "Oy")
        assert moth is True
        assert sorted(moth_list) == sorted(moth_uz.values())
        time.sleep(2)
        self.clear_button(setup_url, "Filtrni tozalash")

    def test_filter_years(self, setup_url):
        self.filter_click_button(setup_url, "Filtrlar")
        time.sleep(2)
        is_year = self.get_years(setup_url, "Yil")
        assert is_year is True
        time.sleep(2)
        self.clear_button(setup_url, "Filtrni tozalash")

    def test_filter_status_activ_valid(self, setup_url):
        self.filter_click_button(setup_url, "Filtrlar")
        time.sleep(2)
        status = self.get_status(setup_url, 'Faol')
        assert status is True

    def test_filter_status_inactive(self, setup_url):
        self.filter_click_button(setup_url, "Filtrlar")
        time.sleep(2)
        status = self.get_status(setup_url, 'Nofaol')
        assert status is True

    def test_filter_status_invalid(self, setup_url):
        self.filter_click_button(setup_url, "Filtrlar")
        time.sleep(2)
        status = self.get_status(setup_url, 'dadada')
        assert status is False

    def test_common_text(self, setup_url):
        time.sleep(2)
        common_text = self.get_common_text(setup_url)
        assert common_text["header_h3_title"] == "Sportzal"
        assert sorted(common_text["header_button_title"]) == sorted(["Sportzal ro’yxati", "Ro'yxatdan o'tkazish"])

        assert common_text["search_placeholder"].get_attribute("placeholder") == "Izlash"
        assert common_text["filter_text"] == "Filtrlar"
        print([item.text for item in common_text["table_header"]], "d,l;ad;al;la")
        assert sorted([item.text for item in common_text["table_header"]]) == sorted(
            ['Sportzal nomi', 'Joylashuvi', 'Tel. raqami', 'Yaratilgan sana', 'Funksiya'])


class TestGymRu(ServiceTestGym):
    @pytest.fixture(autouse=True)
    def setup_login(self, setup_url, change_language, get_env_email_password, get_all_languages):
        if get_all_languages[2].text == "Русский":
            get_all_languages[2].click()
        time.sleep(1)
        email, password = get_env_email_password
        email_input = change_language["email_input_text"]
        email_input.send_keys(email)
        password_input = change_language["password_input_text"]
        password_input.send_keys(password)
        button_click = change_language["button_enter"]
        setup_url.execute_script("arguments[0].click();", button_click)
        time.sleep(3)
        return self.setup(setup_url)

    def test_search_true(self, setup_url, setup_login):
        path, settings_path, club_n = setup_login
        assert club_n == "Спортзал"
        time.sleep(2)
        self.perform_search(setup_url, "Otabek")
        result = self.get_search_result(setup_url)
        assert result == "Otabek"

    def test_search_false(self, setup_url, setup_login):
        path, settings_path, club_n = setup_login
        assert club_n != "Sp"
        time.sleep(2)
        self.perform_search(setup_url, ",fmfs/fmsfmsfm;")
        assert sorted(self.get_search_result(setup_url)) == sorted("Not Found")

    def test_filter_static_text(self, setup_url):
        self.filter_click_button(setup_url, "Фильтры")
        time.sleep(2)
        text_static = self.get_filter_text_static(setup_url)
        assert text_static["filter_text"] == 'Фильтр'
        assert text_static["clear_filter_text"] == 'Очистить фильтр'
        assert text_static["filter_month_text"] == 'Месяц'
        assert text_static["filter_select_text"] == 'Выбрать'
        assert text_static["filter_year_text"] == 'Год'
        assert text_static["filter_status_text"] == 'Статус'
        assert sorted(text_static["filter_active_inactive_text"]) == sorted(['Актив', 'Неактив'])

    def test_filter_moth(self, setup_url):
        self.filter_click_button(setup_url, "Фильтры")
        time.sleep(2)
        moth, moth_list = self.select_button(setup_url, "Месяц")
        assert moth is True
        assert sorted(moth_list) == sorted(moth_ru.values())
        time.sleep(2)
        self.clear_button(setup_url, "Очистить фильтр")

    def test_filter_years(self, setup_url):
        self.filter_click_button(setup_url, "Фильтры")
        time.sleep(2)
        is_year = self.get_years(setup_url, 'Год')
        assert is_year is True
        time.sleep(2)
        self.clear_button(setup_url, "Очистить фильтр")

    def test_filter_status_activ(self, setup_url):
        self.filter_click_button(setup_url, "Фильтры")
        time.sleep(2)
        status = self.get_status(setup_url, 'Актив')
        assert status is True

    def test_filter_status_inactive(self, setup_url):
        self.filter_click_button(setup_url, "Фильтры")
        time.sleep(2)
        status = self.get_status(setup_url, 'Неактив')
        assert status is True

    def test_filter_status_invalid(self, setup_url):
        self.filter_click_button(setup_url, "Фильтры")
        time.sleep(2)
        status = self.get_status(setup_url, 'dadada')
        assert status is False

    def test_common_text(self, setup_url):
        common_text = self.get_common_text(setup_url)
        assert common_text["header_h3_title"] == "Спортзал"
        assert sorted(common_text["header_button_title"]) == sorted(["Список спортзалов", "Регистрация"])

        assert common_text["search_placeholder"].get_attribute("placeholder") == "Поиск"
        assert common_text["filter_text"] == "Фильтры"
        assert sorted([item.text for item in common_text["table_header"]]) == sorted(
            ['Название', 'Адрес спортзала', 'Контакт', 'Дата создания', 'Действия'])
        time.sleep(1)


class TestGymEn(ServiceTestGym):
    @pytest.fixture(autouse=True)
    def setup_login(self, setup_url, change_language, get_env_email_password, get_all_languages):
        if get_all_languages[1].text == "English":
            get_all_languages[1].click()
        time.sleep(1)
        email, password = get_env_email_password
        email_input = change_language["email_input_text"]

        email_input.send_keys(email)
        password_input = change_language["password_input_text"]
        password_input.send_keys(password)
        button_click = change_language["button_enter"]
        setup_url.execute_script("arguments[0].click();", button_click)
        time.sleep(2)
        return self.setup(setup_url)

    def test_search_valid(self, setup_url, setup_login):
        path, settings_path, club_n = setup_login
        assert club_n == "Gym"
        time.sleep(2)
        self.perform_search(setup_url, "Otabek")
        result = self.get_search_result(setup_url)
        assert result == "Otabek"

    def test_search_invalid(self, setup_url, setup_login):
        path, settings_path, club_n = setup_login
        assert club_n != "Sp"
        time.sleep(2)
        self.perform_search(setup_url, ",fmfs/fmsfmsfm;")
        assert sorted(self.get_search_result(setup_url)) == sorted("Not Found")

    def test_filter_static_text(self, setup_url):
        self.filter_click_button(setup_url, "Filters")
        time.sleep(2)
        text_static = self.get_filter_text_static(setup_url)
        assert text_static["filter_text"] == 'Filter'
        assert text_static["clear_filter_text"] == 'Clear filter'
        assert text_static["filter_month_text"] == 'Month'
        assert text_static["filter_select_text"] == 'Select'
        assert text_static["filter_year_text"] == 'Year'
        assert text_static["filter_status_text"] == 'Status'
        assert sorted(text_static["filter_active_inactive_text"]) == sorted(['Active', 'Inactive'])

    def test_filter_moth(self, setup_url):
        self.filter_click_button(setup_url, "Filters")
        time.sleep(2)
        moth, moth_list = self.select_button(setup_url, "Month")
        assert moth is True
        assert sorted(moth_list) == sorted(moth_en.values())
        time.sleep(2)
        self.clear_button(setup_url, "Clear filter")

    def test_filter_years(self, setup_url):
        self.filter_click_button(setup_url, "Filters")
        time.sleep(2)
        is_year = self.get_years(setup_url, 'Year')
        assert is_year is True
        time.sleep(2)
        self.clear_button(setup_url, "Clear filter")

    def test_filter_status_activ(self, setup_url):
        self.filter_click_button(setup_url, "Filters")
        time.sleep(2)
        status = self.get_status(setup_url, 'Active')
        assert status is True

    def test_filter_status_inactive(self, setup_url):
        self.filter_click_button(setup_url, "Filters")
        time.sleep(2)
        status = self.get_status(setup_url, 'Inactive')
        assert status is True

    def test_filter_status_invalid(self, setup_url):
        self.filter_click_button(setup_url, "Filters")
        time.sleep(2)
        status = self.get_status(setup_url, 'dadada')
        assert status is False

    def test_common_text(self, setup_url):
        common_text = self.get_common_text(setup_url)
        assert common_text["header_h3_title"] == "Gym"
        assert sorted(common_text["header_button_title"]) == sorted(["Gym List", "Gym Register"])

        assert common_text["search_placeholder"].get_attribute("placeholder") == "Search"
        assert common_text["filter_text"] == "Filters"
        assert sorted([item.text for item in common_text["table_header"]]) == sorted(
            ['Gym Name', 'Location', 'Contact', 'Date Created', 'Actions'])
        time.sleep(1)
