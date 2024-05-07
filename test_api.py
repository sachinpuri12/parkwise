import pytest
from app import app, db
import json
import pdb

app.config["TESTING"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking_rates_test.db"
db.init_app(app)


@pytest.fixture
def test_app():
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        yield client


@pytest.fixture
def test_db(test_app):
    with test_app.app_context():
        db.create_all()
        yield db
        db.session.rollback()
        db.drop_all()


# test data json
TEST_DATA_DIR = "test_data"


@pytest.fixture
def put_rates_input():
    with open(f"{TEST_DATA_DIR}/put_rates_input.json", "r") as file:
        return json.load(file)


@pytest.fixture
def put_rates_output():
    with open(f"{TEST_DATA_DIR}/put_rates_output.json", "r") as file:
        return json.load(file)


@pytest.fixture
def get_rates_timezone_output():
    with open(f"{TEST_DATA_DIR}/get_rates_timezone_output.json", "r") as file:
        return json.load(file)


@pytest.fixture
def put_rates_single_timezone_input():
    with open(f"{TEST_DATA_DIR}/put_rates_single_timezone_input.json", "r") as file:
        return json.load(file)


@pytest.fixture
def put_rates_single_timezone_output():
    with open(f"{TEST_DATA_DIR}/put_rates_single_timezone_output.json", "r") as file:
        return json.load(file)


class TestApi:
    def test_put_rates(self, client, put_rates_input, put_rates_output):
        response = client.put("/rates", json=put_rates_input)
        assert response.status_code == 200
        assert response.json == put_rates_output

    def test_put_rates_single_timezone(
        self, client, put_rates_single_timezone_input, put_rates_single_timezone_output
    ):
        response = client.put("/rates", json=put_rates_single_timezone_input)
        assert response.status_code == 200
        assert response.json == put_rates_single_timezone_output

    def test_get_rates(self, client, put_rates_input, put_rates_output):
        client.put("/rates", json=put_rates_input)
        response = client.get("/rates")
        assert response.status_code == 200
        assert response.json == put_rates_output

    def test_get_rates_with_timezone(
        self, client, put_rates_input, get_rates_timezone_output
    ):
        client.put("/rates", json=put_rates_input)
        response = client.get("/rates?timezone=America/Chicago")
        assert response.status_code == 200
        assert response.json == get_rates_timezone_output

    @pytest.mark.parametrize(
        "start, end, expected_price",
        [
            ("2024-05-06T11:00:00-05:00", "2024-05-06T12:00:00-05:00", 1500.0),
            ("2024-05-04T12:00:00-05:00", "2024-05-04T13:00:00-05:00", 2000.0),
            ("2024-05-08T12:00:00", "2024-05-08T12:30:00", 1750.0),
            ("2024-05-09T12:00:00", "2024-05-09T13:00:00", "unavailable"),
            ("2024-05-09T12:00:00", "2024-05-10T13:00:00", "unavailable"),
        ],
    )
    def test_get_price(
        self, client, start, end, put_rates_single_timezone_input, expected_price
    ):
        client.put("/rates", json=put_rates_single_timezone_input)
        response = client.get(f"/price?start={start}&end={end}")
        assert response.status_code == 200
        assert "price" in response.json
        assert response.json["price"] == expected_price
