from src.utils.db import create_engine_with_connection_pool
from sqlalchemy.engine.base import Connection
from sqlalchemy.exc import SQLAlchemyError 
from src.config.logging import logger
from sqlalchemy import text
from typing import Optional
from typing import Dict
import hashlib
import bcrypt


engine = create_engine_with_connection_pool()


def check_password(plain_password: str, retrieved_password: bytes) -> bool:
    """
    Checks if the provided plain text password matches the stored hashed password.
    
    Args:
        plain_password (str): The plain text password to verify.
        retrieved_password (bytes): The hashed password retrieved from the database.
        
    Returns:
        bool: True if the passwords match, False otherwise.
    """
    if isinstance(retrieved_password, str):
        retrieved_password = retrieved_password.encode('utf-8')
    return bcrypt.checkpw(plain_password.encode('utf-8'), retrieved_password)


def execute_safe_query(connection: Connection, query: str, params: Optional[Dict] = None) -> None:
    """
    Executes a SQL query safely, handling any potential SQLAlchemy errors.
    
    Args:
        connection (Connection): A SQLAlchemy Connection object.
        query (str): The SQL query to execute.
        params (Optional[Dict]): Parameters to use with the query.
    """
    try:
        connection.execute(text(query), params)
    except SQLAlchemyError as e:
        logger.error(f"Database query failed: {e}")
        raise


def create_users_table() -> None:
    """
    Creates the 'users' table in the database if it does not already exist.
    """
    create_table_statement = """
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(255) NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            team VARCHAR(255),
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (username)
        );
    """
    with engine.begin() as connection:
        execute_safe_query(connection, create_table_statement)
        logger.info("Table 'users' created successfully.")


def insert_user(user_data: Dict[str, str]) -> None:
    """
    Inserts a new user into the 'users' table.
    
    Args:
        user_data (Dict[str, str]): A dictionary containing the user data.
    """
    insert_stmt = f"""
        INSERT INTO users (username, password_hash, first_name, last_name, team)
        VALUES (:username, :password_hash, :first_name, :last_name, :team)
    """
    with engine.begin() as connection:
        execute_safe_query(connection, insert_stmt, user_data)
        logger.info(f"User {user_data['username']} inserted successfully.")


def username_exists(username: str) -> bool:
    """
    Checks if the given username already exists in the 'users' table.
    
    Args:
        username (str): The username to check.
        
    Returns:
        bool: True if the username exists, False otherwise.
    """
    query = "SELECT EXISTS(SELECT 1 FROM users WHERE username = :username)"
    with engine.connect() as connection:
        try:
            result = connection.execute(text(query), {'username': username}).scalar()
            return result
        except SQLAlchemyError as e:
            logger.error(f"Failed to check if username {username} exists: {e}")
            raise


def authenticate_user(username: str, password: str) -> bool:
    """
    Authenticates a user by verifying their username and password.
    
    Args:
        username (str): The user's username.
        password (str): The user's password.
        
    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    query = "SELECT password_hash FROM users WHERE username = :username"
    with engine.connect() as connection:
        try:
            result = connection.execute(text(query), {'username': username}).fetchone()
            if result is not None:
                hashed_password = result[0]
                return check_password(password, hashed_password)
            return False
        except SQLAlchemyError as e:
            logger.error(f"Authentication failed for user {username}: {e}")
            raise


def generate_hash(username, query, feedback, vote):
    """
    Generates a SHA-256 hash from the concatenation of the given fields.
    """
    hash_input = f"{username}{query}{feedback}{vote}".encode('utf-8')
    return hashlib.sha256(hash_input).hexdigest()


def check_hash_exists(hash_value):
    """
    Checks if a given hash already exists in the feedback table.
    """
    query = text("SELECT EXISTS(SELECT 1 FROM feedback WHERE unique_hash = :hash_value)")
    with engine.begin() as connection:
        result = connection.execute(query, {'hash_value': hash_value}).fetchone()
        return result[0]


def create_feedback_table() -> None:
    """
    Creates the 'feedback' table in the database if it does not already exist.
    """
    create_table_statement = """
    CREATE TABLE IF NOT EXISTS feedback (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        username VARCHAR(255) NOT NULL,
        query TEXT,
        title TEXT,
        snippet TEXT,
        url VARCHAR(255),
        feedback TEXT,
        is_relevant ENUM('Yes', 'No', 'NA'),
        feedback_given_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        match_rank INT,
        unique_hash VARCHAR(255) UNIQUE,
        company VARCHAR(255),
        report_type VARCHAR(255),
        country VARCHAR(255),
        year INT,
        FOREIGN KEY (username) REFERENCES users(username)
    );
    """
    with engine.begin() as connection:
        execute_safe_query(connection, create_table_statement)
        logger.info("Table 'feedback' created successfully.")


def insert_feedback(feedback_data):
    """
    Inserts feedback into the database if the hash is unique.
    """
    # Compute the hash including feedback text
    hash_value = generate_hash(
        feedback_data['username'],
        feedback_data['query'],
        feedback_data['feedback'],
        feedback_data['is_relevant']
    )

    # Check if the hash exists
    if check_hash_exists(hash_value):
        print("Duplicate feedback detected. Skipping insertion.")
        return False

    # Prepare the insert query using the text function
    insert_query = text("""
        INSERT INTO feedback (timestamp, username, query, title, snippet, url, feedback, is_relevant, feedback_given_timestamp, match_rank, unique_hash, company, report_type, country, year)
        VALUES (:timestamp, :username, :query, :title, :snippet, :url, :feedback, :is_relevant, :feedback_given_timestamp, :match_rank, :unique_hash, :company, :report_type, :country, :year)
    """)

    # Add the computed hash to the feedback data
    feedback_data['unique_hash'] = hash_value

    # Execute the query with parameters passed as a dictionary
    with engine.begin() as connection:
        connection.execute(insert_query, feedback_data)  # Pass feedback_data as a dictionary
        print("Feedback inserted successfully.")
        return True


def create_tables() -> None:
    """
    Creates necessary tables in the database.
    """
    try:
        create_users_table()
        create_feedback_table()
        logger.info("All necessary tables created successfully.")
    except Exception as e:
        logger.error(f"Failed to create tables: {e}")


if __name__ == "__main__":
    create_tables()