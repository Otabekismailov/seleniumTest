import os

import dotenv
import environs
import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

from .fixture import *  # noqa


@pytest.fixture(scope="session")
def browser():
    # Adjust path to your ChromeDriver executable
    options = Options()
    options.add_argument('--headless')
    server = ChromeService(executable_path='/Users/credo_market/PycharmProjects/seleniumDeepenTest/chromedriver')
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


@pytest.fixture
def get_env_email_password():
    dotenv.load_dotenv('.env')
    # email = os.environ.get("QA_EMAIL")
    # password = os.environ.get("QA_PASSWORD")
    # email = os.environ.get("STAGING_EMAIL")
    # password = os.environ.get("STAGING_PASSWORD")
    email = os.environ.get("DEV_EMAIL")
    password = os.environ.get("DEV_PASSWORD")

    return email, password


@pytest.fixture
def fake_email_password():
    email = "test@terg.com"
    password = "123456"
    return email, password


@pytest.fixture
def setup_url(browser):
    browser.get('https://auth.qa-deepen.uz/auth/sign-in')
    # browser.get('https://login.staging-deepen.uz/auth/sign-in')
    return browser


@pytest.fixture(scope="session")
def db():
    env = environs.Env()
    env.read_env()
    connection = psycopg2.connect(
        dbname=os.getenv('NAMEDB'),
        user=os.getenv('USERDB'),
        password=os.getenv('PASSWORDDB'),
        host=os.getenv('hostdb'),
        port=os.getenv('port')
    )

    yield connection
    connection.close()



