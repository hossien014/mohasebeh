--ابتدا اگر جدول های زر موجود بودند انها را حذف میکند 
DROP TABLE IF EXISTS users; 
DROP TABLE IF EXISTS works; 
DROP TABLE IF EXISTS work_perday; 

--ساخت جدول کاربران 
--ایدی جوری تنظیم شده است که به صورت خوکار اضافه  می شود و یوزر نیم باید حتما خاص باشد
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL UNIQUE,
password TEXT NOT NULL,
email TEXT NOT NULL
);

CREATE TABLE works (
id INTEGER PRIMARY KEY AUTOINCREMENT
,work TEXT NOT NULL 
,category TEXT NOT NULL 
,user_id INTEGER FOREIGNKEY REFERENCES users(id) NOT NULL
);
--"SELECT works.work,work_perday.work_time_minute FROM works INNER JOIN work_perday ON work_perday.work_id =works.id "
CREATE TABLE work_perday(
id INTEGER PRIMARY KEY AUTOINCREMENT
,day_ DATE  NOT NULL 
,work_id INTEGER FOREIGNKEY REFERENCES works(id)
,work_time_minute INTEGER NOT NULL  
,user_id INTEGER FOREIGNKEY REFERENCES users(id) NOT NULL
);

INSERT INTO users(username,password,email)
VALUES("hossien",1234,"test");