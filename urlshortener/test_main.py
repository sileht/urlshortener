from unittest import mock

from fastapi.testclient import TestClient
from main import app


def test_app():
    with TestClient(app) as client:
        url = "https://www.qovery.com/blog/the-simplest-way-to-deploy-laravel-with-mysql-on-aws"
        response = client.post("/encode", json={"url": url})
        assert response.status_code == 200
        assert response.json() == {"url": url, "urlhash": mock.ANY}
        urlhash = response.json()["urlhash"]

        response = client.get("/encode/", json={"urlhash": "foobar"})
        assert response.status_code == 404

        response = client.get(f"/{urlhash}", allow_redirects=False)
        assert response.status_code == 307
        assert response.headers["Location"] == url
