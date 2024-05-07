from flask import Flask, request, jsonify
from models import db
from marshmallow import ValidationError
from converters import (
    parse_rates,
    consolidate_rates,
    parse_time_range,
    get_unique_timezones,
)
from repository import ParkingRateRepository
from validators import ma, PutRatesInputSchema, GetPriceInputSchema, GetRatesInputSchema
from exceptions import InputExceedsAllowedRangeError
from http import HTTPStatus


app = Flask(__name__)


def initialize_extensions():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking_rates.db"
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        ParkingRateRepository.create_all()


@app.route("/rates", methods=["GET", "PUT"])
def rates():
    try:
        if request.method == "GET":
            data = request.args
            validated_args = GetRatesInputSchema().load(data)
            rates = ParkingRateRepository.get_all()
            formatted_rates = consolidate_rates(
                rates, validated_args.get("timezone", "UTC")
            )
            return (jsonify({"rates": formatted_rates}), HTTPStatus.OK)

        elif request.method == "PUT":
            data = request.json
            validated_data = PutRatesInputSchema().load(data)
            rate_dtos = parse_rates(validated_data)
            ParkingRateRepository.overwrite_all(rate_dtos)
            unique_timezones = get_unique_timezones(validated_data)
            fetch_tz = unique_timezones[0] if len(unique_timezones) == 1 else "UTC"
            formatted_rates = consolidate_rates(rate_dtos, fetch_tz)
            return jsonify({"rates": formatted_rates}), HTTPStatus.OK

    except ValidationError as e:
        return jsonify({"error": e.messages}), HTTPStatus.BAD_REQUEST


@app.route("/price", methods=["GET"])
def price():
    try:
        data = request.args
        validated_args = GetPriceInputSchema().load(data)
        time_range_dto = parse_time_range(validated_args)
        price = ParkingRateRepository.get_price(time_range_dto)
        if price is None:
            return jsonify({"price": "unavailable"}), HTTPStatus.OK
        return jsonify({"price": price}), HTTPStatus.OK

    except InputExceedsAllowedRangeError:
        return jsonify({"price": "unavailable"}), HTTPStatus.OK

    except ValidationError as e:
        return jsonify({"error": e.messages}), HTTPStatus.BAD_REQUEST


if __name__ == "__main__":
    initialize_extensions()
    app.run()
