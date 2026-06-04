import requests
import allure

from urls import LOGIN_COURIER_URL


class TestLoginCourier:

    @allure.title('Курьер может авторизоваться')
    def test_login_courier_success(self, created_courier):
        payload = {
            'login': created_courier[0],
            'password': created_courier[1]
        }

        with allure.step('Отправить запрос на авторизацию курьера'):
            response = requests.post(
                LOGIN_COURIER_URL,
                data=payload
            )

        assert response.status_code == 200
        assert 'id' in response.json()

    @allure.title('Нельзя авторизоваться без логина')
    def test_login_courier_without_login_error(self, created_courier):
        payload = {
            'login': '',
            'password': created_courier[1]
        }

        with allure.step('Отправить запрос без логина'):
            response = requests.post(
                LOGIN_COURIER_URL,
                data=payload
            )

        assert response.status_code == 400
        assert response.json()['message'] == (
            'Недостаточно данных для входа'
        )

    @allure.title('Нельзя авторизоваться без пароля')
    def test_login_courier_without_password_error(self, created_courier):
        payload = {
            'login': created_courier[0],
            'password': ''
        }

        with allure.step('Отправить запрос без пароля'):
            response = requests.post(
                LOGIN_COURIER_URL,
                data=payload
            )

        assert response.status_code == 400
        assert response.json()['message'] == (
            'Недостаточно данных для входа'
        )

    @allure.title('Нельзя авторизоваться с неверным логином')
    def test_login_courier_with_wrong_login_error(
        self,
        created_courier
    ):
        payload = {
            'login': 'wrong_login',
            'password': created_courier[1]
        }

        with allure.step('Отправить запрос с неверным логином'):
            response = requests.post(
                LOGIN_COURIER_URL,
                data=payload
            )

        assert response.status_code == 404
        assert response.json()['message'] == (
            'Учетная запись не найдена'
        )

    @allure.title('Нельзя авторизоваться с неверным паролем')
    def test_login_courier_with_wrong_password_error(
        self,
        created_courier
    ):
        payload = {
            'login': created_courier[0],
            'password': 'wrong_password'
        }

        with allure.step('Отправить запрос с неверным паролем'):
            response = requests.post(
                LOGIN_COURIER_URL,
                data=payload
            )

        assert response.status_code == 404
        assert response.json()['message'] == (
            'Учетная запись не найдена'
        )

    @allure.title('Нельзя авторизоваться под несуществующим пользователем')
    def test_login_nonexistent_courier_error(self):
        payload = {
            'login': 'nonexistent_login_12345',
            'password': 'nonexistent_password'
        }

        with allure.step(
            'Отправить запрос с несуществующим пользователем'
        ):
            response = requests.post(
                LOGIN_COURIER_URL,
                data=payload
            )

        assert response.status_code == 404
        assert response.json()['message'] == (
            'Учетная запись не найдена'
        )