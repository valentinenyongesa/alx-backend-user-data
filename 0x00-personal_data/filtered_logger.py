#!/usr/bin/env python3
"""
filtered_logger.py - Module for logging and filtering sensitive data
"""

import logging
import re
import os
import mysql.connector
from typing import List, Tuple

class RedactingFormatter(logging.Formatter):
    """
    RedactingFormatter - Custom log formatter to redact specified fields in log messages
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record and redact specified fields
        """
        message = super().format(record)
        return self.filter_datum(message, self.fields, self.REDACTION, self.SEPARATOR)

    @staticmethod
    def filter_datum(message: str, fields: List[str], redaction: str, separator: str) -> str:
        """
        Replace specified fields with redaction in the log message
        """
        return re.sub(
            fr'(?<={separator}|^)({"|".join(fields)})=([^{separator}]*)',
            lambda x: f'{x.group(1)}={redaction}',
            message
        )

PII_FIELDS: Tuple[str, ...] = ("name", "email", "phone", "ssn", "password")

def get_logger() -> logging.Logger:
    """
    Return a configured logging.Logger object with RedactingFormatter
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    
    logger.addHandler(stream_handler)
    
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Connect to the database using environment variables and return a MySQL connection
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    dbname = os.getenv("PERSONAL_DATA_DB_NAME")

    db = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=dbname
    )

    return db

def main() -> None:
    """
    Retrieve and log filtered data from the database using the configured logger and formatter
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    
    for row in cursor.fetchall():
        formatted_row = "; ".join(f"{field}={value}" for field, value in zip(cursor.column_names, row))
        logger.info(formatted_row)
    
    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
