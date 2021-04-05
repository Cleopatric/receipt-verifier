import json
import pytest
import requests


def get_response(url: str, params: dict) -> dict:
    session = requests.Session()
    response = session.post(url=url, data=params)
    return response.json()


@pytest.fixture(scope='module')
def base_url(request) -> str:
    return r'http://0.0.0.0:8080/api/sign_up'


@pytest.fixture(scope='module')
def error_params(request) -> dict:
    params = {"test": "test"}
    return json.dumps(params)


@pytest.fixture(scope='module')
def error_msg(base_url, error_params) -> dict:
    return get_response(base_url, error_params)


@pytest.fixture(scope='module')
def no_params_msg(base_url) -> dict:
    return get_response(base_url, {})
