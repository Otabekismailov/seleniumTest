import datetime
import logging
import random
import time

import requests
from faker import Faker

from Text_file import address_tashkent_2

fake = Faker()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def gen_uz_phone_number():
    area_code = random.choice(['00', '01', '02'])

    # Generate the remaining 7 digits
    first = str(random.randint(100, 999))
    second = str(random.randint(10, 99))
    third = str(random.randint(10, 99))

    return '+998{}{}{}{}'.format(area_code, first, second, third)


class MethodRole:
    STAFF = 'staff'
    CLUB = 'club'
    PACKAGE = 'package'
    ROOM = 'room'
    MEMBER = 'member'
    CLASS = 'class'
    PAYMENT_LIST = 'payment_list'
    PAYMENT_PACKAGE = 'payment_package'
    PAYMENT_CLASS = 'payment_class'
    GRUPCHEKIN_PKG = 'groupchekin_pkg'
    GRUPCHEKIN_CLASS = 'groupchekin_class'
    CHEKIN = 'chekin'
    NOTIFY = 'notify'


class QaServices:
    def __init__(self, base_url, club_id, pkg_id):
        self.base_url = base_url
        # self.username = '24deepen.demo@deepen.uz'
        # self.password = 'SViIY14_aryo'

        # self.username = 'test.prod@deepen.uz'
        # self.password = 'PRPrD(24payi'

        # self.username = 'yscomplex.qa@deepen.uz'
        #
        # self.password = '12345678i'

        # self.username = 'mrx@deepen.qa'
        # self.password = '12345678i'

        # self.username = 'kozim@deepen.uz'
        # self.password = '12345678aN'
        #
        self.username = '1fit@deepen.qa'
        self.password = '12345678i'

        # self.username = 'kozimjon@gmail.com'
        # self.password = '12345678i'
        self.club_id = club_id
        self.pkg_id = pkg_id
        self.request = requests
        self.headers = {'Content-Type': 'application/json', 'Accept-Language': 'uz', "Club-id": self.club_id}
        self.token_cookies = self.login()  # Login natijasini keshlaymiz
        self.request_count = 0
        self.success_requests = 0
        self.total_time = 0
        self.today = datetime.datetime.today().strftime("%Y-%m-%d")
        self.country = "UZB"

    def login(self):
        try:
            response = self.request.post(f'{self.base_url}api/v1/merchant/login/',
                                         json={'username': self.username, 'password': self.password,
                                               "country": "UZB"},
                                         headers=self.headers)
            response.raise_for_status()
            token = response.json().get('results')
            hash_response = self.request.post(f'{self.base_url}api/v1/merchant/redirect/',
                                              json={'hash': token.get('hash')},
                                              headers=self.headers)
            hash_response.raise_for_status()
            print("Login successful:", hash_response.status_code)
            return hash_response.cookies
        except requests.RequestException as e:
            print(f"Login error: {e}")
            return None

    def send_request(self, method, url, data=None, ids=None):
        try:
            start_time = time.time()
            if method == 'get':
                response = self.request.get(f"{self.base_url}{url}", headers=self.headers, cookies=self.token_cookies)

            elif method == 'post':
                response = self.request.post(f"{self.base_url}{url}", json=data, headers=self.headers,
                                             cookies=self.token_cookies)
                print(response.status_code)
            elif method == 'patch':
                response = self.request.patch(f"{self.base_url}{url}{ids}/", json=data, headers=self.headers,
                                              cookies=self.token_cookies)
            elif method == 'delete':
                response = self.request.delete(f"{self.base_url}{url}", headers=self.headers,
                                               cookies=self.token_cookies)
            else:
                raise ValueError("Unsupported method")

            end_time = time.time()
            self.request_count += 1
            self.total_time += (end_time - start_time)
            if response.status_code in {200, 201}:
                self.success_requests += 1
                logging.info(f"Status code : {response.status_code}")
                return response.json()
            else:
                logging.error(f"Request error, status code: {response.status_code} and Error: {response.json()} ")

                return None
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None

    def fun_method(self, fun, method, url, data=None):
        if method == 'get':
            fun(20, url, method)
        elif method == 'post':
            fun(10, url, method)
        elif method == 'patch':
            # Agar data ro‘yxat yoki iterable bo‘lsa:
            fun(len(data), url, method)
        elif method == 'delete':
            fun(1, url, method)

    def get_avg_response_time(self, url, method, action=None):
        self.request_count = 0
        self.success_requests = 0
        self.total_time = 0

        if action == MethodRole.CLUB:
            self.fun_method(self.club_crud, method, url, self.get_club_list())
        elif action == MethodRole.STAFF:
            self.fun_method(self.staff_crud, method, url, self.get_staff_list())
        elif action == MethodRole.PACKAGE:
            self.fun_method(self.package_crud, method, url, self.get_package_list())
        elif action == MethodRole.ROOM:
            self.fun_method(self.room_crud, method, url, self.get_room_list())
        elif action == MethodRole.CLASS:
            self.fun_method(self.class_crud, method, url, self.get_class_list())
        elif action == MethodRole.MEMBER:
            self.fun_method(self.member_crud, method, url, self.get_member_list())
        elif action == MethodRole.PAYMENT_PACKAGE:
            self.fun_method(fun=self.payment_register_pkg, method=method, url=url)
        elif action == MethodRole.PAYMENT_CLASS:
            self.fun_method(fun=self.payment_register_cls, method=method, url=url)
        elif action == MethodRole.GRUPCHEKIN_PKG:
            self.fun_method(self.grup_chekin_register_pkg, method, url)
        elif action == MethodRole.GRUPCHEKIN_CLASS:
            self.fun_method(self.grup_chekin_register_cls, method, url)
        elif action == MethodRole.CHEKIN:
            pass
        elif action == MethodRole.NOTIFY:
            self.fun_method(self.notification_register, method, url)

        avg_response_time = self.total_time / self.success_requests if self.success_requests > 0 else float('inf')
        return {'avg_response_time': f"{avg_response_time:.2f}", 'Total requests sent': self.request_count}

    # TODO CLUB CRUD
    def club_crud(self, repeat, url, method):
        if method == 'post':
            logging.info("POST action for CLUB started...")
            for _ in range(repeat):
                self.send_request(method, url, self.club_data())
        elif method == 'patch':
            logging.info("PATCH action for CLUB started...")
            club_lists = self.get_club_list()[:2]
            for ids in range(len(club_lists)):
                self.send_request(method, url, self.club_data(), ids=club_lists[ids].get("id"))
        elif method == 'delete':
            logging.info("DELETE action for CLUB started...")
            club_lists = self.get_club_list()[:2]
            for ids in range(len(club_lists)):
                self.send_request(method, url, self.member_data(), ids=club_lists[ids].get("id"))
        elif method == 'get':
            logging.info("GET action for CLUB started...")
            for _ in range(repeat):
                self.send_request(method, url)

    def get_club_list(self):
        return \
            self.request.get(f"{self.base_url}api/v1/management/club-list/?is_active=1&year=2024&order=asc&sort=name",
                             headers=self.headers,
                             cookies=self.token_cookies).json()['results']

    # TODO STAFF CRUD
    def staff_crud(self, repeat, url, method):
        if method == 'post':
            logging.info("POST action for Staff started...")
            for _ in range(repeat):
                self.send_request(method, url, self.staff_data())
        elif method == 'patch':
            logging.info("PATCH action for Staff started...")
            staff_lists = self.get_staff_list()
            for ids in range(len(staff_lists)):
                self.send_request(method, url, self.club_data(), ids=staff_lists[ids].get("id"))
        elif method == 'delete':
            logging.info("DELETE action for Staff started...")
            staff_lists = self.get_staff_list()
            for ids in range(len(staff_lists)):
                self.send_request(method, url, self.member_data(), ids=staff_lists[ids].get("id"))
        elif method == 'get':
            logging.info("GET action for Staff started...")
            for _ in range(repeat):
                self.send_request(method, url)

    def get_staff_list(self):
        return self.request.get(f"{self.base_url}api/v1/staffs/?page=1&per_page=100", headers=self.headers,
                                cookies=self.token_cookies).json()['results']

    # TODO PACKAGE CRUD
    def package_crud(self, repeat, url, method):
        if method == 'post':
            logging.info("POST action for Package started...")
            for _ in range(repeat):
                self.send_request(method, url, self.package_data())
        elif method == 'patch':
            logging.info("PATCH action for Package started...")
            package_lists = self.get_package_list()
            for ids in range(len(package_lists)):
                self.send_request(method, url, self.package_data(), ids=package_lists[ids].get("id"))
        elif method == 'delete':
            logging.info("DELETE action for Package started...")
            package_lists = self.get_package_list()
            for ids in range(len(package_lists)):
                self.send_request(method, url, self.package_data(), ids=package_lists[ids].get("id"))
        elif method == 'get':
            logging.info("GET action for Package started...")
            for _ in range(repeat):
                self.send_request(method, url)

    def get_package_list(self):
        response = self.request.get(
            f"{self.base_url}api/v1/management/package-list/?page=1&per_page=10",
            headers=self.headers,
            cookies=self.token_cookies
        )

        # Check for successful response
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch package list, status code: {response.status_code}")

        pkg = response.json().get("results", [])
        pkg_list = [
            item for item in pkg
            if "club" in item and item["club"].get("id") == int(self.headers.get("Club-id"))
        ]
        return pkg_list

    # TODO ROOM CRUD
    def room_crud(self, repeat, url, method):
        if method == 'post':
            logging.info("POST action for Room started...")
            for _ in range(repeat):
                self.send_request(method, url, self.room_data())
        elif method == 'patch':
            logging.info("PATCH action for Room started...")
            room_lists = self.get_room_list()
            for ids in range(len(room_lists)):
                self.send_request(method, url, self.room_data(), ids=room_lists[ids].get("id"))
        elif method == 'delete':
            logging.info("DELETE action for Room started...")
            room_lists = self.get_room_list()
            for ids in range(len(room_lists)):
                self.send_request(method, url, self.room_data(), ids=room_lists[ids].get("id"))
        elif method == 'get':
            logging.info("GET action for Room started...")
            for _ in range(repeat):
                self.send_request(method, url)

    def get_room_list(self):
        return self.request.get(f"{self.base_url}api/v1/management/room-list/?is_active=1", headers=self.headers,
                                cookies=self.token_cookies).json().get('results', [])

    # TODO Class CRUD
    def class_crud(self, repeat, url, method):
        if method == 'post':
            logging.info("POST action for Class started...")
            for _ in range(repeat):
                self.send_request(method, url, self.class_data())
        elif method == 'patch':
            logging.info("PATCH action for Class started...")
            class_lists = self.get_class_list()
            for ids in range(len(class_lists)):
                self.send_request(method, url, self.class_data(), ids=class_lists[ids].get("id"))
        elif method == 'delete':
            logging.info("DELETE action for Class started...")
            class_lists = self.get_class_list()
            for ids in range(len(class_lists)):
                self.send_request(method, url, self.class_data(), ids=class_lists[ids].get("id"))
        elif method == 'get':
            logging.info("GET action for Room started...")
            for _ in range(repeat):
                self.send_request(method, url)

    def get_class_list(self):
        return self.request.get(f"{self.base_url}api/v1/management/class-list/?page=1&per_page=100",
                                headers=self.headers, cookies=self.token_cookies).json().get("results", [])

    # TODO MEMBER CRUD
    def member_crud(self, repeat, url, method):
        if method == 'post':
            logging.info("POST action for MEMBER started...")
            for _ in range(repeat):
                print(self.member_data(), "MEMBERS")
                self.send_request(method, url, self.member_data())
        elif method == 'patch':
            logging.info("PATCH action for MEMBER started...")
            member_list = self.get_member_list()
            for ids in range(len(member_list)):
                self.send_request(method, url, self.member_data(), ids=member_list[ids].get("id"))

        elif method == 'delete':
            logging.info("DELETE action for MEMBER started...")
            member_list = self.get_member_list()
            for ids in range(len(member_list)):
                self.send_request(method, url, self.member_data(), ids=member_list[ids].get("id"))
        elif method == 'get':
            logging.info("GET action for MEMBER started...")
            for _ in range(repeat):
                self.send_request(method, url)

    def get_member_list(self):
        # TODO FAQAT DRAFT USER KELADI
        return self.request.get(f"{self.base_url}api/v1/management/member-list/?status=draft", headers=self.headers,
                                cookies=self.token_cookies).json().get("results", [])

    def get_member_list_noti(self):

        return self.request.get(f"{self.base_url}api/v1/management/member-list/", headers=self.headers,
                                cookies=self.token_cookies).json().get("results", [])

    # TODO PAYMENT  REGISTER  USER  DRAFT

    def payment_register_pkg(self, count, url, method):
        if method == 'post':
            logging.info("POST action for Payment Package started...")
            for item in self.payment_package_data():
                self.send_request(method, url, item)
        elif method == 'get':
            logging.info("GET action for Payment started...")
            for _ in range(20):
                self.send_request(method, url)

    def payment_register_cls(self, count, url, method):
        if method == 'post':
            logging.info("POST action for Payment Class started...")
            for item in self.payment_class_data():
                self.send_request(method, url, item)
        elif method == 'get':
            logging.info("GET action for Payment started...")
            for _ in range(20):
                self.send_request(method, url)

    def payment_list(self):
        payment = self.request.get(f'{self.base_url}api/v1/management/payment-list/?page=1&per_page=100', self.headers,
                                   cookies=self.token_cookies).json().get('results', [])
        return payment

    def grup_chekin_register_pkg(self, repeat, url, method):
        plan_register = []

        for i in self.grup_chekin_data_pkg():
            plan = self.request.get(
                f"{self.base_url}api/v1/check-in/group-checkin/{i.get('id')}/?subscription=1&page=1&per_page=20",
                headers=self.headers, cookies=self.token_cookies).json().get(
                "results", [])

            if plan:
                for item in plan:
                    plan_register.append({"plan": item.get('id')})

        print(plan_register, "Plans Registered")
        self.send_request(method, url, plan_register)

    def grup_chekin_register_cls(self, repeat, url, method):
        plan_register = []
        for i in self.grup_chekin_data_pkg():
            plan = self.request.get(
                f"{self.base_url}api/v1/check-in/group-checkin/{i.get('id')}/?subscription=2&page=1&per_page=20",
                headers=self.headers, cookies=self.token_cookies).json().get(
                "results", [])

            if plan:
                for item in plan:
                    plan_register.append({"plan": item.get('id')})

        print(plan_register, "Plans Registered")
        self.send_request(method, url, plan_register)

    def notification_register(self, repeat, url, method):
        logging.info("POST action for Notification started...")
        for i in range(repeat):
            self.send_request(method, url, self.notifation_data())

    def check_in_register(self):
        pass

    # TODO DATA

    def member_data(self):
        return {
            "first_name": fake.random_element([fake.first_name_female(), fake.first_name_male()]),
            "last_name": fake.random_element([fake.last_name_female(), fake.last_name_male()]),
            "gender": fake.random_element(["male", "female"]),
            "birth_date": fake.date_of_birth().strftime("%Y-%m-%d"),
            "email": fake.company_email(),
            "phone": gen_uz_phone_number(),
            "phone2": "",
            "through": fake.random_element([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]),
            "date_joined": self.today,
            "description": fake.text(),
            "address": fake.random_element([item for item in address_tashkent_2])}

    def club_data(self):
        return {
            "email": fake.company_email(),
            "name": fake.company(),
            "is_active": fake.random_element([True, False]),
            "phone": gen_uz_phone_number(),
            "conditions": f"<p>{fake.text()}</p>",
            "address": fake.random_element([item for item in address_tashkent_2])
        }

    def staff_data(self):
        club_list_data = [item.get('id') for item in self.get_club_list()]
        return {
            "first_name": fake.random_element([fake.first_name_female(), fake.first_name_male()]),
            "last_name": fake.random_element([fake.last_name_female(), fake.last_name_male()]),
            "gender": fake.random_element(["male", "female"]),
            "birth_date": fake.date_of_birth().strftime("%Y-%m-%d"),
            "email": fake.email(),
            "phone": gen_uz_phone_number(),
            # "avatar": fake.random_element([1, 23, 44, 55, 66, 77, 88]),
            "clubs": club_list_data,
            "role": fake.random_element([2, 3, 4, 5]),
            "is_active": fake.random_element([True, False]),
            "password": fake.password()

        }

    def package_data(self):
        membership_packages = [
            "Basic Fitness Pass",
            "Active Lifestyle Plan",
            "Premium Performance",
            "Family Fitness Bundle",
            "Student Strength Saver",
            "Elite Wellness Package",
            "Ultimate Gym Access",
            "Pro Athlete Membership",
            "Flex & Fit Club",
            "Champion's Choice Plan"
        ]
        return {
            "name": fake.random_element(membership_packages),
            "price": fake.random_element([1000000, 400000, 700000, 100000]),
            "days": fake.random_element([10, 40, 360, 90]),
            "visit": fake.random_element([20, 4, 55, 11, 33, 44]),
            "start_time": fake.date_time().strftime("%H:%M"),
            "end_time": fake.date_time().strftime("%H:%M"),
            "description": fake.text(),
            "is_active": True,
            "is_global": fake.random_element([True, False])
        }

    def room_data(self):
        return {"club": int(self.headers.get("Club-id")),
                "is_active": fake.random_element([True, False]),
                "description": fake.text(),
                "name": fake.random_element([
                    "Strength Studio",
                    "Flex Zone",
                    "Cardio Lab",
                    "Powerhouse",
                    "Zen Den",
                    "Endurance Room",
                    "Recovery Lounge",
                    "The Grind",
                    "Pulse Room",
                    "The Hive"
                ]
                )}

    def class_data(self):
        return {"name": fake.random_element([
            "Marathon Training",
            "Martial Arts",
            "Meditation Session",
            "Muscle Building",
            "Mountain Biking",
            "Mobility Drills",
            "Mixed Martial Arts (MMA)",
            "Mini Triathlon",
            "Mindful Yoga",
            "Mountain Climbing"
        ]),
            "club": int(self.headers.get("Club-id")),
            "description": fake.text(),
            "period": 28,
            "is_active": fake.random_element([True, False]),
            "price": fake.random_element([1000000, 400000, 700000, 100000]),
            "room": fake.random_element([item.get("id") for item in self.get_room_list()]),
            "slot": fake.random_int(),
            # "subtotal": fake.random_element([1000000,400000,700000,100000]),
            # "total": fake.random_element([1000000,400000,700000,100000]),
            "trainer": fake.random_element(
                [item.get("id") for item in self.get_staff_list() if item.get("role") == 'trainer'])
        }

    def payment_package_data(self):
        payment_list_data = []
        pkg_plan = self.get_package_list()
        for i in self.get_member_list():
            payment_list_data.append({
                "customer": i.get('id'),
                "discount_amount": 0,
                "discount_reason": "",
                "discount_value": 0,
                "payment_date": self.today,
                "payment_method": "terminal",
                "payments": [{"amount": 1000000, "payment_method": "terminal"}],
                "start_date": self.today,
                "subscription": {"type": 1,
                                 "plan": self.pkg_id,
                                 "club": int(self.club_id)},
                "subtotal": 1000000,
                "total": 1000000,
            })
        return payment_list_data

    def payment_class_data(self):

        """
            customer:60
            discount_amount:0
            discount_reason:""
            discount_value:0
            payment_date:"2024-12-13"
            payment_method:"transfer"
            payments:[0:{amount: 1000000, payment_method: "transfer"}]
            subscription: {type: 2, plan: "9", club: null}
            subtotal: 1000000
            total: 1000000

        :return:
        """
        payment_list_data = []
        for i in self.get_member_list():
            payment_list_data.append({
                "customer": i.get('id'),
                "discount_amount": 0,
                "discount_reason": "",
                "discount_value": 0,
                "payment_date": self.today,
                "payment_method": "terminal",
                "payments": [{"amount": 1000000, "payment_method": "terminal"}],
                "start_date": self.today,
                "subscription": {"type": 2, "plan": 6,
                                 "club": self.club_id},
                "subtotal": 1000000,
                "total": 1000000,
            })

        return payment_list_data

    def grup_chekin_data_pkg(self):
        response = self.request.get(
            f"{self.base_url}api/v1/management/package-list/?page=1&per_page=100",
            headers=self.headers,
            cookies=self.token_cookies
        ).json().get("results", [])
        pkg_plan = []
        if response:
            for i in response:
                pkg_plan.append({"id": i.get("id"), })
        return pkg_plan

    def grup_chekin_data_cls(self):
        response = self.request.get(
            f"{self.base_url}api/v1/management/class-list/?page=1&per_page=100",
            headers=self.headers,
            cookies=self.token_cookies
        ).json().get("results", [])
        cls_plan = []
        if response:
            for i in response:
                cls_plan.append({"id": i.get("id"), })
        return cls_plan

    def get_staffs_list(self):
        response = self.request.get(
            f"{self.base_url}api/v1/staffs/club-staff-list/",
            headers=self.headers,
            cookies=self.token_cookies
        ).json().get("results", [])
        print(response, "DATA")
        return response

    def notifation_data(self):
        member_list = self.get_member_list_noti() or []
        staff_list = self.get_staffs_list() or []
        print(staff_list, "STADD @")
        data = {
            "all_customers": False,
            "all_staffs": False,
            "customers": [fake.random_element([item["id"] for item in member_list])] if member_list else [],

            # TODO 2 ID RASM YUBORMASLIK KERAK  !!!!!😤
            "images": [1, 3, 4, 5, 6, 7],
            "message": fake.text(),
            "staffs": [fake.random_element([item["id"] for item in staff_list])] if staff_list else [],
            # "staffs": [],
            "title": "Test Uchun To'gri tushinina Kerak edi 😊😀😂 Jaxl qilish yoq 😤🤬😡  Yaxshilab Test qilyapman Uzr Oma"
        }
        print(data, "DATA >>>>")
        return data

    def create_invontery_products(self, number, method, url):

        for i in range(number):
            data = {
                "images": [

                ],
                "attributes": [],
                "name": f"ProductTest{i}",
                "is_active": True,
                "original_price": "5000",
                "sale_price": "1000000",
                "other": "string",
                "unit_value": "0",
                "reference_code": 9223,
                "quantity": 1,
                "category": 1,
                "unit": 1,
                "color": None
            }
            self.send_request(method, url, data)

    def delete_club(self):

        response = self.request.delete(
            f"{self.base_url}api/v1/management/club/2/",
            headers=self.headers,
            cookies=self.token_cookies
        )
        print(response.status_code, "Testt")
        return response.status_code

    def one_time_create(self,number):
        logging.info("POST action for One time started...")
        url = 'api/v1/management/one-time-payment/'

        for _ in range(number):
            data = {
                "full_name": fake.random_element([fake.name_male(), fake.name_female()]),
                "payment_method": "terminal",
                "price": fake.random_int(min=10000, max=1000000)
            }
            response = self.request.post(
                f"{self.base_url}{url}",
                json=data,
                headers=self.headers,
                cookies=self.token_cookies
            )

            logging.info(response.json())


