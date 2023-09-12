--ابتدا اگر جدول های زر موجود بودند انها را حذف میکند 
DROP TABLE IF EXISTS users; 

--ساخت جدول کاربران 
--ایدی جوری تنظیم شده است که به صورت خوکار اضافه  می شود و یوزر نیم باید حتما خاص باشد
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL UNIQUE,
password TEXT NOT NULL,
email TEXT NOT NULL
);
