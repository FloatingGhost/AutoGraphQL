from schema.schema import make_schema
import os
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pytest


@pytest.fixture
def db_connection():
    engine = create_engine("sqlite:///test.db", echo=True)
    Sessiongen = sessionmaker(bind=engine)
    session = Sessiongen()
    return session


@pytest.fixture
def schema():
    s = make_schema("sqlite:///test.db", ["parent", "child"])
    return s


def test_db_creation():
    from tests import make_test_db


def test_schema_generation():
    schema = make_schema("sqlite:///test.db", ["parent"])
    return schema


def test_schema_top_level(db_connection, schema):
    query = """
    query {
        parent {
            edges {
                node {
                    name
                }
            }
        }
    }
    """

    expected_result = {
        "parent": {
            "edges": [
                {"node": {"name": "Alice"}}
            ]
        }
    }

    data = schema.execute(query, context={"session": db_connection}).data
    assert(dict(data) == expected_result)


def test_child_connection(db_connection, schema):
    query = """
    query {
        parent {
            edges {
                node {
                    name,
                    childCollection {
                        edges {
                            node {
                                name
                            }
                        }
                    }
                }
            }
        }
    }
    """

    expected_result = {
        "parent": {
            "edges": [
                {"node": {
                   "name": "Alice",
                   "childCollection": {
                        "edges": [
                            {"node": {"name": "Bob"}},
                            {"node": {"name": "Catherine"}},
                            {"node": {"name": "Dave"}}
                        ]
                    }
                }}
            ]
        }
    }

    data = schema.execute(query, context={"session": db_connection}).data
    assert(dict(data) == expected_result)


def test_many_to_many(db_connection, schema):
    query = """
    query {
        child {
            edges {
                node {
                    name,
                    friendCollection {
                        edges {
                            node {
                                name,
                                childCollection {
                                    edges {
                                        node {
                                            name
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    """

    expected_result = {
        "child": {
            "edges": [
                {"node": {
                    "name": "Bob",
                    "friendCollection": {
                        "edges": [
                            {"node": {
                                "name": "Gavin",
                                "childCollection": {
                                    "edges": [
                                        {"node": {"name": "Bob"}},
                                        {"node": {"name": "Catherine"}}
                                    ]
                                }
                            }}
                        ]
                    }
                }},
                {"node": {      
                    "name": "Catherine",
                    "friendCollection": {
                        "edges": [  
                            {"node": {   
                                "name": "Gavin",
                                "childCollection": {
                                    "edges": [    
                                        {"node": {"name": "Bob"}},
                                        {"node": {"name": "Catherine"}}
                                    ]
                                }
                            }},
                            {"node": {
                                "name": "Hackerman",
                                "childCollection": {
                                    "edges": [ 
                                        {"node": {"name": "Catherine"}},
                                        {"node": {"name": "Dave"}}
                                    ]
                                }
                            }}
                        ]   
                    }
                }},
                {"node": {      
                    "name": "Dave",
                    "friendCollection": {
                        "edges": [  
                            {"node": {   
                                "name": "Hackerman",
                                "childCollection": {
                                    "edges": [    
                                        {"node": {"name": "Catherine"}},
                                        {"node": {"name": "Dave"}}
                                    ]
                                }
                            }}
                        ]   
                    }
                }}
            ]
        }
    } 

    data = schema.execute(query, context={"session": db_connection}).data
    assert(dict(data) == expected_result)
    

def test_remove_db():
    os.unlink(os.path.join(os.path.abspath(os.curdir), "test.db"))
