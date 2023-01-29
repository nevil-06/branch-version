from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from src.entry.model import Entry


class EntryResponse(BaseModel):
    name : Optional[str]
    status : Optional[str]
    country : Optional[str]
    state : Optional[str]
    
    class  Config:
        orm_mode= True

class EntryTable(EntryResponse):
    id : Optional[UUID]
    is_deleted : Optional[bool]
    created_at : Optional[str]
    updated_at : Optional[str]
    comp_id : Optional[str]
    

class EntryReq(EntryResponse):
    pass
