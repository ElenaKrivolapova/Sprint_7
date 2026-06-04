import pytest
import requests

from courier import (
    register_new_courier_and_return_login_password,
    generate_payload
)
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


@pytest.fixture
def created_courier():
    courier_data = register_new_courier_and_return_login_password()

    yield courier_data

    delete_courier(
        courier_data[0],
        courier_data[1]
    )


@pytest.fixture
def payload_with_cleanup():
    payload = generate_payload()

    yield payload

    delete_courier(
        payload['login'],
        payload['password']
    )