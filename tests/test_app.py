import os
import sys
import pytest

# Add the project root folder to Python path so tests can import app.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Currency Converter" in response.data


def test_empty_amount_does_not_crash(client):
    response = client.post("/", data={
        "amount": "",
        "from_currency": "USD",
        "to_currency": "GBP"
    })
    assert response.status_code == 200
    assert b"Please enter a valid number" in response.data


def test_non_numeric_amount_does_not_crash(client):
    response = client.post("/", data={
        "amount": "abc",
        "from_currency": "USD",
        "to_currency": "GBP"
    })
    assert response.status_code == 200
    assert b"Please enter a valid number" in response.data


def test_10_usd_to_gbp(client):
    response = client.post("/", data={
        "amount": "10",
        "from_currency": "USD",
        "to_currency": "GBP"
    })
    assert response.status_code == 200
    assert b"7.9" in response.data or b"7.90" in response.data


def test_1_gbp_to_eur(client):
    response = client.post("/", data={
        "amount": "1",
        "from_currency": "GBP",
        "to_currency": "EUR"
    })
    assert response.status_code == 200
    assert b"1.16" in response.data


def test_23_eur_to_usd(client):
    response = client.post("/", data={
        "amount": "23",
        "from_currency": "EUR",
        "to_currency": "USD"
    })
    assert response.status_code == 200
    assert b"25.07" in response.data
