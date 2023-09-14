from flask import Blueprint,render_template,redirect,url_for,request,flash,g
from mohasebeh_v1.auth import login_required
from mohasebeh_v1 import singleton
from mohasebeh_v1.db import get_db
import sqlite3

bp=Blueprint("work",__name__,url_prefix="/work")

@bp.route("/",methods=["GET","POST"])
@login_required
def work():
      works_in_db= get_db().execute("SELECT work FROM works WHERE user_id= ?",(g.user["id"],)).fetchall()
      return render_template("work/work.html",pagetitle="کار ها", works=works_in_db)


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
                                    db.execute("INSERT INTO works(work,category,user_id)VALUES(?,?,?)",(item.strip(),category,g.user["id"]))
                                    db.commit()
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
      