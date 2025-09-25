import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_register_page_loads(client):
    """Register page should load with 'Register' text"""
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Register" in response.data


def test_login_page_loads(client):
    """Login page should load with 'Login' text"""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_dashboard_redirects_if_not_logged_in(client):
    """Dashboard should redirect unauthenticated users to login"""
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
