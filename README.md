# QA portfolio

A practice suite for [saucedemo.com](https://www.saucedemo.com) on Playwright and
pytest with Allure reporting, plus unit tests for a few small helpers.

## What is here

- `pages.py` — page objects for the login screen, the catalogue and the checkout
- `test_saucedemo_smoke.py` — browser tests: sign-in, rejected sign-in, cart,
  sorting by price, and the checkout flow end to end
- `conftest.py` — fixtures, including a login state saved once per session and
  reused, and a hook that attaches a screenshot to the Allure report on failure
- `test_call_oop.py`, `test_beepDetection.py`, `test_Cartesia.py` — unit tests for
  helpers around call state and billing, tone frequency matching and transcript
  cleanup

Those last three come out of what I test at work, a VoIP platform. A detected tone
never lands exactly on its nominal frequency and speech recognition never returns
the same string twice, so neither is ever compared for equality.

## Running

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest
```

The base URL and the credentials are read from `.env` if it exists, otherwise from
the defaults in `config.py` — saucedemo publishes them on its own login page.

For the Allure report:

```bash
pytest --alluredir=allure-results
allure serve allure-results
```
