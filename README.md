# Parking Rates API

This API allows you to manage parking rates and calculate prices for given time ranges.

## Setup

1. Clone the repository

2. Ensure Python3.9 is installed

3. Initialize virtual environment

   ```bash
   # navigate to repo root
   cd parkwise/

   # create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install dependencies:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

5. Start the server:

   ```bash
   python3 app.py
   ```

API should now be accessible on `http://localhost:5000`

## Endpoints

### `PUT /rates`

#### Description

Overwrites existing parking rates.

A rate is comprised of `days`, `times`, `tz` (timezone), and `price`. If no `tz` value is specified, the rate will be defaulted to `UTC`.

#### Request Body

```json
{
  "rates": [
    {
      "days": "mon,tues,wed,thurs",
      "times": "0900-2100",
      "tz": "America/New_York",
      "price": 10.5
    },
    {
      "days": "fri",
      "times": "1000-2100",
      "tz": "America/New_York",
      "price": 10.5
    },
    {
      "days": "sat,sun",
      "times": "0900-1800",
      "tz": "America/Chicago",
      "price": 12.75
    }
  ]
}
```

#### Response

- `200 OK`: Returns a JSON object with consolidated parking rates.

#### Output

```json
{
  "rates": [
    {
      "end": "MONDAY 21:00",
      "price": 10.5,
      "start": "MONDAY 09:00",
      "timezone": "America/New_York"
    },
    {
      "end": "TUESDAY 21:00",
      "price": 10.5,
      "start": "TUESDAY 09:00",
      "timezone": "America/New_York"
    },
    {
      "end": "WEDNESDAY 21:00",
      "price": 10.5,
      "start": "WEDNESDAY 09:00",
      "timezone": "America/New_York"
    },
    {
      "end": "THURSDAY 21:00",
      "price": 10.5,
      "start": "THURSDAY 09:00",
      "timezone": "America/New_York"
    },
    {
      "end": "FRIDAY 21:00",
      "price": 10.5,
      "start": "FRIDAY 10:00",
      "timezone": "America/New_York"
    },
    {
      "end": "SATURDAY 19:00",
      "price": 12.75,
      "start": "SATURDAY 10:00",
      "timezone": "America/New_York"
    },
    {
      "end": "SUNDAY 19:00",
      "price": 12.75,
      "start": "SUNDAY 10:00",
      "timezone": "America/New_York"
    }
  ]
}
```

### `GET /rates`

#### Description

Retrieve parking rates.

#### Parameters

- `timezone` (optional): Timezone to format the rates. Default is "UTC".

#### Response

- `200 OK`: Returns a JSON object with consolidated parking rates.

#### Request

```bash
curl -X GET "http://localhost:5000/rates?timezone=America/New_York"
```

#### Response Output

```json
{
  "rates": [
    {
      "end": "TUESDAY 01:00",
      "price": 10.5,
      "start": "MONDAY 13:00",
      "timezone": "UTC"
    },
    {
      "end": "WEDNESDAY 01:00",
      "price": 10.5,
      "start": "TUESDAY 13:00",
      "timezone": "UTC"
    },
    {
      "end": "THURSDAY 01:00",
      "price": 10.5,
      "start": "WEDNESDAY 13:00",
      "timezone": "UTC"
    },
    {
      "end": "FRIDAY 01:00",
      "price": 10.5,
      "start": "THURSDAY 13:00",
      "timezone": "UTC"
    },
    {
      "end": "SATURDAY 01:00",
      "price": 10.5,
      "start": "FRIDAY 14:00",
      "timezone": "UTC"
    },
    {
      "end": "SATURDAY 23:00",
      "price": 12.75,
      "start": "SATURDAY 14:00",
      "timezone": "UTC"
    },
    {
      "end": "SUNDAY 23:00",
      "price": 12.75,
      "start": "SUNDAY 14:00",
      "timezone": "UTC"
    }
  ]
}
```

### `GET /price`

#### Description

Calculate price for a given time range.

#### Parameters

- `start`: Start time (ISO-8601 format).
- `end`: End time (ISO-8601 format).

#### Request

```bash
curl -X GET "http://localhost:5000/price?start=2024-05-01T10:00:00Z&end=2024-05-01T15:00:00Z"
```

#### Response

- `200 OK`: Returns a JSON object with the calculated price.
- `200 OK` (if price is unavailable): Returns a JSON object with "price" set to "unavailable".

#### Output

```json
{
  "price": 10.25
}
```

## Tests

Tests are contained in `test_api.py`. Test suite can be run with `pytest`

```bash
pytest
```
