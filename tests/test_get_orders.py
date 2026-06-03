import requests
import allure

from urls import ORDERS_URL


class TestGetOrders:

    @allure.title('Получение списка заказов')
    def test_get_orders_success(self):
        response = requests.get(
            ORDERS_URL
        )

        assert response.status_code == 200
        assert 'orders' in response.json()
        assert isinstance(
            response.json()['orders'],
            list
        )