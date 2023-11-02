#!/usr/bin/env python3
"""
Obfuscating a log message using regular expression
"""


from typing import List
import re


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
