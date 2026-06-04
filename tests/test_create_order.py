import requests
import pytest
import allure

from urls import ORDERS_URL
from order_data import ORDER_PAYLOAD


class TestCreateOrder:

    @allure.title('Создание заказа с разными вариантами цвета')
    @pytest.mark.parametrize(
        'color',
        [
            ['BLACK'],
            ['GREY'],
            ['BLACK', 'GREY'],
            []
        ]
    )
    def test_create_order_with_different_colors_success(self, color):
        payload = ORDER_PAYLOAD.copy()
        payload['color'] = color

        with allure.step('Отправить запрос на создание заказа'):
            response = requests.post(
                ORDERS_URL,
                json=payload
            )

        assert response.status_code == 201
        assert 'track' in response.json()