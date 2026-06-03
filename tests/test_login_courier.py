import requests
import allure

from courier import register_new_courier_and_return_login_password
from urls import LOGIN_COURIER_URL
from conftest import delete_courier


class TestLoginCourier:

    @allure.title('Курьер может авторизоваться')
    def test_login_courier_success(self):
        courier = register_new_courier_and_return_login_password()

        payload = {
            'login': courier[0],
            'password': courier[1]
        }

        response = requests.post(
            LOGIN_COURIER_URL,
            data=payload
        )

        assert response.status_code == 200
        assert 'id' in response.json()

        delete_courier(
            courier[0],
            courier[1]
        )

    @allure.title('Нельзя авторизоваться без логина')
    def test_login_courier_without_login_error(self):
        courier = register_new_courier_and_return_login_password()

        payload = {
            'login': '',
            'password': courier[1]
        }

        response = requests.post(
            LOGIN_COURIER_URL,
            data=payload
        )

        assert response.status_code == 400
        assert response.json()['message'] == (
            'Недостаточно данных для входа'
        )

        delete_courier(
            courier[0],
            courier[1]
        )

    @allure.title('Нельзя авторизоваться без пароля')
    def test_login_courier_without_password_error(self):
        courier = register_new_courier_and_return_login_password()

        payload = {
            'login': courier[0],
            'password': ''
        }

        response = requests.post(
            LOGIN_COURIER_URL,
            data=payload
        )

        assert response.status_code == 400
        assert response.json()['message'] == (
            'Недостаточно данных для входа'
        )

        delete_courier(
            courier[0],
            courier[1]
        )

    @allure.title('Нельзя авторизоваться с неверным логином')
    def test_login_courier_with_wrong_login_error(self):
        courier = register_new_courier_and_return_login_password()

        payload = {
            'login': 'wrong_login',
            'password': courier[1]
        }

        response = requests.post(
            LOGIN_COURIER_URL,
            data=payload
        )

        assert response.status_code == 404
        assert response.json()['message'] == (
            'Учетная запись не найдена'
        )

        delete_courier(
            courier[0],
            courier[1]
        )

    @allure.title('Нельзя авторизоваться с неверным паролем')
    def test_login_courier_with_wrong_password_error(self):
        courier = register_new_courier_and_return_login_password()

        payload = {
            'login': courier[0],
            'password': 'wrong_password'
        }

        response = requests.post(
            LOGIN_COURIER_URL,
            data=payload
        )

        assert response.status_code == 404
        assert response.json()['message'] == (
            'Учетная запись не найдена'
        )

        delete_courier(
            courier[0],
            courier[1]
        )

    @allure.title('Нельзя авторизоваться под несуществующим пользователем')
    def test_login_nonexistent_courier_error(self):
        payload = {
            'login': 'nonexistent_login_12345',
            'password': 'nonexistent_password'
        }

        response = requests.post(
            LOGIN_COURIER_URL,
            data=payload
        )

        assert response.status_code == 404
        assert response.json()['message'] == (
            'Учетная запись не найдена'
        )