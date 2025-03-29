from django.urls import reverse


class TestMerchantView:

    def test_successful_login(self, api_client, setup_merchant_user):
        user = setup_merchant_user

        headers = {"Accept-Language": "uz"}
        data = {
            'username': "otabek@gmail.com",
            'password': "1234"
        }
        url = reverse('authentication:login')
        response = api_client.post(url, data, format='json', **headers)
        assert response.status_code == 200
        assert sorted(response.data.keys()) == sorted(['success', 'message', 'results'])

    def test_error_login_400(self, setup_merchant_user, api_client):
        user = setup_merchant_user
        headers = {"Accept-Language": "uz"}
        data = {
            'username': "123444",
            'password': "1234"
        }
        url = reverse('authentication:login')
        response = api_client.post(url, data, format='json', **headers)
        assert response.status_code == 400
        assert response.data["username"][0] == "Enter a valid email address."

    def test_redirect_to_login_valid(self, setup_merchant_user, api_client, one_time_pass):
        user = setup_merchant_user
        headers = {"Accept-Language": "uz"}
        url = reverse('authentication:redirect')

        one = one_time_pass.create(username=user.username)
        data = {
            "hash": one.hash
        }

        response = api_client.post(url, data, format='json', **headers)
        assert response.status_code == 200
        assert sorted(response.data.keys()) == sorted(['success', 'message', 'results'])

    def test_redirect_to_login_invalid(self, setup_merchant_user, api_client, one_time_pass):
        headers = {"Accept-Language": "uz"}
        url = reverse('authentication:redirect')
        data = {
            "a": "1232414"
        }

        response = api_client.post(url, data, format='json', **headers)
        assert response.status_code == 400
        assert response.data["hash"][0] == "This field is required."

    def test_logout_valid(self, setup_merchant_user, api_client, one_time_pass):
        user = setup_merchant_user
        headers = {"Accept-Language": "uz"}
        url = reverse('authentication:redirect')

        one = one_time_pass.create(username=user.username)
        data = {
            "hash": one.hash
        }
        response = api_client.post(url, data, format='json', **headers)
        urls = reverse('authentication:logout')
        response = api_client.post(urls, format='json', **headers)
        assert response.status_code == 200
        assert sorted(response.data.keys()) == sorted(['success', 'message'])
        assert response.cookies.get('access').value == ''
        assert response.cookies.get('refresh').value == ''
        assert response.cookies.get('csrftoken').value == ''

    def test_profile_list(self, setup_merchant_user, api_client, one_time_pass):
        user = setup_merchant_user
        headers = {"Accept-Language": "uz"}
        url = reverse('authentication:redirect')

        one = one_time_pass.create(username=user.username)
        data = {
            "hash": one.hash
        }

        response = api_client.post(url, data, format='json', **headers)
        access_token = response.data.get('access')
        headers = {"Accept-Language": "uz", "HTTP_AUTHORIZATION": f'Bearer {access_token}'}
        # Set the tokens in the headers
        profile_url = reverse('authentication:profile')
        response = api_client.get(profile_url, {"pk": user.id}, format='json', **headers)
        assert response.status_code == 200
        assert sorted(response.data['results']) == sorted(
            ['id', 'merchant_name', 'merchant_phone', 'merchant_address', 'staff_name', 'staff_phone', 'email',
             'language', ])

    def test_profile_detail(self, setup_merchant_user, api_client, access_tokens):
        user = setup_merchant_user

        data = {
            "username": "+9998912233939",
            "staff_name": "Figma"
        }
        headers = {"Accept-Language": "uz", "HTTP_AUTHORIZATION": f'Bearer {access_tokens}'}
        profile_url = reverse('authentication:profile', kwargs={"pk": user.id})
        response = api_client.patch(profile_url, data, format='json', **headers)
        assert response.status_code == 200
        assert sorted(response.data.keys()) == sorted(['success', 'message'])

    def test_profile_check_auth_valid(self, setup_merchant_user, api_client, access_tokens):
        headers = {"Accept-Language": "uz", "HTTP_AUTHORIZATION": f'Bearer {access_tokens}'}
        profile_url = reverse('authentication:check_auth')
        response = api_client.get(profile_url, format='json', **headers)
        assert response.status_code == 200
        assert sorted(response.data['results']) == sorted(['merchant_name', 'version'])

    def test_profile_check_auth_invalid(self, setup_merchant_user, api_client):
        headers = {"Accept-Language": "uz"}
        profile_url = reverse('authentication:check_auth')
        response = api_client.get(profile_url, format='json', **headers)
        assert response.status_code == 401
        assert sorted(response.data.keys()) == sorted(['success', 'message'])
        assert response.data['success'] == False
        assert response.data['message'] == '401 Authorization required'

    def test_staff_get_profile(self, api_client, setup_db_dashboard):
        user, role, club, mr, club_staff, access_token = setup_db_dashboard
        headers = {
            "HTTP_Accept-Language": "uz",
            'HTTP_Cookie': f"{access_token}",
            "HTTP_Club-Id": f"{club.id}",
        }
        url = reverse(f'authentication:staff_profile')

        response = api_client.get(url, format='json',
                                  **headers)

        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['message'] == 'OK'
        assert sorted(response.data['results']) == sorted(['first_name', 'last_name',
                                                           'gender', 'birth_date',
                                                           'phone', 'email',
                                                           'avatar', 'role'])

    def test_staff_patch_profile(self, api_client, setup_db_dashboard):
        user, role, club, mr, club_staff, access_token = setup_db_dashboard
        headers = {
            "HTTP_Accept-Language": "uz",
            'HTTP_Cookie': f"{access_token}",
            "HTTP_Club-Id": f"{club.id}",
        }
        url = reverse(f'authentication:staff_profile')
        data = {'first_name': '1212'}
        response = api_client.patch(url, data=data, format='json',
                                    **headers)

        assert response.status_code == 200
        assert response.data['success'] is True
        assert response.data['message'] == 'OK'
        assert sorted(response.data['results']) == sorted(['first_name', 'last_name',
                                                           'gender', 'birth_date',
                                                           'phone', 'email',
                                                           'avatar', 'role'])
        assert response.data['results']['first_name'] == '1212'
