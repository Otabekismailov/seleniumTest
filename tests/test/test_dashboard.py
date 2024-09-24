import time

import pytest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .services import HomePagePathName


class DashboardService:
    def setub_dashboard(self, setup_url):
        try:
            send_merchant_name = setup_url.find_element(By.XPATH, "//p[text()='Taşkent']/ancestor::button")
            send_merchant_name.click()
            button_url = setup_url.find_element(By.CLASS_NAME, 'css-f084kn')
            setup_url.execute_script('arguments[0].click();', button_url)
            time.sleep(2)
            dashboard_text = ""
            path = setup_url.find_elements(By.XPATH, "//li[@class='MuiBox-root css-0']/child::a")
            settings_path = setup_url.find_element(By.XPATH, "//a[@class='active']")
            for item in path:
                if HomePagePathName.DASHBOARD == item.get_attribute('href').split('/')[-1]:
                    item.click()
                    dashboard_text = item.text
                    break
            return path, settings_path, dashboard_text

        except NoSuchElementException:
            path = setup_url.find_elements(By.XPATH, "//li[@class='MuiBox-root css-0']/child::a")
            settings_path = setup_url.find_element(By.XPATH, "//ul[@class='MuiBox-root css-1i6zpsk']/following::a")
            dashboard_text = ""
            for item in path:
                if HomePagePathName.DASHBOARD == item.get_attribute('href').split('/')[-1]:
                    item.click()
                    dashboard_text = item.text
                    break
            return path, settings_path, dashboard_text

    def get_members_color(self, setup_url):
        wait = WebDriverWait(setup_url, 10)
        button_members = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                "//button[contains(@class, 'MuiTab-root') and "
                                                                "contains(@class, 'Mui-selected') and"
                                                                " contains(@class, 'css-1e2pbx6')]")))
        button_members.click()
        try:
            sector_pgk = setup_url.find_element(By.XPATH, "//*[name()='path' and @name='Package']")
            sector_class = setup_url.find_element(By.XPATH, "//*[name()='path' and @name='Class']")
            return [sector_pgk.get_attribute('fill'), sector_class.get_attribute('fill'), button_members.text]
        except NoSuchElementException:
            return ["Not Found", button_members.text]

    def get_members_pkg_and_cls_name(self, setup_url):
        try:
            # cls yoki pkg bo'lmasa
            pkg_names = setup_url.find_elements(By.XPATH,
                                                "//p[@class='MuiTypography-root MuiTypography-body1 css-1tbtvx7']")

            return [item.text for item in pkg_names]

        except NoSuchElementException as e:
            try:
                # cls bo'lsa va pkg bo'lmasa

                pkg_name = setup_url.find_element(By.XPATH,
                                                  "//p[@class='MuiTypography-root MuiTypography-body1 css-1tbtvx7']")
                cls_name = setup_url.find_element(By.XPATH,
                                                  "//p[@class='MuiTypography-root MuiTypography-body1 css-1qyt6u7']")
                return [cls_name.text, pkg_name.text]
            except NoSuchElementException:
                try:
                    # pkg bo'lsa ham class bo'lsa

                    new = [item.text for item in setup_url.find_elements(By.XPATH,
                                                                         "//p[@class='MuiTypography-root MuiTypography-body1 css-1qyt6u7']")]
                    return new
                except NoSuchElementException:
                    # pkg bo'lsa  va cls bo'lmasa
                    pkg_name = setup_url.find_element(By.XPATH,
                                                      "//p[@class='MuiTypography-root MuiTypography-body1 css-1qyt6u7']")
                    cls_name = setup_url.find_element(By.XPATH,
                                                      "//p[@class='MuiTypography-root MuiTypography-body1 css-1tbtvx7']")
                    return [cls_name.text, pkg_name.text]

    def get_members_common(self, setup_url):
        data = {
            "pkg_cls_sum": setup_url.find_elements(By.XPATH,
                                                   "//p[@class='MuiTypography-root MuiTypography-bodyXxl css-1g8daas']"),
            "h_4_title": setup_url.find_elements(By.CLASS_NAME, "css-15ibv0l"),
            "male_and_female": setup_url.find_elements(By.XPATH,
                                                       "//div[@class='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-lg-1.3 "
                                                       "css-zptm22']/child::p[1]"),
            "week": setup_url.find_element(By.XPATH, "//button[@value='week']"),
            "month": setup_url.find_element(By.XPATH, "//button[@value='month']"),
            "members_round_count_text": setup_url.find_element(By.CLASS_NAME, "css-1sju51s"),

        }
        return data

    def get_sales(self, setup_url):
        sales_click = setup_url.find_element(By.XPATH,
                                             "//button[@class='MuiButtonBase-root MuiTab-root MuiTab-textColorSecondary css-1e2pbx6']")
        sales_text = sales_click.text
        sales_click.click()
        time.sleep(2)
        data = {
            "h_4_title_payment": setup_url.find_element(By.CLASS_NAME, "css-gpqyb4").text,
            "h_4_title_abonement": setup_url.find_element(By.CLASS_NAME, "css-vnups8").text,
            "h_4_title_statis": setup_url.find_element(By.CLASS_NAME, "css-12j020v").text,
            "payment_method": setup_url.find_elements(By.XPATH,
                                                      "//p[@class='MuiTypography-root MuiTypography-bodySm css-15s1mdl']"),
            "payment_method_UZS": setup_url.find_elements(By.XPATH,
                                                          "//p[@class='MuiTypography-root MuiTypography-bodySm css-1wv8n4b']"),
            "sales_sum_text": setup_url.find_element(By.XPATH,
                                                     "//p[@class='MuiTypography-root MuiTypography-bodyMd css-130xuen']").text,
            "sales_sum_pkg": setup_url.find_element(By.XPATH,
                                                    "//p[@class='MuiTypography-root MuiTypography-bodySm css-14173ym']").text.split(
                "  ")[0],
            "pkg_text": setup_url.find_element(By.XPATH,
                                               "//p[@class='MuiTypography-root MuiTypography-body1 MuiTypography-noWrap css-qqkm3j']").text,
            "pkg_title": setup_url.find_element(By.XPATH,
                                                "//p[@class='MuiTypography-root MuiTypography-body1 MuiTypography-noWrap css-qqkm3j']").get_attribute(
                "title"),
            "pkg_name_and_cls_name": setup_url.find_elements(By.XPATH,
                                                             "//p[@class='MuiTypography-root MuiTypography-bodySm css-l6mz95']"),
            "sales_text": sales_text,
        }
        return data


