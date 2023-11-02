#!/usr/bin/env python3
"""
1. Obfuscating a log message using regular expression.
2. Getting a configured logger for logging user data.
3. Establishing and creating connection to MySQL database
using environment variables.
4. Retrieve user data from the database
and log it using a configured logger
"""


import os
import mysql.connector
from typing import List
import re
import logging


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """
    Obfuscating a log message using regular expression.

    Args:
     fields (list[str]):
     list of strings representing fields to obfuscate.
     redaction (str):
     string representing how the field will be obfuscated.
     message (str):
     string representing the log line.
     separator (str):
    string representing the character separating all fields in the log line.

    Returns:
    - str: The obfuscated log message.
    """
    return re.sub(
        fr'({separator.join(fields)})=[^\\{separator}]+',
        rf'\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initializing the RedactingFormatter
        with the specified fields to redact.

        Args:
        - fields (List[str]):
        list of strings representing fields to redact in log records.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formatting the log record by redacting specified fields.

        Args:
        - record (logging.LogRecord): The log record to be formatted.

        Returns:
        - str: The formatted log message with specified fields redacted.
        """
        log_message = super(RedactingFormatter, self).format(record=record)
        return filter_datum(self.fields, self.REDACTION, log, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Getting a configured logger for logging user data.

    Returns:
    logging.Logger:
    The configured logger named "user_data" with specific settings.
    """
    # Create a logger named "user_data"
    user_data_logger = logging.getLogger('user_data')
    user_data_logger.setLevel(logging.INFO)

    # Disable propagation to other loggers
    user_data_logger.propagate = False

    # Create a StreamHandler with a RedactingFormatter using PII_FIELDS
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))

    # Add the StreamHandler to the logger
    user_data_logger.addHandler(stream_handler)

    return user_data_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Establishing and creating connection to MySQL database
    using environment variables

    Returns:
    mysql.connector.connection.MySQLConnection:
    The database connection object.
    """
    # Retrieving database credentials from environment variables
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    # Creating a connection to the database
    db_connection = mysql.connector.connect(
        user=db_username,
        password=db_password,
        host=db_host,
        database=db_name
    )

    return db_connection


def main() -> None:
    """
    Retrieve user data from the database
    and log it using a configured logger.
    """
    # Establish a database connection
    db_connection = get_db()

    # Initialize a logger
    user_data_logger = get_logger()

    # Create a cursor to interact with the database
    cursor = db_connection.cursor()

    # Execute the SQL query to retrieve user data
    cursor.execute("SELECT * FROM users")

    # Fetch all rows from the query result
    rows = cursor.fetchall()

    # Process and log each row
    for row in rows:
        user_data_entry = (
            "name={}; email={}; phone={}; ssn={}; "
            "password={}; ip={}; last_login={}; user_agent={};"
        ).format(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        user_data_logger.info(user_data_entry)

    # Close the cursor and the database connection
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    main()
