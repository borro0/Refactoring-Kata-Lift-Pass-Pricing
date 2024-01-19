import pytest
from urllib.parse import urlencode

from lift_pass_pricing.prices import app


@pytest.fixture(scope="module")
def test_client():
    # Create a test client using the Flask application configured for testing
    app.testing = True
    with app.test_client() as testing_client:
        # Establish an application context
        with app.app_context():
            yield testing_client  # this is where the testing happens!


def test_app_1DayPrice(test_client):
    response = test_client.get(f'/prices?{urlencode({"type": "1jour"})}')
    assert response.json == {"cost": 35}


def test_app_NightPriceNormalAge(test_client):
    response = test_client.get(f'/prices?{urlencode({"type": "night", "age": 30})}')
    assert response.json == {"cost": 19}


def test_app_1DayMondayReductionNoAge(test_client):
    response = test_client.get(
        f'/prices?{urlencode({"type": "1jour", "date": "2019-02-11"})}'
    )
    assert response.json == {"cost": 23}


def test_app_MultiplePassPrices(test_client):
    input_requests = {
        "multiple_prices": [
            {"type": "night", "age": 30},
            {"type": "1jour", "date": "2019-02-11"},
        ]
    }
    response = test_client.get(f"/prices?{urlencode(input_requests)}")
    assert response.json == [{"cost": 19}, {"cost": 23}]
