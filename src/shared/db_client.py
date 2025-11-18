"""
Virgin Voyages MXP Database Client.

This module provides a Python client for direct database access to the MXP SQL Server.
It uses pymssql for connecting to the database (better SQL Server auth support on Mac/Linux).
"""

import os
from contextlib import contextmanager
from typing import Any, Generator

import pymssql
from dotenv import load_dotenv

# Load environment variables from .env file
_ = load_dotenv()

# Database Configuration
DB_SERVER = os.getenv("DB_SERVER", "C-LAB-MX-AG-LIS.virginvoyages.qa.dev")
DB_PORT = os.getenv("DB_PORT", "1442")
DB_DATABASE = os.getenv("DB_DATABASE", "mxp")
DB_USERNAME = os.getenv("DB_USERNAME", "OnboardAmenityTool")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def get_connection() -> pymssql.Connection:
    """
    Create a new database connection using pymssql.

    Returns:
        pymssql Connection object

    Raises:
        pymssql.Error: If connection fails
    """
    return pymssql.connect(
        server=DB_SERVER,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_DATABASE,
        tds_version="7.4",
    )


@contextmanager
def get_db_connection() -> Generator[pymssql.Connection, None, None]:
    """
    Context manager for database connections.
    Automatically closes the connection when done.

    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM table")
            results = cursor.fetchall()

    Yields:
        pymssql Connection object
    """
    conn = None
    try:
        conn = get_connection()
        yield conn
    finally:
        if conn:
            conn.close()


@contextmanager
def get_db_cursor() -> Generator[pymssql.Cursor, None, None]:
    """
    Context manager for database cursor.
    Automatically commits and closes the connection when done.

    Usage:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM table")
            results = cursor.fetchall()

    Yields:
        pymssql Cursor object
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except Exception:
        if conn:
            conn.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def execute_query(query: str, params: tuple = ()) -> list[tuple]:
    """
    Execute a SELECT query and return all results.

    Args:
        query: SQL query string
        params: Query parameters (use %s placeholders in query)

    Returns:
        List of tuples from the query result

    Example:
        results = execute_query("SELECT * FROM Person WHERE PIN = %s", (12345,))
        for row in results:
            print(row[0], row[1])  # Access by index
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result if result else []


def execute_query_dict(query: str, params: tuple = ()) -> list[dict[str, Any]]:
    """
    Execute a SELECT query and return results as list of dictionaries.

    Args:
        query: SQL query string
        params: Query parameters (use %s placeholders in query)

    Returns:
        List of dictionaries with column names as keys

    Example:
        results = execute_query_dict("SELECT * FROM Person WHERE PIN = %s", (12345,))
        for row in results:
            print(row['FirstName'], row['LastName'])
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        if not cursor.description:
            return []
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        return [dict(zip(columns, row)) for row in results] if results else []


def execute_scalar(query: str, params: tuple = ()) -> Any:
    """
    Execute a query and return a single value.

    Args:
        query: SQL query string
        params: Query parameters (use %s placeholders in query)

    Returns:
        Single value from the first row, first column

    Example:
        count = execute_scalar("SELECT COUNT(*) FROM Person")
        print(f"Total persons: {count}")
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        row = cursor.fetchone()
        return row[0] if row else None


def execute_non_query(query: str, params: tuple = ()) -> int:
    """
    Execute an INSERT, UPDATE, or DELETE query.

    Args:
        query: SQL query string
        params: Query parameters (use %s placeholders in query)

    Returns:
        Number of rows affected

    Example:
        rows = execute_non_query(
            "UPDATE Person SET Email = %s WHERE PIN = %s",
            ("new.email@example.com", 12345)
        )
        print(f"Updated {rows} rows")
    """
    with get_db_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.rowcount


def test_connection() -> dict[str, Any]:
    """
    Test the database connection and return server information.

    Returns:
        Dictionary with connection status and server info
    """
    try:
        with get_db_cursor() as cursor:
            cursor.execute(
                "SELECT @@VERSION as Version, DB_NAME() as DbName, SYSTEM_USER as UserName"
            )
            row = cursor.fetchone()
            if not row:
                raise Exception("No response from server.")

            return {
                "status": "connected",
                "database": row[1],
                "user": row[2],
                "version": row[0][:100] + "..." if len(row[0]) > 100 else row[0],
            }
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
        }
