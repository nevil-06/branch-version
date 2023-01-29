from typing import List
from sqlalchemy.orm import Session
from src.user.schema import User
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status
from src.competition.model import Competition
from src.utils.db_session_create import get_db
from src.competition.schema import CompetitionResponse, CompetitionTable


competiton_router = APIRouter()


#competiton routes that are not deleted
@competiton_router.get('/competitons/all', status_code = status.HTTP_200_OK, response_model= List[CompetitionResponse])
def get_all_competitions(db: Session = Depends(get_db)):
    competitons = db.query(Competition).filter(Competition.is_deleted != True).all()
    return competitons


#get 1 competiton that is not deleted
@competiton_router.get('/competiton/{id}', status_code = status.HTTP_200_OK, response_model= CompetitionResponse)
def get_competition(id: str, db: Session = Depends(get_db)):
    competiton = db.query(Competition).filter(Competition.id == id, Competition.is_deleted != True).first()
    return competiton


#competiton routes that are deleted
@competiton_router.get('/competitons/del', status_code = status.HTTP_200_OK, response_model= List[CompetitionResponse])
def get_all_deleted_competitions(db: Session = Depends(get_db)):
    competitons = db.query(Competition).filter(Competition.is_deleted == True).all()
    return competitons


#admin function to see full data 
@competiton_router.get('/admin/competitons/all')
def admin_get_all(db: Session = Depends(get_db)):
        competitons = db.query(Competition).filter(Competition.is_deleted != True).all()
        return competitons



#create new competition details                
@competiton_router.post('/competitons', status_code = status.HTTP_201_CREATED)
def create_competition(competiton: CompetitionTable, db: Session = Depends(get_db)):
    create_comptetition= db.query(Competition).filter(Competition.name == competiton.name, User.is_deleted != True).first()
    
    if create_comptetition:
        return {"message": "Competiton details already exists"}
    else:
        new_competition = Competition(
            name = competiton.name,
            status = competiton.status,
            url = competiton.url,        
            user_id = competiton.user_id
        )
        db.add(new_competition)
        db.commit()
        return new_competition


#update
@competiton_router.put('/competiton/{id}', status_code = status.HTTP_202_ACCEPTED, response_model= CompetitionResponse)
def update_competition(id: str, competiton: CompetitionTable, db: Session = Depends(get_db)):
    updatecompetition = db.query(Competition).filter(Competition.id == id, Competition.is_deleted != True).first()
    
    if updatecompetition:
        updatecompetition.update(competiton.dict())
        db.add(updatecompetition)
        db.commit()
        return updatecompetition
    else:
        return {"message": f"competiton with id: {id} is deleted so cannot update"}



#delete
@competiton_router.delete('/competiton/{id}')
def delete_competition(id: str, db: Session = Depends(get_db)):
    deletecompetition = db.query(Competition).filter(Competition.id == id).first()
    if deletecompetition.is_deleted != True:
        deletecompetition.is_deleted = True
        db.commit()
        return {"message": "competiton details deleted successfully"}
    elif deletecompetition.is_deleted == True:
        return {"message": "competiton details already deleted"}

# end of competiton routes
