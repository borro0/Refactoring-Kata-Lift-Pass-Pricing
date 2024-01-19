import pytest

from datetime import datetime
from lift_pass_pricing.price_calculator import PriceCalculator


class PriceDataAccessForTest:
    def __init__(self):
        self.base_price = {"1jour": 35, "night": 19}
        self.holidays = ["2019-02-18", "2019-02-25", "2019-03-04"]

    def get_pass_type_base_price(self, type):
        return self.base_price[type]

    def get_holidays(self):
        return [datetime.fromisoformat(holiday) for holiday in self.holidays]


@pytest.fixture()
def price_calculator() -> PriceCalculator:
    price_data_access = PriceDataAccessForTest()
    return PriceCalculator(price_data_access)


def test_1DayPrice(price_calculator: PriceCalculator):
    price = price_calculator.calculate_price(type="1jour")
    assert price == 35


def test_NightPriceNormalAge(price_calculator: PriceCalculator):
    price = price_calculator.calculate_price(type="night", age=30)
    assert price == 19


def test_NightPriceNoAgeNoCosts(price_calculator: PriceCalculator):
    # this test might actually show a bug in the pricing algorithm
    price = price_calculator.calculate_price(type="night")
    assert price == 0


def test_1DayAgeUnder6NoCost(price_calculator: PriceCalculator):
    price = price_calculator.calculate_price(type="1jour", age=1)
    assert price == 0


def test_1DayMondayReductionNoAge(price_calculator: PriceCalculator):
    price = price_calculator.calculate_price(type="1jour", date="2019-02-11")
    assert price == 23


def test_NightAgeOver64Reduction(price_calculator: PriceCalculator):
    price = price_calculator.calculate_price(type="night", age=65)
    assert price == 8


def test_1DayMondayReductionNormalAge(price_calculator: PriceCalculator):
    price = price_calculator.calculate_price(type="1jour", date="2019-02-11", age=30)
    assert price == 23


def test_1DayNoMondayReductionDuringHoliday(price_calculator: PriceCalculator):
    price = price_calculator.calculate_price(type="1jour", date="2019-02-18")
    assert price == 35


def test_1DayPriceAgeUnder15GetsReduction(price_calculator: PriceCalculator):
    price = price_calculator.calculate_price(type="1jour", age=14)
    assert price == 25


def test_1DayPriceAgeOver64GetsReduction(price_calculator: PriceCalculator):
    price = price_calculator.calculate_price(type="1jour", age=65)
    assert price == 27
