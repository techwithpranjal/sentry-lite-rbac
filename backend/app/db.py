from sqlmodel import SQLModel, create_engine, Session
from app.core.settings import settings

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  
    connect_args={"check_same_thread": False}
)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session