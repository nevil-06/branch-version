from typing import List
from sqlalchemy.orm import Session
from src.entry.model import Entry
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.utils.db_session_create import get_db
from fastapi import APIRouter, Depends, status
from src.entry.schema import EntryTable, EntryResponse


entry_router = APIRouter()


#get all entries that are not deleted
@entry_router.get('/entries/all', status_code = status.HTTP_200_OK, response_model= List[EntryResponse])
def get_all_entries(db: Session = Depends(get_db)):
    entries = db.query(Entry).filter(Entry.is_deleted != True).all()
    return entries


#get 1 entry that is not deleted
@entry_router.get('/entry/{id}', status_code= status.HTTP_200_OK, response_model= EntryResponse)
def get_entry(entry_id: str, db: Session = Depends(get_db)):
    entry = db.query(Entry).filter(Entry.id == id, Entry.is_deleted != True).first()
    if entry:
        return entry



#get entries that are deleted
@entry_router.get('/entries/del', status_code = status.HTTP_200_OK, response_model= List[EntryResponse])
def get_all_deleted_entries(db: Session = Depends(get_db)):
    entries = db.query(Entry).filter(Entry.is_deleted == True).all()
    return entries


#admin function to see full data 
@entry_router.get('/admin/entries/all')
def admin_get_all_entries(db: Session = Depends(get_db)):
        entries = db.query(Entry).filter(Entry.is_deleted != True).all()
        return entries


#create                   
@entry_router.post('/entries', status_code = status.HTTP_201_CREATED)
def create_entry(entry: EntryTable, db: Session = Depends(get_db)):
    db_entry = db.query(Entry).filter(Entry.name == entry.name).first()
    
    if db_entry is not None:
        return {"message": "Entry already exists"}

    new_entry = Entry(
    name = entry.name,
    status =entry.status,
    country = entry.country,
    state = entry.state,
    comp_id = entry.comp_id)

    db.add(new_entry)
    db.commit()
    return new_entry


#update entry that are available
@entry_router.put('/entry/{id}',status_code = status.HTTP_202_ACCEPTED, response_model= EntryResponse)
def update_entry(id: str, entry: EntryTable, db: Session = Depends(get_db)):
    updateentry = db.query(Entry).filter(Entry.id == id).first()
    if updateentry:
        updateentry.update(entry.dict())
        db.add(updateentry)
        db.commit()
        return updateentry
    else:
        return {"message": f"Entry details for id: {id} is deleted so cannot update"}
    


#delete entry using entry_id
@entry_router.delete('/entry/{id}')
def delete_entry(id: str, db: Session = Depends(get_db)):
    deleteentry = db.query(Entry).filter(Entry.id == id).first()

    if deleteentry.is_deleted != True:
        deleteentry.is_deleted = True
        db.commit()
        return {"message": "entry is deleted successfully"}
    elif deleteentry.is_deleted == True:
        return {"message": "entry is already deleted"}

# end of entry routes
