import pytest
import app as app_module
from app import app


@pytest.fixture(autouse=True)
def reset_state():
    """Reset in-memory state before every test for isolation."""
    app_module.users = []
    app_module.next_id = 1
    yield


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# POST /users
# ---------------------------------------------------------------------------

def test_post_creates_user_returns_201(client):
    """Successful POST creates a user and returns 201 with id/name/email."""
    resp = client.post('/users', json={'name': 'Alice', 'email': 'alice@example.com'})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data['id'] == 1
    assert data['name'] == 'Alice'
    assert data['email'] == 'alice@example.com'


def test_post_duplicate_email_returns_400(client):
    """POSTing a duplicate email returns 400 with an error message."""
    client.post('/users', json={'name': 'Alice', 'email': 'alice@example.com'})
    resp = client.post('/users', json={'name': 'Alice2', 'email': 'alice@example.com'})
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data


def test_post_missing_name_returns_400(client):
    """POSTing without 'name' returns 400 with an error message."""
    resp = client.post('/users', json={'email': 'bob@example.com'})
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data


def test_post_missing_email_returns_400(client):
    """POSTing without 'email' returns 400 with an error message."""
    resp = client.post('/users', json={'name': 'Bob'})
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data


# ---------------------------------------------------------------------------
# GET /users
# ---------------------------------------------------------------------------

def test_get_returns_empty_list_initially(client):
    """GET /users returns an empty list when no users exist."""
    resp = client.get('/users')
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_get_returns_users_after_post(client):
    """GET /users returns the created users after one or more POSTs."""
    client.post('/users', json={'name': 'Alice', 'email': 'alice@example.com'})
    client.post('/users', json={'name': 'Bob', 'email': 'bob@example.com'})
    resp = client.get('/users')
    assert resp.status_code == 200
    users = resp.get_json()
    assert len(users) == 2
    emails = {u['email'] for u in users}
    assert emails == {'alice@example.com', 'bob@example.com'}
