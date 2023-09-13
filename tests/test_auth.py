
from flask.testing import FlaskClient
from flask import url_for,session,g
import pytest
from mohasebeh_v1.db import get_db
from mohasebeh_v1 import singleton


def test_register(client: FlaskClient, app):
    assert client.get("/auth/register").status_code == 200
    response = client.post(
        "/auth/register", data={"username": "a", "password": "a", "email": "a"})
    assert response.headers["Location"] == "/auth/login" or "http://localhost/auth/login"

    response = client.post(
        "/auth/register", data={"username": "b", "password": "a", "email": "a"})
    assert response.status_code == 302

    # چک کردن دیتا بیس
    with app.app_context():
        assert get_db().execute("SELECT * FROM users WHERE username='a'").fetchone() is not None


def test_login(client: FlaskClient, auth):
    assert client.get("/auth/login").status_code==200
    assert auth.login().headers["Location"]=="/" or "http://localhost/"
    
    with client:
      client.get("/")
      assert session["user"]=="test"
      assert g.user["username"] == "test"
      client.get("/auth/logout")
      assert "user" not in session

@pytest.mark.parametrize(
      ("username","password","email","message"),
      (
            ("user","","email",b"invalid user password"),
            ("","pass","email",b"invalid user name"),
            ("user","pass","",b"invalid user email"),
      ),
)
def test_invalid_register(client:FlaskClient,username,password,email,message):
      
      r=client.post("/auth/register",data={"username":username,"password":password,"email":email})
      assert message in r.data


@pytest.mark.parametrize(("username","password","message")
                        , (
                            ("test","",singleton.incorrect_password.encode("utf-8")) ,
                            ("","test",singleton.incorrect_username.encode("utf-8")),  
                            ("wwwwwwww","test",singleton.invalid_username.encode("utf-8")),  
                            ("test","test",b""),  
                          )    
                        )      
def test_invaild_login(client:FlaskClient,username,password,message):
      
      r=client.post("/auth/login",data={"username":username ,"password":password})
      assert message in r.data
      
#تست سِشن ها      
def test_sessions(client:FlaskClient,auth,app):
    auth.login()
    with client.session_transaction() as sess:
        assert sess["user"]=="test"
  