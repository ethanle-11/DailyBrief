from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Briefing
from app.schemas import BriefingResponse
from app.services.dining import get_lunch_menu

app = FastAPI()

@app.get("/")
def root():
    return {"message": "DailyBrief API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

# Briefings

@app.get("/briefings", response_model=list[BriefingResponse])
def get_briefings(db: Annotated[Session, Depends(get_db)]):
    statement = select(Briefing)
    briefings = db.scalars(statement).all()
    return briefings

@app.post("/briefings", response_model=BriefingResponse)
def create_briefing(db: Annotated[Session, Depends(get_db)]):
    briefing = Briefing()

    db.add(briefing)
    db.commit()
    db.refresh(briefing)

    return briefing

# Dining

@app.get("/dining/lunch")
def get_lunch():
    return get_lunch_menu()