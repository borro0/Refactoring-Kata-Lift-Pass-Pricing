import math

from datetime import datetime
from lift_pass_pricing.price_data_access import PriceDataAccess

class PriceCalculator:

    def __init__(self, price_data_access):
        self.price_data_access : PriceDataAccess = price_data_access

    def calculate_price(self, type, age=None, date=None) -> int:
        base_price = self.price_data_access.get_pass_type_base_price(type)
        cost = base_price

        if age is not None and age < 6:
            cost = 0
        else:
            if type is not None and type != "night":
                is_holiday = False
                reduction = 0
                if date:
                    date = datetime.fromisoformat(date)
                    for holiday in self.price_data_access.get_holidays():
                        if (
                            date.year == holiday.year
                            and date.month == holiday.month
                            and holiday.day == date.day
                        ):
                            is_holiday = True
                    if not is_holiday and date.weekday() == 0:
                        reduction = 35

                # TODO: apply reduction for others
                if age is not None and age < 15:
                    cost = math.ceil(base_price * 0.7)
                else:
                    if age is None:
                        cost = base_price * (1 - reduction / 100)
                        cost = math.ceil(cost)
                    else:
                        if age > 64:
                            cost = base_price * 0.75 * (1 - reduction / 100)
                            cost = math.ceil(cost)
                        else:
                            cost = base_price * (1 - reduction / 100)
                            cost = math.ceil(cost)
            else:
                if age is not None and age >= 6:
                    if age > 64:
                        cost = math.ceil(base_price * 0.4)
                    else:
                        pass
                else:
                    cost = 0
        return cost