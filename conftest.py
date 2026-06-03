import requests

from urls import (
    LOGIN_COURIER_URL,
    CREATE_COURIER_URL
)


def delete_courier(login, password):

    login_data = {
        'login': login,
        'password': password
    }

    response = requests.post(
        LOGIN_COURIER_URL,
        data=login_data
    )

    if response.status_code == 200:

        courier_id = response.json()['id']

        requests.delete(
            f'{CREATE_COURIER_URL}/{courier_id}'
        )