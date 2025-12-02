from __future__ import annotations

"""
MAGIC Week 0 shim for scripts.fastjsonschema_exceptions.

Goal
----
- Provide the exception classes that scripts.error_reporting expects:
    * JsonSchemaException
    * JsonSchemaValueException
    * JsonSchemaDefinitionException
- Keep behaviour very small and import-safe.
"""

class JsonSchemaException(Exception):
    """
    Base exception for JSON schema related errors.
    """
    pass


class JsonSchemaDefinitionException(JsonSchemaException):
    """
    Raised for errors in the JSON schema *definition* itself.
    """
    pass


class JsonSchemaValueException(JsonSchemaException):
    """
    Raised when a value does not conform to the JSON schema.
    """
    pass


__all__ = [
    "JsonSchemaException",
    "JsonSchemaDefinitionException",
    "JsonSchemaValueException",
]
