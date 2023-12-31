from flask import Flask, render_template
import os
from mohasebeh_v1 import auth, db,works_handeling,home


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "mohasbat.sqlite"),
    )
    if not test_config:
        try:
            app.config.from_pyfile("config.py")
        except FileNotFoundError as e:
            print(f"you have to make P{e.filename}")
    else:
        app.config.update(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(works_handeling.bp)
    app.register_blueprint(home.bp)

    
    app.add_url_rule("/",endpoint="index")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
