#!/usr/bin/env python3
"""
main.py - Main file to demonstrate usage of implemented functionalities
"""


import logging

from filtered_logger import filter_datum, RedactingFormatter, get_logger, get_db, main as log_filtered_data
from encrypt_password import hash_password, is_valid


def main():
    # 1. Filtering Log Messages
    print("Filtering Log Messages:")
    fields = ["password", "date_of_birth"]
    messages = [
        "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;",
        "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"
    ]
    for message in messages:
        filtered_message = filter_datum(fields, 'xxx', message, ';')
        print(filtered_message)

    print("\n")

    # 2. Using Logger with RedactingFormatter
    print("Using Logger with RedactingFormatter:")
    message = "name=Bob;email=bob@dylan.com;ssn=000-123-0000;password=bobby2019;"
    log_record = logging.LogRecord("my_logger", logging.INFO, None, None, message, None, None)
    formatter = RedactingFormatter(fields=("email", "ssn", "password"))
    formatted_log = formatter.format(log_record)
    print(formatted_log)
    
    print("\n")

    # 3. Connecting to Secure Database and Logging Filtered Data
    print("Connecting to Secure Database and Logging Filtered Data:")
    log_filtered_data()  # This will log filtered data from the database

    print("\n")

    # 4. Hashing and Validating Passwords
    print("Hashing and Validating Passwords:")
    password = "MyAmazingPassw0rd"
    hashed_password = hash_password(password)
    print(hashed_password)
    print(is_valid(hashed_password, password))


if __name__ == "__main__":
    main()
