from fastapi.testclient import TestClient

from fast_api_jwt.service.main import app

client = TestClient(app)

def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello from our fast-api app."}

def test_docs():
    response = client.get("/docs")
    assert response.status_code == 200
    assert response.text.strip().startswith("<!DOCTYPE html>")