class TestDashboardUz(DashboardService):
    @pytest.fixture(autouse=True)
    def setup_login(self, setup_url, change_language, get_env_email_password, get_all_languages):
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
        return self.setub_dashboard(setup_url)

    def test_dashboard_client(self, setup_login, setup_url):
        path, settings_path, dashboard_text = setup_login
        sector = self.get_members_color(setup_url)
        assert dashboard_text == "Analitika"
        assert sorted(sector) == sorted(['#664AEA', '#16A34A', "Mijozlar"]) or sorted(sector) == sorted(
            ["Not Found", "Mijozlar"])
        time.sleep(4)
        cls_and_cls_name = self.get_members_pkg_and_cls_name(setup_url)
        print(cls_and_cls_name, ",dl;mal;dma;ldma;ld")
        assert sorted(cls_and_cls_name) == sorted(['Mashg’ulot', 'Abonement'])
        common_text = self.get_members_common(setup_url)
        pkg_cls_sum_int = [int(item.text) for item in common_text['pkg_cls_sum']]

        assert common_text['week'].text == 'Hafta'
        assert common_text['month'].text == 'Oy'
        setup_url.execute_script('arguments[0].click()', common_text['month'])
        time.sleep(2)
        setup_url.execute_script('arguments[0].click()', common_text['week'])
        assert sorted([item.text for item in common_text['male_and_female']]) == sorted(['Erkak', 'Ayol'])
        assert sorted([item.text for item in common_text['h_4_title']]) == sorted(
            ['Demografiya', 'Mijozlar', 'Tashriflar'])
        assert all(isinstance(item, int) for item in pkg_cls_sum_int)
        assert common_text['members_round_count_text'].text == "Jami"
        time.sleep(2)

    def test_dashboard_sales(self, setup_url):
        sales = self.get_sales(setup_url)
        assert sales['h_4_title_payment'] == "To’lovlar"
        assert sales['h_4_title_abonement'] == "Abonementlar"
        assert sales['h_4_title_statis'] == "Statistika"
        assert sorted(set([item.text for item in sales['payment_method_UZS']])) == sorted(["(UZS)"])
        assert sorted([item.text for item in sales['payment_method']]) == sorted(
            ["Karta", "Terminal", "Naqd", "Hisob o‘tkazma"])
        assert sales['sales_sum_text'] == "Jami"
        assert sales['sales_sum_pkg'] == "Sotuv jami"
        assert sales['pkg_title'] == sales['pkg_text']
        assert sorted([item.text for item in sales['pkg_name_and_cls_name'] if item.text != '']) == sorted(
            ["Mashg’ulot", "Abonement"])


