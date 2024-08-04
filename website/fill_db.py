from website import db
from website.models import User
from werkzeug.security import generate_password_hash
from faker import Faker
import random


def populate_database():
    if User.query.first():
        print("Database already populated")
        return

    fake = Faker()
    Faker.seed(0)
    random.seed(0)

    for _ in range(20):
        full_name = fake.name()
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90)
        pesel_number = ''.join([str(random.randint(0, 9)) for _ in range(11)])
        address = fake.address()
        email = fake.unique.email()
        phone_number = fake.phone_number()
        account_type = random.choice(['personal', 'business'])
        password = '123'
        password_hash = generate_password_hash(password)
        balance = round(random.uniform(0, 10000), 2)

        new_user = User(
            full_name=full_name,
            date_of_birth=date_of_birth,
            pesel_number=pesel_number,
            address=address,
            email=email,
            phone_number=phone_number,
            account_type=account_type,
            password_hash=password_hash,
            balance=balance
        )
        db.session.add(new_user)

    db.session.commit()
    print("Database populated with sample data")
