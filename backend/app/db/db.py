from sqlmodel import SQLModel, create_engine, Session
from app.core.settings import settings
from app.db.seed import seed

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  
    connect_args={"check_same_thread": False}
)

def init_db():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        if settings.ENV == "development":
            seed(session)

def get_session():
    with Session(engine) as session:
        yield session