class TestDashboardRu(DashboardService):
    @pytest.fixture(autouse=True)
    def setup_login(self, setup_url, change_language, get_env_email_password, get_all_languages):
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
        return self.setub_dashboard(setup_url)

    def test_dashboard_client(self, setup_login, setup_url):
        path, settings_path, dashboard_text = setup_login
        sector = self.get_members_color(setup_url)
        assert dashboard_text == "Аналитика"
        assert sorted(sector) == sorted(['#664AEA', '#16A34A', "Клиенты"]) or sorted(sector) == sorted(
            ["Not Found", "Клиенты"])
        time.sleep(2)
        cls_and_cls_name = self.get_members_pkg_and_cls_name(setup_url)
        assert sorted(cls_and_cls_name) == sorted(['Классы', 'Aбонементы'])
        common_text = self.get_members_common(setup_url)
        pkg_cls_sum_int = [int(item.text) for item in common_text['pkg_cls_sum']]

        assert common_text['week'].text == 'Неделя'
        assert common_text['month'].text == 'Месяц'
        setup_url.execute_script('arguments[0].click()', common_text['month'])
        time.sleep(2)
        setup_url.execute_script('arguments[0].click()', common_text['week'])
        assert sorted([item.text for item in common_text['male_and_female']]) == sorted(['Мужской', 'Женский'])
        assert sorted([item.text for item in common_text['h_4_title']]) == sorted(
            ['Демография', 'Клиенты', 'Посещаемость'])
        assert all(isinstance(item, int) for item in pkg_cls_sum_int)
        assert common_text['members_round_count_text'].text == "Всего"
        time.sleep(2)

    def test_dashboard_sales(self, setup_url):
        sales = self.get_sales(setup_url)
        assert sales['sales_text'] == "Продажи"
        assert sales['h_4_title_payment'] == "Платежи"
        assert sales['h_4_title_abonement'] == "Абонементы"
        assert sales['h_4_title_statis'] == "Статистика продаж"
        assert sorted(set([item.text for item in sales['payment_method_UZS']])) == sorted(["(UZS)"])
        assert sorted([item.text for item in sales['payment_method']]) == sorted(
            ["Перевод", "Терминал", "Наличные", "Перечисление"])
        assert sales['sales_sum_text'] == "Общая сумма"
        assert sales['sales_sum_pkg'] == "Сумма продаж"
        assert sales['pkg_title'] == sales['pkg_text']
        assert sorted([item.text for item in sales['pkg_name_and_cls_name'] if item.text != '']) == sorted(
            ['Абонементы', 'Занятия'])


class TestDashboardEn(DashboardService):
    @pytest.fixture(autouse=True)
    def setup_login(self, setup_url, change_language, get_env_email_password, get_all_languages):
        if get_all_languages[1].text == "English":
            get_all_languages[1].click()
        email, password = get_env_email_password
        email_input = change_language["email_input_text"]
        email_input.send_keys(email)
        password_input = change_language["password_input_text"]
        password_input.send_keys(password)
        button_click = change_language["button_enter"]
        setup_url.execute_script("arguments[0].click();", button_click)
        time.sleep(2)
        return self.setub_dashboard(setup_url)

    def test_dashboard_client(self, setup_login, setup_url):
        path, settings_path, dashboard_text = setup_login
        sector = self.get_members_color(setup_url)
        assert dashboard_text == "Dashboard"
        assert sorted(sector) == sorted(['#664AEA', '#16A34A', "Members"]) or sorted(sector) == sorted(
            ["Not Found", "Members"])
        time.sleep(2)
        cls_and_cls_name = self.get_members_pkg_and_cls_name(setup_url)
        assert sorted(cls_and_cls_name) == sorted(['Class member', 'Package member'])
        common_text = self.get_members_common(setup_url)
        pkg_cls_sum_int = [int(item.text) for item in common_text['pkg_cls_sum']]

        assert common_text['week'].text == 'Week'
        assert common_text['month'].text == 'Month'
        setup_url.execute_script('arguments[0].click()', common_text['month'])
        time.sleep(2)
        setup_url.execute_script('arguments[0].click()', common_text['week'])
        assert sorted([item.text for item in common_text['male_and_female']]) == sorted(['Female', 'Male'])
        assert sorted([item.text for item in common_text['h_4_title']]) == sorted(
            ['Members', 'Demographics', 'Attendance'])
        assert all(isinstance(item, int) for item in pkg_cls_sum_int)
        assert common_text['members_round_count_text'].text == "Total"
        time.sleep(2)

    def test_dashboard_sales(self, setup_url):
        sales = self.get_sales(setup_url)
        assert sales['sales_text'] == 'Sales'
        assert sales['h_4_title_payment'] == "Payments"
        assert sales['h_4_title_abonement'] == "Packages"
        assert sales['h_4_title_statis'] == "Sales summary"
        assert sorted(set([item.text for item in sales['payment_method_UZS']])) == sorted(["(UZS)"])
        assert sorted([item.text for item in sales['payment_method']]) == sorted(
            ["Cash", "Card", "Terminal", "Funds transfer"])
        assert sales['sales_sum_text'] == "Total sales"
        assert sales['sales_sum_pkg'] == "Total sold"
        assert sales['pkg_title'] == sales['pkg_text']
        assert sorted([item.text for item in sales['pkg_name_and_cls_name'] if item.text != '']) == sorted(
            ['Class', 'Package'])
