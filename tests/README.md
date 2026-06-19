Tests for the Mergington High School Activities API

Run tests with:

```
pip install -r requirements.txt
pytest -q
```

Notes:
- Tests use the synchronous FastAPI `TestClient` and are isolated by a fixture that snapshots and restores the in-memory `activities` dictionary between tests.
- Files: `tests/conftest.py`, `tests/test_activities.py`
