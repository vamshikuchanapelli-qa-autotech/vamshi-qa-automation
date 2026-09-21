# API Automation with Robot Framework

A small API automation project using Python, Robot Framework, and a page-object model (POM). The Python API helper owns authentication and session management, while the Robot suite stays readable and focused on behavior.

## Project structure

```text
modules/api_automation/api_helper.py    # API helper
tests/API_suites/__init__.robot         # Suite setup and teardown
tests/API_suites/sample_api.robot       # Sample API test
robot.toml                              # RobotCode configuration
local_env.sh                            # Local API configuration
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Run the tests

```bash
source local_env.sh
.venv/bin/robotcode robot -d vamshi-results
```

Set the API URL, login URL, username, and password in `local_env.sh`, then source it before running the suite:

```bash
source local_env.sh
.venv/bin/robotcode robot -d vamshi-results
```

`local_env.sh` is ignored by Git so credentials remain local. It exports `API_AUTH_URL`, `API_USERNAME`, and `API_PASSWORD`, which are consumed by the Python API helper during suite setup. The helper accepts `access_token`, `token`, or `id_token` from the login response and adds it as a bearer token to the session.

`tests/API_suites/__init__.robot` creates a bearer token through the configured login API in suite setup, stores it in the shared master dictionary, and closes the API session in suite teardown.

```bash
source local_env.sh && .venv/bin/robotcode robot -d vamshi-results
```

The sample test verifies that the access token was created and stored.

Open `vamshi-results/report.html` for the Robot Framework report.