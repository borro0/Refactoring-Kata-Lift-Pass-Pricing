from flask import Flask
from flask import request
from lift_pass_pricing.price_calculator import PriceCalculator
from lift_pass_pricing.price_data_access import PriceDataAccess
import json

app = Flask("lift-pass-pricing")

connection_options = {
    "host": "localhost",
    "user": "root",
    "database": "lift_pass",
    "password": "mysql",
}

price_data_access = PriceDataAccess(connection_options)


@app.route("/prices", methods=["GET", "PUT"])
def prices():
    res = {}
    if request.method == "PUT":
        lift_pass_cost = request.args["cost"]
        lift_pass_type = request.args["type"]
        price_data_access.store_pass_type_base_price(lift_pass_cost, lift_pass_type)
        return {}
    elif request.method == "GET":
        res = handle_get_request()

    return res


def handle_get_request():
    if "multiple_prices" in request.args:
        res = []
        for request_params in json.loads(request.args["multiple_prices"].replace("'", '"')):
            res.append({"cost": request_single_pass_price(request_params)})
    else:
        res = {}
        res["cost"] = request_single_pass_price(request.args)
    return res

def request_single_pass_price(arg_dict):
    price_calculator = PriceCalculator(price_data_access)

    pass_type = arg_dict["type"]
    age = int(arg_dict["age"]) if "age" in arg_dict else None
    date = arg_dict["date"] if "date" in arg_dict else None

    return price_calculator.calculate_price(pass_type, age, date)


def main():
    app.run(port=3005)

if __name__ == "__main__":
    main()
