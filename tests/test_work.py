from flask import current_app,Flask,g,session
import pytest
import sqlite3
from mohasebeh_v1.db import get_db
from mohasebeh_v1 import singleton
from flask.testing import FlaskClient
from conftest import AuthActions


#تست رفتن به صفحه کار ها بدون ورود به سایت 
def test_viste_work_without_login(client:FlaskClient,app:Flask):
      r=client.get("/work/")
      assert r.status_code==302
      assert r.headers["Location"] =="/auth/register" or "http://localhost/auth/register"
       
      
      
def test_viste_work_with_login(client:FlaskClient,auth:AuthActions):
      #تست ورود موفق
      r_login=auth.login()    
      assert r_login.headers["Location"] =="/" or "http://localhost/"
            
      #بازدید از صفحه ورک در حال ورود
      r_viste_work_endpoit=client.get("/work/")
      assert r_viste_work_endpoit.status_code == 200
      assert "test" in str(r_viste_work_endpoit.data) # نام کاربری تست است .در اینجا چک می شود که نام کاربری در صفحه وجود داشته باشد
    
@pytest.mark.parametrize(
("work","category","message"),
(
      ("","",singleton.empty_filed),
      ("","catgory",singleton.empty_filed),
      ("work","",singleton.empty_filed),
      ("test","test",singleton.alrady_exist),#این کار در دیتا بیس وجود دارد
),   
)
def test_add_invaid_work(client:FlaskClient,auth:AuthActions ,work,category,message): 
      auth.login()
      client.post("/work/add",data={ "work":"test"  , "category":"test" })
      r_add_invalid_work=client.post("/work/add",data={ "work":work  , "category":category })
      assert r_add_invalid_work.status_code == 302
      
      redirect_url = r_add_invalid_work.headers["Location"]
      r_after_redirect=client.get(redirect_url)
      assert message in str(r_after_redirect.data)

def test_add_vaild_work_Delete(client:FlaskClient,auth:AuthActions,app:Flask):
      
      auth.login().headers["Location"] =="/" #ورود به اکانت 
      #مدت زیادی سعی کردم به مسیر 
      # /work 
      #وصل شوم ولی این کار فقط به مسیر لوکال هاست ریدارکت می کند
      add_work_url="http://localhost/work/add"
      work_url="http://localhost/work/"
      delete_work_url="http://localhost/work/delete" 
      client.post(add_work_url,data={"work": "readbook", "category": "sport"})
      r_get_to_wrok_after_add_work=client.get(work_url)
      assert singleton.work_added in str(r_get_to_wrok_after_add_work.data)
      
      with app.app_context():
            db=get_db()
            readbook_wrok=db.execute("SELECT * FROM works WHERE work ='readbook'").fetchone()
            assert readbook_wrok is not None
            
      #تست کردن حذف کار
      client.post(delete_work_url,data={"work_to_delete":"readbook"})
      with app.app_context():
            db=get_db()
            readbook_wrok=db.execute("SELECT * FROM works WHERE work ='readbook'").fetchone()
            assert readbook_wrok is  None
