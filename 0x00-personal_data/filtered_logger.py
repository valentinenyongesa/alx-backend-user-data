#!/usr/bin/env python3
"""
Module for filtering log data.
"""

import logging
import re
from typing import List


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        record.message = self.filter_message(record.message)
        return super().format(record)

    def filter_message(self, message: str) -> str:
        for field in self.fields:
            message = self.filter_datum([field], self.REDACTION, message, self.SEPARATOR)
        return message

def filter_datum(fields, redaction, message, separator):
    """
    Replace occurrences of specified fields in the log message with redaction.

    Args:
        fields (list of str): Fields to obfuscate.
        redaction (str): String representing the redaction.
        message (str): Log message.
        separator (str): Separator character between fields in the log message.

    Returns:
        str: Log message with specified fields obfuscated.
    """
    import re
    return re.sub(r'(?:{}=)(.*?)(?={})'.format('|'.join(fields), re.escape(separator)), redaction, message)
