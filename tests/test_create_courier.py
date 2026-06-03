import requests
import random
import allure

from urls import CREATE_COURIER_URL
from conftest import delete_courier


class TestCreateCourier:

    def generate_random_string(self, length):
        letters = 'abcdefghijklmnopqrstuvwxyz'

        return ''.join(
            random.choice(letters)
            for i in range(length)
        )

    def generate_payload(self):
        return {
            'login': self.generate_random_string(10),
            'password': self.generate_random_string(10),
            'firstName': self.generate_random_string(10)
        }

    @allure.title('Курьера можно создать')
    def test_create_courier_success(self):
        payload = self.generate_payload()

        response = requests.post(
            CREATE_COURIER_URL,
            data=payload
        )

        assert response.status_code == 201
        assert response.json() == {'ok': True}

        delete_courier(
            payload['login'],
            payload['password']
        )

    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_two_identical_couriers_error(self):
        payload = self.generate_payload()

        requests.post(
            CREATE_COURIER_URL,
            data=payload
        )

        response = requests.post(
            CREATE_COURIER_URL,
            data=payload
        )

        assert response.status_code == 409
        assert response.json()['message'] == (
            'Этот логин уже используется. Попробуйте другой.'
        )

        delete_courier(
            payload['login'],
            payload['password']
        )

    @allure.title('Нельзя создать курьера без логина')
    def test_create_courier_without_login_error(self):
        payload = {
            'password': '1234',
            'firstName': 'saske'
        }

        response = requests.post(
            CREATE_COURIER_URL,
            data=payload
        )

        assert response.status_code == 400
        assert response.json()['message'] == (
            'Недостаточно данных для создания учетной записи'
        )

    @allure.title('Нельзя создать курьера без пароля')
    def test_create_courier_without_password_error(self):
        payload = {
            'login': self.generate_random_string(10),
            'firstName': 'saske'
        }

        response = requests.post(
            CREATE_COURIER_URL,
            data=payload
        )

        assert response.status_code == 400
        assert response.json()['message'] == (
            'Недостаточно данных для создания учетной записи'
        )