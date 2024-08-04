import pytest
from website import create_app, db


@pytest.fixture()
def app():
    app = create_app()

    with app.app_context():
        db.create_all()
        from website.fill_db import populate_database
        populate_database()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()
