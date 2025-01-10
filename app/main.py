from fastapi import FastAPI
from app.database import Base, engine
from app.routes import cats, missions

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(cats.router)
app.include_router(missions.router)
