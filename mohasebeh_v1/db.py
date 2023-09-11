from flask import current_app, g, Flask
import sqlite3
import click


def get_db():
    print("getting db")
    if "db" not in g:
        # ساخت کانکشن به یک دیتا بیست و ذخیر کردن ان در متغیر گلوبال فلسک
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        # این خط باعث میشود جواب ریکوئست ما از دیتا بیس به صورت دیکشنری برگردد
        g.db.row_factory = sqlite3.Row
        #
    return g.db


def init_db():
    """با استفاده از فایل اسکیما جدول های اولیه را می سازد"""
    print("init_db")
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        # حالا باید فایل را تبدیل به متن متن کنیم
        db.executescript(f.read().decode("utf8"))


def close_db(e=None):
    """اگر در گلوبال دیتا بیسی وجود داشت ان را می بندد"""

    print("close_db")
    db = g.pop("db", None)
    if db is not None:
        db.close()


@click.command("init-db")
def init_db_command():
    init_db()
    click.echo("Initialized Database done ")


def init_app(app: Flask):
    # بعد از هر ریکوئست تیر داون اجرا می شود
    print("init_app")
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
