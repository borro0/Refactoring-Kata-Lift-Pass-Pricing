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


def test_1DayPrice(test_client):
    response = test_client.get(f'/prices?{urlencode({"type": "1jour"})}')
    assert response.json == {"cost": 35}


def test_NightPriceNormalAge(test_client):
    response = test_client.get(f'/prices?{urlencode({"type": "night", "age": 30})}')
    assert response.json == {"cost": 19}


def test_NightPriceNoAgeNoCosts(test_client):
    # this test might actually show a bug in the pricing algorithm
    response = test_client.get(f'/prices?{urlencode({"type": "night"})}')
    assert response.json == {"cost": 0}


def test_1DayAgeUnder6NoCost(test_client):
    response = test_client.get(f'/prices?{urlencode({"type": "1jour", "age": 1})}')
    assert response.json == {"cost": 0}


def test_1DayMondayReductionNoAge(test_client):
    response = test_client.get(
        f'/prices?{urlencode({"type": "1jour", "date": "2019-02-11"})}'
    )
    assert response.json == {"cost": 23}


def test_NightAgeOver64Reduction(test_client):
    response = test_client.get(f'/prices?{urlencode({"type": "night", "age": 65})}')
    assert response.json == {"cost": 8}


def test_1DayMondayReductionNormalAge(test_client):
    response = test_client.get(
        f'/prices?{urlencode({"type": "1jour", "date": "2019-02-11", "age": 30})}'
    )
    assert response.json == {"cost": 23}


def test_1DayNoMondayReductionDuringHoliday(test_client):
    response = test_client.get(
        f'/prices?{urlencode({"type": "1jour", "date": "2019-02-18"})}'
    )
    assert response.json == {"cost": 35}


def test_1DayPriceAgeUnder15GetsReduction(test_client):
    response = test_client.get(f'/prices?{urlencode({"type": "1jour", "age": "14"})}')
    assert response.json == {"cost": 25}


def test_1DayPriceAgeOver64GetsReduction(test_client):
    response = test_client.get(f'/prices?{urlencode({"type": "1jour", "age": "65"})}')
    assert response.json == {"cost": 27}

def test_Set1DayPrice(test_client):
    response = test_client.put(f'/prices?{urlencode({"type": "1jour", "cost": 35})}')
    assert response.status_code == 200
