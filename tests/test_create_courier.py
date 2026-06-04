import requests
import allure

from urls import CREATE_COURIER_URL
from courier import generate_random_string


class TestCreateCourier:

    @allure.title('Курьера можно создать')
    def test_create_courier_success(self, payload_with_cleanup):

        with allure.step('Отправить запрос на создание курьера'):
            response = requests.post(
                CREATE_COURIER_URL,
                data=payload_with_cleanup
            )

        assert response.status_code == 201
        assert response.json() == {'ok': True}

    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_two_identical_couriers_error(
        self,
        payload_with_cleanup
    ):

        with allure.step('Создать курьера'):
            requests.post(
                CREATE_COURIER_URL,
                data=payload_with_cleanup
            )

        with allure.step('Повторно отправить запрос с теми же данными'):
            response = requests.post(
                CREATE_COURIER_URL,
                data=payload_with_cleanup
            )

        assert response.status_code == 409
        assert response.json()['message'] == (
            'Этот логин уже используется. Попробуйте другой.'
        )

    @allure.title('Нельзя создать курьера без логина')
    def test_create_courier_without_login_error(self):
        payload = {
            'password': '1234',
            'firstName': 'saske'
        }

        with allure.step('Отправить запрос на создание курьера без логина'):
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
            'login': generate_random_string(10),
            'firstName': 'saske'
        }

        with allure.step('Отправить запрос на создание курьера без пароля'):
            response = requests.post(
                CREATE_COURIER_URL,
                data=payload
            )

        assert response.status_code == 400
        assert response.json()['message'] == (
            'Недостаточно данных для создания учетной записи'
        )