"""
app package for the data generator.

This package contains:
- main.py       : Entry point
- config.py     : Loads environment variables and settings
- db.py         : Database connection, schema, and insert helpers
- rules.py      : Rule engine logic
- generator.py  : Synthetic record generator
- logging.py    : Logging setup
"""
__all__ = ["config", "db", "rules", "generator", "logging", "main"]
__version__ = "0.1.0"
