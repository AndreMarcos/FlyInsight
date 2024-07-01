from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class BaseDAO:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.Session()
