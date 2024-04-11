#!/usr/bin/env python3
"""
Module for filtering log data.
"""

import re

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
    return re.sub(r'(?:{}=)(.*?)(?={})'.format('|'.join(fields), re.escape(separator)), redaction, message)
