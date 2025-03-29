import datetime
import random

import pytest
import requests
from faker import Faker

fake = Faker()


@pytest.fixture()
def today():
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    return today


@pytest.fixture()
def base_url():
    url = 'https://test.qa-deepen.uz/'
    # url_staging = 'https://mfit.staging-deepen.uz/'
    return url


def test_register(base_url):
    headers = {'Accept-Language': 'uz'}
    test_qa_username = ''
    test_staging_username = 'mfit@gmail.com'
    r = requests.post(base_url + 'api/v1/merchant/login/', json={'username': 'dev@gmail.com', 'password': '12345678i'},
                      headers=headers)
    assert r.status_code == 200


def test_redirect(base_url):
    headers = {'Accept-Language': 'uz'}
    login = requests.post(base_url + 'api/v1/merchant/login/',
                          json={'username': 'test@gmail.com', 'password': '12345678i'},
                          headers=headers)
    hash_ = login.json().get('results')

    hash_url = requests.post(base_url + 'api/v1/merchant/redirect/', json={'hash': hash_.get('hash')}, )
    assert hash_url.status_code == 200


@pytest.fixture()
def login(base_url):
    headers = {'Accept-Language': 'uz'}
    login = requests.post(base_url + 'api/v1/merchant/login/',
                          json={'username': 'dev@gmail.com', 'password': '12345678i'},
                          headers=headers)
    hash_ = login.json().get('results')

    hash_url = requests.post(base_url + 'api/v1/merchant/redirect/', json={'hash': hash_.get('hash')}, )
    return hash_url


def test_get_club(login, base_url):
    club = requests.get(base_url + 'api/v1/management/club-list/?is_active=1&year=2024&order=asc&sort=name',
                        cookies=login.cookies)

    assert club.status_code == 200


@pytest.fixture()
def get_club_id(login, base_url):
    club = requests.get(base_url + 'api/v1/management/club-list/?is_active=1&year=2024&order=asc&sort=name',
                        cookies=login.cookies)
    data = club.json().get('results')
    for item in data:
        if item.get('id') == 6:
            return item.get('id')
    return None


@pytest.fixture()
def gen_uz_phone():
    area_code = random.choice(['00', '01', '02'])

    # Generate the remaining 7 digits
    first = str(random.randint(100, 999))
    second = str(random.randint(10, 99))
    third = str(random.randint(10, 99))

    return '+998{}{}{}{}'.format(area_code, first, second, third)


@pytest.fixture()
def get_member_by_id(login, base_url, get_club_id, gen_uz_phone, today):
    headers = {'Accept-Language': 'uz', 'Content-Type': 'application/json', 'Club-Id': str(get_club_id)}
    response = requests.post(base_url + 'api/v1/management/member/', json={
        "first_name": fake.first_name_female(),
        "last_name": fake.last_name_female(),
        "gender": fake.random_element(["male", "female"]),
        "birth_date": "2010-02-01",
        "email": fake.company_email(),
        "phone": '+998015074411',
        "phone2": "",
        "through": 1,
        "date_joined": today,
        "description": fake.text(max_nb_chars=100),
        "address": {
            "address_line": "salom",
            "latitude": "12.11",
            "longitude": "23.11"
        }
    }, headers=headers, cookies=login.cookies)
    yield response.json()['results']['id']
    # requests.delete(base_url + f"api/v1/management/member/{response.json()['results']['id']}/",
    #                 headers=headers, cookies=login.cookies)


def test_create_member(get_club_id, base_url, login, gen_uz_phone, today):
    headers = {'Accept-Language': 'uz', 'Content-Type': 'application/json', 'Club-Id': str(get_club_id)}
    response = requests.post(base_url + 'api/v1/management/member/', json={
        "first_name": fake.first_name_female(),
        "last_name": fake.last_name_female(),
        "gender": fake.random_element(["male", "female"]),
        "birth_date": "2010-02-01",
        "email": fake.company_email(),
        "phone": "+998015074411",
        "phone2": "",
        "through": 1,
        "date_joined": today,
        "description": "<p>Lorem ipsum</p>",
        "address": {
            "address_line": "salom",
            "latitude": "12.11",
            "longitude": "23.11"
        }
    }, headers=headers, cookies=login.cookies)

    assert response.status_code == 201


def test_get_member_by_id(login, get_club_id, base_url, get_member_by_id):
    headers = {'Accept-Language': 'uz', 'Content-Type': 'application/json', 'Club-Id': str(get_club_id)}
    response = requests.get(base_url + f'api/v1/management/member/{get_member_by_id}/', cookies=login.cookies,
                            headers=headers)
    print(response.text, "TES")
    print(response.status_code)
