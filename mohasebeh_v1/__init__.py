from flask import Flask, render_template
import os
from mohasebeh_v1 import auth, db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "mohasbat.sqlite"),
    )
    if not test_config:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.bp)
    db.init_app(app)

    @app.route("/")
    def index():
        return render_template("home.html", pagetitle="صفحه اصلی ")

    return app