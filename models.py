from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    def to_dict(self) -> dict:
        return {"id": self.id, "name": self.name}


class MenuItem(Base):
    __tablename__ = "menu_item"

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey("restaurant.id"))
    restaurant = relationship(Restaurant)

    def to_dict(self) -> dict:
        """Returns object data in easily serializable format"""
        return {
            "name": self.name,
            "description": self.description,
            "id": self.id,
            "price": self.price,
            "course": self.course,
        }


engine = create_engine("sqlite:///restaurantmenu.db")


Base.metadata.create_all(engine)
