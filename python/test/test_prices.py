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


def test_something(test_client):
    response = test_client.get(f'/prices?{urlencode({"type": "1jour"})}')
    assert response.json == {"cost": 35}
