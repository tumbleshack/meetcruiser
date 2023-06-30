import os

import boto3
import psycopg2
from sqlalchemy import make_url


def get_new_connection(uri):
    db_url = make_url(uri)
    endpoint = db_url.host
    port = db_url.port
    user = db_url.username
    region = db_url.host.split(".")[2]
    dbname = db_url.database

    session = boto3.Session()
    client = session.client("rds")

    token = client.generate_db_auth_token(
        DBHostname=endpoint, Port=port, DBUsername=user, Region=region
    )
    print("Generated token, connecting to RDS")
    conn = psycopg2.connect(
        host=endpoint,
        port=port,
        database=dbname,
        user=user,
        password=token,
        connect_timeout=5,
    )
    print("Connected to RDS")
    return conn
