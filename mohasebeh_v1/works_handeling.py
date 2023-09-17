from flask import Blueprint,render_template,redirect,url_for,request,flash,g
from mohasebeh_v1.auth import login_required
from mohasebeh_v1 import singleton
from mohasebeh_v1.db import get_db
import sqlite3
import jdatetime
import datetime
import re
import json


bp=Blueprint("work",__name__,url_prefix="/work")

@bp.route("/",methods=["GET","POST"])
@login_required
def work():
      
      week_ago=( jdatetime.date .today() - jdatetime.timedelta(days=7)).strftime("%Y-%m-%d")
      today_j =jdatetime.date.today().strftime("%Y-%m-%d")
      today_m= datetime.date .today()
            
     
      works_in_db= get_db().execute("SELECT * FROM works WHERE user_id= ?",(g.user["id"],)).fetchall()
      
      print("")
      return render_template("work/work.html",pagetitle="کار ها",
            works=works_in_db
            ,today_j=today_j,
            today_m=today_m
            ,work_time_dict_week=get_work_time_jason(old_time=week_ago,new_time=today_j)
            ,work_time_dict_full=get_work_time_jason(old_time="0000,00,00",new_time="1500,01,01"))    


@login_required
@bp.route("add",methods=["POST"])
def add(): 
      db= get_db()
      if request.method=="POST":
            work=request.form["work"]
            category=request.form["category"]
            
            if not work or not category :
                  flash(singleton.empty_filed+"باید تمام فیلد ها را پر کنید")
                  return redirect(url_for("work.work"))
            
            else:
                  works_in_db= db.execute("SELECT work FROM works WHERE user_id= ?",(g.user["id"],)).fetchall()
                  exsit_Works=[row[0] for row in works_in_db]#  تبدیل دیکشنری کارها در دیتا بیس به لیست 
                  user_new_works=work.split("-") # تبدیل کار های ورودی کاربران به لیست 
                  already_exists=[]
                  try:  
                        for item in user_new_works:
                              if item not in exsit_Works:
                                    #db.execute("INSERT INTO works(work,category,user_id)VALUES(?,?,?)",(item.strip(),category,g.user["id"]))
                                    #db.commit()
                                    insert_work_to_sql(g.user["id"],item,category)
                              else:
                                    already_exists.append(item)
                  except sqlite3.IntegrityError as e : # اگر در حالتی خاص دیتا بیس ارور تکرای داد 
                        flash(f" را قبلا وارد کرده اید لطفا یک کار غیر تکراری اضافه کنید {work} " +singleton.alrady_exist)
                        return redirect(url_for("work.work"))
                  else:
                        if len(already_exists)>0:
                             
                              flash( f" این کارها را قبلا اضافه کرده اید {singleton.alrady_exist}{already_exists}")
                              return redirect(url_for("work.work"))
                        else:
                              flash(" کار ها با موفقیت افزوده شد" +singleton.work_added)  
                              return redirect(url_for("work.work"))                         

@bp.route("/delete",methods=["POST"])
@login_required
def delete():
      work_to_delete= request.form["work_to_delete"]
      db=get_db()
      db.execute("DELETE FROM works WHERE work= ? ",(work_to_delete,))
      db.commit()
      return redirect(url_for("work.work"))

@bp.route("/add_daily",methods=["POST"])
def add_daily():
      if request.method=="POST":
            user_input=request.form["daily_works"]
            work_dates=user_input.split("-")
            for work_info in work_dates:
                  if "=" not in work_info:
                        flash(f" {singleton.badformat_not_equal_sign}فرمت متنی که ورد کردید غلط است شما باید  به صورت  مثلا ورزش =1:24 وارد کنید")
                        return redirect(url_for("work.work"))
                  
                  work_title,work_time= work_info.split("=")
                  if not re.fullmatch(singleton.time_validation_pattern_re,work_time):
                        flash(f"فرمت زمان را درست وارد نکرده اید. یا باید فقط دقیقه را بنویسید مثل ورزش=20 یا برای ساعت باید از فرمت ورزش =3:24 استفاده کنید{singleton.badformat_time} ")
                        return redirect(url_for("work.work"))
                  
                  work_time_minute=0
                  if ":" in work_time:
                        list_time=work_time.split(":")
                        hour= int(list_time[0])
                        minute= int(list_time[1])
                        work_time_minute=(hour*60)+minute
                        
                  else:
                        work_time_minute=int(work_time)
                  
                  day_=str(jdatetime.date.today().strftime("%Y-%m-%d"))
                  work_id=get_work_id(g.user["id"],work_title)
                  user_id=g.user["id"]
                  db=get_db()
                  db.execute("INSERT INTO work_perday(day_,work_id,work_time_minute,user_id)VALUES(?,?,?,?)",(day_,work_id,work_time_minute,user_id))
                  db.commit()
                  flash(f"{work_title}اضافه شدند")
                  
            return redirect(url_for("work.work"))

@bp.route("/work_time_dict")
def work_time_dict():
      max=request.args["max"]
      max=request.args["time"]
      
      return  json.dumps(get_work_time_jason(max) ,ensure_ascii=False)
       

def get_work_time_jason(old_time,new_time,max=0):
    work_time_table= get_db().execute("""
      SELECT works.work, SUM(work_perday.work_time_minute) AS total_time 
      FROM works INNER JOIN work_perday
      ON work_perday.work_id = works.id 
      WHERE works.user_id =? 
      AND work_perday.day_ BETWEEN ? AND ? -- تاریخ قدیمی تر باید اول باشد و جدید تر دوم 
      GROUP BY works.work -- باعث میشود ورک ها یونیک بشوند
      HAVING  SUM(work_perday.work_time_minute) > ? -- جمع را نمی شود در محدود کننده ور استفاده کرد و بایدا ز هوینگ استفاده کنیم
      """,(g.user["id"] ,old_time,new_time, int(max))).fetchall()
      #work_time_dict=[dict(item) for item in work_time_table]
      
    work_time_dict={}
    for item in work_time_table:
          item= dict(item)
          item["total_time"]= convert_minute_to_hour( item["total_time"])
          a= str(item["work"])
          work_time_dict[ a ] =item["total_time"]
            
    return work_time_dict
      

def get_work_id(user_id,work):
      db=get_db()
      result = db.execute("SELECT id FROM works WHERE work=? AND user_id=?", (work,user_id)).fetchone()
      if result:
            return result[0]
      else :
            #اگر این کار نبود ان را بساز
            try:
                  insert_work_to_sql(user_id,work)
                  result = db.execute("SELECT id FROM works WHERE work=? AND user_id=?", (work,user_id)).fetchone()
                  if result:
                        return result[0]
            except sqlite3.IntegrityError as e:
                  return "کار تکراری است"

            
      
def insert_work_to_sql(user_id,work,category="defult"):
      db=get_db()
      db.execute("INSERT INTO works(work,category,user_id)VALUES(?,?,?)",(work.strip(),category,user_id))
      db.commit()
                  

def convert_minute_to_hour(minute:int):
      hour=(minute/60).__round__()
      b=hour*60
      new_min=abs( minute-b)
      return {"h":hour,"m":new_min}

