"""
Create database in blank development environment.

This script is used in the  setup process. Its
sole purpose is to delete a postgres database
from database connection environment variables.

Usage: python3 -m script.create_database
"""

import sqlalchemy
import sys
from ..env import getenv
from ..database import engine

# Ensures that the script can only be run in development mode
if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)

with engine.connect() as connection:
    connection.execute(
        sqlalchemy.text("COMMIT")
    ) 
    database = getenv("POSTGRES_DATABASE")
    stmt = sqlalchemy.text(f"DROP DATABASE {database}")
    connection.execute(stmt)
