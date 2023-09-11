import mohasebeh_v1
from flask.testing import FlaskClient


def test_config():
    assert not mohasebeh_v1.create_app().testing
    assert mohasebeh_v1.create_app({"TESTING": True}).testing


def test_index(client: FlaskClient):
      r=client.get("/").status_code
      assert r==200
