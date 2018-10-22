from graphene import ObjectType, Schema
from graphene.relay import Node
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField


def make_schema(connection_string: str, top_level_fields: list):
    """Make a graphQL schema from an existing SQL database

    Args:
        connection_string (str): Standard SQLAlchemy DB conn string
        top_level_fields (list): List of table names to have as the top-level types

    Returns:
        schema (graphene.Schema): Schema all ready to use

    Notes:
        Relies heavily on foreign keys to find relationships, so make sure
        you have them!
    """

    base_class = automap_base()
    engine = create_engine(connection_string)
    base_class.prepare(engine, reflect=True)
    session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    base_class.query = session.query_property()

    query_properties = {"node": Node.Field()}

    for (cls, model) in base_class.classes.items():
        meta = type("Meta", (), {"model": model, "interfaces": (Node, )})
        subclass = type(cls, (SQLAlchemyObjectType, ), {"Meta": meta})

        if cls in top_level_fields:
            query_properties[cls] = SQLAlchemyConnectionField(subclass)

    Query = type("Query", (ObjectType, ), query_properties)

    return Schema(query=Query)
