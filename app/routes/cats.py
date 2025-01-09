import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/cats", tags=["Spy Cats"])

CAT_API_BREEDS_URL = "https://api.thecatapi.com/v1/breeds"


def is_valid_breed(breed_name: str) -> bool:
    try:
        response = requests.get(CAT_API_BREEDS_URL)
        response.raise_for_status()
        breeds = response.json()
        return any(breed["name"].lower() == breed_name.lower() for breed in breeds)
    except requests.RequestException:
        raise HTTPException(status_code=500, detail="Error accessing TheCatAPI")


@router.post("/", response_model=schemas.SpyCat)
def create_cat(cat: schemas.SpyCatCreate, db: Session = Depends(get_db)):
    if len(cat.name)<2:
        raise HTTPException(status_code=400, detail="Too short name")

    if cat.salary < 0:
        raise HTTPException(status_code=400, detail="Salary must be a positive number")

    if cat.years_of_experience < 0:
        raise HTTPException(status_code=400, detail="Years of experience must be a positive number")

    if not is_valid_breed(cat.breed):
        raise HTTPException(status_code=400, detail="Invalid cat breed")

    db_cat = models.SpyCat(**cat.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat


@router.delete("/{cat_id}", status_code=204)
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    db_cat = db.query(models.SpyCat).filter(models.SpyCat.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    db.delete(db_cat)
    db.commit()
    return {"message": "Cat deleted successfully"}


@router.patch("/{cat_id}/salary", response_model=schemas.SpyCat)
def update_cat_salary(cat_id: int, salary: float, db: Session = Depends(get_db)):
    if salary < 0:
        raise HTTPException(status_code=400, detail="Salary must be a positive number")

    db_cat = db.query(models.SpyCat).filter(models.SpyCat.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    db_cat.salary = salary
    db.commit()
    db.refresh(db_cat)
    return db_cat


@router.get("/", response_model=List[schemas.SpyCat])
def list_cats(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.SpyCat).offset(skip).limit(limit).all()


@router.get("/{cat_id}", response_model=schemas.SpyCat)
def get_cat(cat_id: int, db: Session = Depends(get_db)):
    db_cat = db.query(models.SpyCat).filter(models.SpyCat.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")
    return db_cat
