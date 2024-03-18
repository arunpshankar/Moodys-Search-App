from google.cloud.sql.connector import Connector
from sqlalchemy.engine.base import Connection
from sqlalchemy.engine.base import Engine
from src.config.logging import logger
from sqlalchemy import create_engine
from src.config.setup import config
import bcrypt

# Global variables
INSTANCE_CONNECTION_NAME = f"{config.PROJECT_ID}:{config.REGION}:{config.CLOUD_SQL_INSTANCE}"

# Initialize Connector object globally to reuse
connector = Connector()

# This will hold the connection object once it's created
_connection = None

# Added to track if the connection has been logged
_connection_established_logged = False

def get_connection() -> Connection:
    """
    Establishes a connection to the Cloud SQL instance or returns the existing connection if already established.
    Logs the connection establishment only the first time.

    Returns:
        A connection object to the Cloud SQL database.
    """
    global _connection, _connection_established_logged  # Reference the global variables to modify them
    if _connection is None:  # Check if the connection does not already exist
        try:
            _connection = connector.connect(
                INSTANCE_CONNECTION_NAME,
                "pymysql",
                user=config.CLOUD_SQL_USERNAME,
                password=config.CLOUD_SQL_PASSWORD,
                db=config.CLOUD_SQL_DATABASE
            )
            if not _connection_established_logged:
                logger.info("Successfully established connection to Cloud SQL.")
                _connection_established_logged = True  # Ensure this log happens only once
        except Exception as e:
            logger.error(f"Failed to connect to Cloud SQL: {e}")
            raise
    return _connection

def create_engine_with_connection_pool() -> Engine:
    """
    Creates a SQLAlchemy engine with a connection pool using the `get_connection` function.

    Returns:
        A SQLAlchemy engine object.
    """
    engine = create_engine("mysql+pymysql://", creator=get_connection)
    return engine

def encrypt_password(password: str) -> bytes:
    """
    Generates a salt and hashes the provided password.
    
    Args:
        password (str): The plain text password to hash.
        
    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
