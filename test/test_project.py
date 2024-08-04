from website.models import User


def test_home(client):
    response = client.get('/')
    assert b'<title>Home</title>' in response.data


def test_signing_up(client, app):
    # Sign up a new user and check the last record in the DB
    response = client.post('/signup', data={'full_name': 'Tim Spencer',
                                            'date_of_birth': '2012-12-12',
                                            'pesel_number': '12345678910',
                                            'address': 'Jana Kochanowskiego Street 21',
                                            'email': 'tim@gmail.com',
                                            'phone_number': '123456789',
                                            'initial_balance': '2138.42',
                                            'account_type': 'personal',
                                            'password': '123',
                                            'confirm_password': '123'})

    with app.app_context():
        assert User.query.count() == 21
        assert User.query[-1].email == 'tim@gmail.com'


def test_logging_in(client):
    response = client.post('/login', data={'email': 'katelynmontgomery@example.com',
                                           'password': '123'})

    # Expecting a redirect
    assert response.status_code == 302

    # Redirect
    assert response.location == '/user'
