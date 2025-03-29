from django.urls import reverse


class TestDashboard:

    def test_get_report(self, setup_db_dashboard, api_client):
        user, role, club, mr, club_staff, access_token = setup_db_dashboard
        headers = {
            "HTTP_Accept-Language": "uz",
            'HTTP_Cookie': f"{access_token}",
            "HTTP_Club-Id": f"{club.id}",
        }
        url = reverse(f'dashboard:members_reports')
        data = {'username': user.username, 'password': user.password, }

        response = api_client.get(url, data=data, format='json', **headers)
        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['message'] == "OK"
        assert sorted(response.data['results'].keys()) == sorted(['member', 'demographic', "attendance"])
        assert sorted(response.data['results']['member'].keys()) == sorted(['package_members', 'class_members'])
        assert sorted(response.data['results']['demographic'].keys()) == sorted(['male_percent', 'female_percent'])
        assert sorted(set(response.data['results']['attendance'][0].keys())) == sorted(['date', 'count'])

    def test_get_attendance(self, setup_db_dashboard, api_client):
        user, role, club, mr, club_staff, access_token = setup_db_dashboard
        headers = {
            "HTTP_Accept-Language": "uz",
            'HTTP_Cookie': f"{access_token}",
            "HTTP_Club-Id": f"{club.id}",
        }
        url = reverse(f'dashboard:members_report')
        data = {'username': user.username, 'password': user.password, }

        response = api_client.get(url, data=data, format='json', **headers)
        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['message'] == "OK"
        assert sorted(set(response.data['results'][0].keys())) == sorted(['date', 'count'])

    def test_get_sales_by_packages(self, setup_db_dashboard, api_client):
        user, role, club, mr, club_staff, access_token = setup_db_dashboard
        headers = {
            "HTTP_Accept-Language": "uz",
            'HTTP_Cookie': f"{access_token}",
            "HTTP_Club-Id": f"{club.id}",
        }
        url = reverse(f'dashboard:sales-sales_by_packages')
        data = {'username': user.username, 'password': user.password, }
        response = api_client.get(url, data=data, format='json', **headers)
        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['message'] == "OK"
        assert sorted(response.data['results'].keys()) == sorted(['income_data', 'package_sales_data'])
        assert sorted(set(response.data['results']['package_sales_data'][0].keys())) == sorted(['name', 'total'])
        assert sorted(set(response.data['results']['income_data'].keys())) == sorted(['total_amount', 'percent'])

    def test_get_sales_by_methods(self, setup_db_dashboard, api_client):
        user, role, club, mr, club_staff, access_token = setup_db_dashboard
        headers = {
            "HTTP_Accept-Language": "uz",
            'HTTP_Cookie': f"{access_token}",
            "HTTP_Club-Id": f"{club.id}",
        }
        url = reverse(f'dashboard:sales-sales_by_methods')
        data = {'username': user.username, 'password': user.password, }
        response = api_client.get(url, data=data, format='json', **headers)
        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['message'] == "OK"
        assert sorted(set(response.data['results'][0].keys())) == sorted(['method', 'amount'])

    def test_get_sales_summery(self, setup_db_dashboard, api_client):
        user, role, club, mr, club_staff, access_token = setup_db_dashboard
        headers = {
            "HTTP_Accept-Language": "uz",
            'HTTP_Cookie': f"{access_token}",
            "HTTP_Club-Id": f"{club.id}",
        }
        url = reverse(f'dashboard:sales-sales_summery')
        data = {'username': user.username, 'password': user.password, }
        response = api_client.get(f"{url}", data=data, format='json',
                                  **headers)
        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['message'] == "OK"
        print(response.data['results'][0].keys(), "dl,a;d,l;a")
        assert sorted(set(response.data['results'][0].keys())) == sorted(
            ['start_date', 'end_date', 'cls_total', 'pkg_total'])

    def test_get_sales_summery_days(self, setup_db_dashboard, api_client):
        user, role, club, mr, club_staff, access_token = setup_db_dashboard
        headers = {
            "HTTP_Accept-Language": "uz",
            'HTTP_Cookie': f"{access_token}",
            "HTTP_Club-Id": f"{club.id}",
        }
        url = reverse(f'dashboard:sales-sales_summery')
        data = {'username': user.username, 'password': user.password, }
        response = api_client.get(f"{url}", data=data, format='json',
                                  **headers)
        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['message'] == "OK"
        print(response.data['results'][0].keys(), "dl,a;d,l;a")
        assert sorted(set(response.data['results'][0].keys())) == sorted(
            ['start_date', 'end_date', 'cls_total', 'pkg_total'])

    def test_get_sales_summery_days_8_else(self, setup_db_dashboard, api_client):
        user, role, club, mr, club_staff, access_token = setup_db_dashboard
        headers = {
            "HTTP_Accept-Language": "uz",
            'HTTP_Cookie': f"{access_token}",
            "HTTP_Club-Id": f"{club.id}",
        }
        url = reverse(f'dashboard:sales-sales_summery') + "?start_date=2024-08-10&end_date=2024-08-15"
        data = {'username': user.username, 'password': user.password,
                "start_date": "2024-08-10",
                "end_date": "2024-08-15"}
        response = api_client.get(url, data=data, format='json',
                                  **headers)
        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['message'] == "OK"

        assert sorted(set(response.data['results'][0].keys())) == sorted(
            ['start_date', 'end_date', 'cls_total', 'pkg_total'])

    def test_get_sales_summery_days_14(self, setup_db_dashboard, api_client):
        user, role, club, mr, club_staff, access_token = setup_db_dashboard
        headers = {
            "HTTP_Accept-Language": "uz",
            'HTTP_Cookie': f"{access_token}",
            "HTTP_Club-Id": f"{club.id}",
        }
        url = reverse(f'dashboard:sales-sales_summery')
        data = {'username': user.username, 'password': user.password,
                "start_date": "2024-08-10",
                "end_date": "2024-08-20"}
        response = api_client.get(url, data=data, format='json',
                                  **headers)
        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['message'] == "OK"

        assert sorted(set(response.data['results'][0].keys())) == sorted(
            ['start_date', 'end_date', 'cls_total', 'pkg_total'])

    def test_get_sales_summery_days_31(self, setup_db_dashboard, api_client):
        user, role, club, mr, club_staff, access_token = setup_db_dashboard
        headers = {
            "HTTP_Accept-Language": "uz",
            'HTTP_Cookie': f"{access_token}",
            "HTTP_Club-Id": f"{club.id}",
        }
        url = reverse(f'dashboard:sales-sales_summery') + "?start_date=2024-08-10&end_date=2024-08-15"
        data = {'username': user.username, 'password': user.password,
                "start_date": "2024-08-10",
                "end_date": "2024-09-10"}
        response = api_client.get(url, data=data, format='json',
                                  **headers)
        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['message'] == "OK"

        assert sorted(set(response.data['results'][0].keys())) == sorted(
            ['start_date', 'end_date', 'cls_total', 'pkg_total'])

    def test_get_sales_summery_days_15(self, setup_db_dashboard, api_client):
        user, role, club, mr, club_staff, access_token = setup_db_dashboard
        headers = {
            "HTTP_Accept-Language": "uz",
            'HTTP_Cookie': f"{access_token}",
            "HTTP_Club-Id": f"{club.id}",
        }
        url = reverse(f'dashboard:sales-sales_summery')
        data = {'username': user.username, 'password': user.password,
                "start_date": "2024-08-15",
                "end_date": "2024-09-14"}
        response = api_client.get(url, data=data, format='json',
                                  **headers)
        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['message'] == "OK"

        assert sorted(set(response.data['results'][0].keys())) == sorted(
            ['start_date', 'end_date', 'cls_total', 'pkg_total'])

