from src.database_files.database import SessionLocal

def get_db():
    try:
        db = SessionLocal()
        return db
    except AttributeError:
        print("Can not get the DB.")