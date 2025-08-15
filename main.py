"""
Root-level entry point for the data generator service.

Usage:
    python main.py

This simply imports and calls the `main()` function from data_generator.app.main.
"""

from data_generator.app.main import main as run_generator

if __name__ == "__main__":
    run_generator()