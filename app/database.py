from neo4j import GraphDatabase, basic_auth
from .models import DbCredentials

def get_neo4j_driver(creds: DbCredentials):
    return GraphDatabase.driver(
        creds.uri, 
        auth=basic_auth(creds.user, creds.password)
    )

def determine_type(value):
    if isinstance(value, (int)): return "int"
    if isinstance(value, (float)): return "float"
    if isinstance(value, (bool)): return "boolean"
    from datetime import datetime
    if isinstance(value, datetime): return "datetime"
    return "string"