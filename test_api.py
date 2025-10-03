from fastapi.testclient import TestClient
from api import app


def test_analyze_get():
    client = TestClient(app)
    resp = client.get('/analyze', params={'url': 'https://httpbin.org/html'})
    assert resp.status_code == 200
    j = resp.json()
    assert 'title' in j
    assert 'text' in j
    assert 'scores' in j


def test_analyze_post():
    client = TestClient(app)
    resp = client.post('/analyze', json={'url': 'https://httpbin.org/html'})
    assert resp.status_code == 200
    j = resp.json()
    assert 'dominant' in j