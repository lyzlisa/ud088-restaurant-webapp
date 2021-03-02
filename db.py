from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "sqlite:///restaurantmenu.db",
    connect_args={"check_same_thread": False},
)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
