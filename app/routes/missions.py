from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/missions", tags=["Missions and Targets"])


@router.post("/", response_model=schemas.Mission)
def create_mission(mission: schemas.MissionCreate, db: Session = Depends(get_db)):
    db_mission = models.Mission(complete=False)
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)

    for target in mission.targets:
        db_target = models.Target(
            name=target.name,
            country=target.country,
            notes=target.notes,
            complete=target.complete,
            mission_id=db_mission.id
        )
        db.add(db_target)

    db.commit()
    db.refresh(db_mission)
    return db_mission


@router.delete("/{mission_id}", status_code=204)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    db_mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if db_mission.cat_id:
        raise HTTPException(status_code=400, detail="Cannot delete a mission assigned to a cat")

    db.delete(db_mission)
    db.commit()
    return {"message": "Mission deleted successfully"}


@router.patch("/{mission_id}/targets/{target_id}", response_model=schemas.TargetUpdate)
def update_target(mission_id: int, target_id: int, target_update: schemas.TargetUpdate,
                  db: Session = Depends(get_db)):
    db_target = db.query(models.Target).filter(models.Target.id == target_id,
                                               models.Target.mission_id == mission_id).first()

    if not db_target:
        raise HTTPException(status_code=404, detail="Target not found")

    db_mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if db_mission.complete or db_target.complete:
        raise HTTPException(status_code=400, detail="Cannot update a completed target or mission")

    if target_update.notes is not None:
        db_target.notes = target_update.notes
    if target_update.complete is not None:
        db_target.complete = target_update.complete

    db.commit()
    db.refresh(db_target)
    return target_update



@router.patch("/{mission_id}/complete", response_model=schemas.Mission)
def complete_mission(mission_id: int, db: Session = Depends(get_db)):
    db_mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    incomplete_targets = db.query(models.Target).filter(models.Target.mission_id == mission_id,
                                                        models.Target.complete == False).all()
    if incomplete_targets:
        raise HTTPException(status_code=400, detail="Cannot complete mission with incomplete targets")

    db_mission.complete = True

    if db_mission.cat_id:
        db_mission.cat_id = None

    db.commit()
    db.refresh(db_mission)
    return db_mission


@router.patch("/{mission_id}/assign-cat/{cat_id}", response_model=schemas.Mission)
def assign_cat_to_mission(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    db_mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()

    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    if db_mission.cat_id:
        raise HTTPException(status_code=400, detail="Mission already assigned to a cat")

    db_cat = db.query(models.SpyCat).filter(models.SpyCat.id == cat_id).first()
    if not db_cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    existing_mission = db.query(models.Mission).filter(models.Mission.cat_id == cat_id, models.Mission.complete == False).first()
    if existing_mission:
        raise HTTPException(status_code=400, detail="Cat is already assigned to another active mission")

    db_mission.cat_id = cat_id
    db.commit()
    db.refresh(db_mission)
    return db_mission


@router.get("/", response_model=List[schemas.Mission])
def list_missions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Mission).offset(skip).limit(limit).all()


@router.get("/{mission_id}", response_model=schemas.Mission)
def get_mission(mission_id: int, db: Session = Depends(get_db)):
    db_mission = db.query(models.Mission).filter(models.Mission.id == mission_id).first()
    if not db_mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return db_mission
