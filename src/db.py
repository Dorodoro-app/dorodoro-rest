from sqlalchemy import create_engine

db_string = "postgresql://postgres:12345678@localhost:5432/dorodoro"

db = create_engine(db_string)
