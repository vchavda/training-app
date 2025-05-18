import requests
import time

BASE_URL = 'http://localhost:5000'

# Wait briefly for the containerized app to start up
def wait_for_app(timeout=10):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(f"{BASE_URL}/")
            if r.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            time.sleep(0.5)
    raise RuntimeError("App did not start in time")


def test_hello_world():
    assert wait_for_app(), "App did not start"
    resp = requests.get(f"{BASE_URL}/")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Hello, World!"}


def test_add():
    resp = requests.get(f"{BASE_URL}/add?a=2&b=3")
    assert resp.status_code == 200
    assert resp.json() == {"result": 5.0}


if __name__ == '__main__':
    import pytest
    # Run pytest with verbose output
    pytest.main(['-v'])

