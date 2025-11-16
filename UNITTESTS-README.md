# Nebula API Tests

The test_api.py contains the unit tests for the Nebula FastAPI application.

## 1. Installation

First, install the required Python packages for testing. It's recommended to do this in a virtual environment.

From the root directory of the project (`nebula-api`), run the following command:

```bash
pip install -r requirements.txt
```

## 2. Running the Tests

To run the tests, navigate to the root directory of the project (`nebula-api`) and use `pytest`:

```bash
pytest
```

Pytest will automatically discover and run the tests.

## 3. Running the Application Locally

To run the FastAPI application locally for development and manual testing, use the following command from the root directory of the project:

```bash
uvicorn nebula_api:app --reload
```

This will start a local development server. You can then access the API at `http://127.0.0.1:8000`.
