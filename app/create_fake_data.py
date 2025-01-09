import random

from faker import Faker
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import SessionLocal, get_db
from models import Mission, Target, SpyCat

breeds = [
    "American Shorthair",
    "Abyssinian",
    "Aegean",
    "American Bobtail",
    "American Curl"
]

# Инициализация Faker
fake = Faker()


def create_fake_cats(db: Session = Depends(get_db), n: int = 10):
    for _ in range(n):
        name = fake.first_name()
        years_of_experience = random.randint(1, 10)
        breed = random.choice(breeds)
        salary = random.randint(1000, 5000)

        fake_cat = SpyCat(
            name=name,
            years_of_experience=years_of_experience,
            breed=breed,
            salary=salary
        )

        db.add(fake_cat)

    db.commit()
    print("Randomly cats created")


def create_fake_missions(db: Session, n: int = 10):
    for _ in range(n):
        assign_cat = random.choice([True, False])

        if assign_cat:
            name = fake.first_name()
            years_of_experience = random.randint(1, 10)
            breed = random.choice(breeds)
            salary = random.randint(1000, 5000)

            new_cat = SpyCat(
                name=name,
                years_of_experience=years_of_experience,
                breed=breed,
                salary=salary
            )

            db.add(new_cat)
            db.commit()
            db.refresh(new_cat)
            cat_id = new_cat.id
        else:
            cat_id = None

        mission = Mission(
            cat_id=cat_id,
            complete=False
        )

        db.add(mission)
        db.commit()
        db.refresh(mission)

        num_targets = random.randint(1, 3)

        for _ in range(num_targets):
            target_name = fake.sentence(nb_words=3)
            country = fake.country()
            notes = fake.text(max_nb_chars=200)
            complete = random.choice([True, False])

            target = Target(
                mission_id=mission.id,
                name=target_name,
                country=country,
                notes=notes,
                complete=complete
            )

            db.add(target)

        db.commit()
        print(f"Created mission with ID {mission.id} and {num_targets} targets.")


def main():
    db = SessionLocal()
    try:
        create_fake_cats(db, n=10)
        create_fake_missions(db, n=5)
    finally:
        db.close()


if __name__ == "__main__":
    main()
