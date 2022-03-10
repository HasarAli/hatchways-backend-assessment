from blog_api import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_ping(client):
    response = client.get("/api/ping")
    print(response)
    assert response.status_code == 200
  