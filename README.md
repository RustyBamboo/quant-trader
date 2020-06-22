# Trader

A simple Robinhood seller bot that will sell all quantities of a stock if value drops below threshold.

## Setup

`git clone ...`

`cd quant-trader`

`git submodule update --init`

`touch .env`

Add to `.env`:

```shell
RH_USERNAME=USERNAME
RH_PASSWORD=PASSWORD
```

`python -m venv pyrh_env`

`source pyrh_env/bin/activate`

Install python packages: `marshmallow`, `pytz`, `requests`, `yarl`, `python-dotenv`, `python-dateutil` etc...

Modify `main.py` values `PRICE_DIFF_LIMIT` and `REFRESH_TIME`

## Run

`source pyrh_env/bin/activate`

`python main.py`