from flask import Blueprint,render_template,redirect,url_for,request,flash,g
from mohasebeh_v1.auth import login_required
from mohasebeh_v1 import singleton
from mohasebeh_v1.db import get_db
import sqlite3

bp=Blueprint("work",__name__,url_prefix="/work")

@bp.route("/",methods=["GET","POST"])
@login_required
def work():
      print("get work")
      db= get_db()
      user_id = g.user["id"]
      works_in_db=db.execute("SELECT * FROM works WHERE user_id= ?",(user_id,)).fetchall()
      error=None
      
      if request.method=="POST":
            print("post work") 
            work=request.form["work"]
            category=request.form["category"]
            
            if not work or not category :
                  error=singleton.empty_filed+"باید تمام فیلد ها را پر کنید"
                  flash(error)
                  return redirect(url_for("work.work"))
            
            else:
                  try:  
                        work_list=work.split("-")
                        for item in work_list:
                              db.execute("INSERT INTO works(work,category,user_id)VALUES(?,?,?)",(item,category,user_id))
                              db.commit()
                  except sqlite3.IntegrityError as e :
                        flash(f" را قبلا وارد کرده اید لطفا یک کار غیر تکراری اضافه کنید {work} " +singleton.alrady_exist)
                        return redirect(url_for("work.work"))
                  else:
                        db.commit()
                        print("coomite")
      flash("کار ها با موفقیت افزوده شد" +singleton.work_added)                  
      return render_template("work/work.html",pagetitle="کار ها", works=works_in_db)


@bp.route("/delete-work",methods=["POST"])
def delete_work():
      work_to_delete= request.form["work_to_delete"]
      db=get_db()
      db.execute("DELETE FROM works WHERE work= ? ",(work_to_delete,))
      db.commit()
      return redirect(url_for("work.work"))
      