def services_difference_time(services_old, services_new):
    result = {}
    result["Eski serverning o'rtacha javob vaqti"] = f"{services_old['avg_response_time']} soniya"
    result["Yangi serverning o'rtacha javob vaqti"] = f"{services_new['avg_response_time']} soniya"

    old_time = float(services_old['avg_response_time'])
    new_time = float(services_new['avg_response_time'])
    if old_time < new_time:
        difference = new_time - old_time
        result["difference"] = f'Eski server tezroq va {difference:.2f} soniyaga tezroq ishlaydi.'
    elif old_time > new_time:
        difference = old_time - new_time
        result["difference"] = f'Yangi server tezroq va {difference:.2f} soniyaga tezroq ishlaydi.'
    else:
        result["difference"] = 'Ikkala serverning tezligi bir xil.'

    result["Yuborilgan requestlar soni"] = f"{services_old['Jami yuborilgan requestlar soni']} ta"
    return result


if __name__ == "__main__":
    print('START PROGRESS.......')
    club_id = input("Club ID Kiriting: ")
    pkg_id = input("Package ID Kiriting: ")
    if club_id and pkg_id:
        # server_1 = QaServices("https://app.deepen.uz/", club_id,int(pkg_id))
        server_1 = QaServices("https://app.qa.deepen.uz/", club_id, int(pkg_id))
        # server_1 = QaServices("http://192.168.1.67:8000/", club_id, int(pkg_id))
        # server_1 = QaServices("https://app.deepen.uz/")
        # server_1 = QaServices("http://192.168.1.67:8000/")
        # server_2 = QaServices("https://pro.mukhtor.uz/")
        # server_2 = QaServices("https://pro.mukhtor.uz/")

        # club_list = server_1.get_avg_response_time(
        #     'api/v1/management/club-list/?is_active=1&year=2024&order=asc&sort=name', method='get', action=MethodRole.CLUB)
        # club_edit = server_1.get_avg_response_time(
        #
        #     'api/v1/management/club/', method='patch', action=MethodRole.CLUB)
        #
        # staff_create = server_1.get_avg_response_time('api/v1/staffs/', method='post', action=MethodRole.STAFF)
        # # staff_edit = server_1.get_avg_response_time('api/v1/staffs/', method='patch', action=MethodRole.STAFF)
        # #
        # pkg_create = server_1.get_avg_response_time('api/v1/management/package/', method='post', action=MethodRole.PACKAGE)
        # pkg_edit = server_1.get_avg_response_time('api/v1/management/package/', method='patch', action=MethodRole.PACKAGE)
        # pkg_list = server_1.get_avg_response_time('api/v1/management/package-list/?page=1&per_page=100', method='get',
        #                                           action=MethodRole.PACKAGE)
        #
        # room_create = server_1.get_avg_response_time('api/v1/management/room/', method='post', action=MethodRole.ROOM)
        # room_edit = server_1.get_avg_response_time('api/v1/management/room/', method='patch', action=MethodRole.ROOM)
        # room_lst = server_1.get_avg_response_time('api/v1/management/room-list/?q=T', method='get', action=MethodRole.ROOM)

        # cls_create = server_1.get_avg_response_time('api/v1/management/class/', method='post', action=MethodRole.CLASS)
        # cls_edit = server_1.get_avg_response_time('api/v1/management/class/', method='patch', action=MethodRole.CLASS)
        # cls_list = server_1.get_avg_response_time('api/v1/management/class-list/?page=1&per_page=100', method='get',
        #                                           action=MethodRole.CLASS)
        #
        # member_create = server_1.get_avg_response_time('api/v1/management/member/', method='post',
        #                                                action=MethodRole.MEMBER)
        # # member_edit = server_1.get_avg_response_time('api/v1/management/member/', method='patch', action=MethodRole.MEMBER)
        # # member_lst = server_1.get_avg_response_time('api/v1/management/member-list/?page=1&per_page=1000', method='get')
        # #
        # payment_create_pkg = server_1.get_avg_response_time('api/v1/management/payment/', method='post',
        #                                                     action=MethodRole.PAYMENT_PACKAGE)
        # member_create_2 = server_1.get_avg_response_time('api/v1/management/member/', method='post',
        #                                                  action=MethodRole.MEMBER)
        # payment_create_cls = server_1.get_avg_response_time('api/v1/management/payment/', method='post',
        #                                                     action=MethodRole.PAYMENT_CLASS)
        # TODO DELETE QILISH ISHLAYDI
        # print(server_1.get_avg_response_time('api/v1/management/member/', method='delete', action=MethodRole.MEMBER))

        # grup_chekin_pkg = server_1.get_avg_response_time('api/v1/check-in/register/', method='post',
        #                                                  action=MethodRole.GRUPCHEKIN_PKG)
        #
        # grup_chekin_cls = server_1.get_avg_response_time('api/v1/check-in/register/', method='post',
        #                                                  action=MethodRole.GRUPCHEKIN_CLASS)
        #
        # create_notifacation = server_1.get_avg_response_time('api/v1/notifications/', method='post',
        #                                                      action=MethodRole.NOTIFY)
        # create_inventory = server_1.create_invontery_products(100, 'post', 'api/v1/inventory/products/')
        # Club_delete = server_1.delete_club()
        one_time_create = server_1.one_time_create(10)
