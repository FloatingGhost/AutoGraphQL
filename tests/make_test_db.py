from sqlalchemy import create_engine, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///test.db", echo=True)
Sessiongen = sessionmaker(bind=engine)
session = Sessiongen()

base = declarative_base()


class Parent(base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    children = relationship("Child", back_populates="parent")


child_has_friend = Table("child_has_friend", base.metadata,
    Column("child_id", ForeignKey("child.id"), primary_key=True),
    Column("friend_id", ForeignKey("friend.id"), primary_key=True)
)

class Child(base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    parent_id = Column(Integer, ForeignKey("parent.id"))
    children = relationship("Grandchild", back_populates="parent")
    parent = relationship("Parent", back_populates="children")
    friends = relationship("Friend", secondary=child_has_friend, back_populates="friends")

class Grandchild(base):
    __tablename__ = "grandchild"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    parent_id = Column(Integer, ForeignKey("child.id"))
    parent = relationship("Child", back_populates="children")


class Friend(base):
    __tablename__ = "friend"
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    friends = relationship("Child", secondary=child_has_friend, back_populates="friends")

base.metadata.create_all(engine)

p1 = Parent(name="Alice")
c1 = Child(name="Bob", parent=p1)
c2 = Child(name="Catherine", parent=p1)
c3 = Child(name="Dave", parent=p1)
gc1 = Grandchild(name="Ed", parent=c1)
gc2 = Grandchild(name="Fax Machine", parent=c2)
f1 = Friend(name="Gavin", friends=[c1, c2])
f2 = Friend(name="Hackerman", friends=[c2, c3])
 
session.add(p1)
session.add(c1)
session.add(c2)
session.add(gc1)
session.add(gc2)
session.add(f1)
session.add(f2)

session.commit()
session.close_all()
