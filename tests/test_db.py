from flask import current_app
import pytest
import sqlite3
from mohasebeh_v1.db import get_db


def test_get_db_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT * FROM users")
    assert "closed" in str(e.value)


def test_init_command(runner, monkeypatch):

    class recorder:
        called = False  

        def fake_init_call():
            recorder.called = True
            
    monkeypatch.setattr("mohasebeh_v1.db.init_db", recorder.fake_init_call)
    result = runner.invoke(args=["init-db"])
    assert "Database done" in result.output
    assert recorder.called
    
