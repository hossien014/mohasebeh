import pytest
import tempfile
from mohasebeh_v1 import create_app
from mohasebeh_v1 import db
from flask import current_app,Flask
import os
path=os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(path,"test_schema.sql"),"rb") as f:
      sql_scripte=f.read().decode("utf8")

@pytest.fixture   
def app():
      db_file_descripton,db_tmp_path= tempfile.mkstemp()
      app=create_app({"TESTING": True, "DATABASE": db_tmp_path})
      #تمام کار هایی که با دیتا بیس داریم باید در اپ کانتکس انجام شود
      with app.app_context():
            db.init_db()
            db.get_db().executescript(sql_scripte)
      
      yield app
      
      os.close(db_file_descripton)
      os.unlink(db_tmp_path)
      
@pytest.fixture
def client(app:Flask):
      return app.test_client()

@pytest.fixture
def runner(app:Flask):
      return app.test_cli_runner()



class AuthActions:
      def __init__(self ,client) -> None:
            self.client=client
      
      def login(self,username="test",password="test",email="test"):
            return self.client.post(
                  "/auth/login",data={"username":username ,"password":password}
            )
      def logout(self):
        return self._client.get("/auth/logout")

@pytest.fixture
def auth(client):
      return AuthActions(client)
      