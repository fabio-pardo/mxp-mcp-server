#!/usr/bin/env python3
"""
Test MXP Database Connection Script

This script tests the database connection and displays helpful debugging information.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.shared.db_client import (
    test_connection,
    execute_query_dict,
)


def main():
    """Run database connection tests."""
    print("=" * 70)
    print("MXP Database Connection Test")
    print("=" * 70)
    print()

    # Test 1: Basic Connection
    print("TEST 1: Testing database connection...")
    print("-" * 70)
    connection_info = test_connection()

    if connection_info["status"] == "connected":
        print("✅ CONNECTION SUCCESSFUL!")
        print(f"\n   Database: {connection_info['database']}")
        print(f"   User: {connection_info['user']}")
        print(f"   SQL Server Version: {connection_info['version']}")
        print()
    else:
        print("❌ CONNECTION FAILED!")
        print(f"\n   Error: {connection_info['error']}")
        print("\n   Troubleshooting tips:")
        print("   1. Verify credentials in .env file")
        print("   2. Check if VPN is connected")
        print("   3. Confirm network access to database server")
        print("   4. Verify SQL Server login exists and is not locked")
        return 1

    print()
    print("=" * 70)

    # Test 2: List available tables
    print("\nTEST 2: Listing available tables...")
    print("-" * 70)
    try:
        tables = execute_query_dict(
            """
            SELECT TOP 10 
                TABLE_SCHEMA, 
                TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
            """
        )
        print(f"✅ Found {len(tables)} tables:")
        for i, table in enumerate(tables, 1):
            print(f"   {i}. {table['TABLE_SCHEMA']}.{table['TABLE_NAME']}")

    except Exception as e:
        print(f"❌ Error listing tables: {e}")
        return 1

    print()
    print("=" * 70)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 70)
    print()
    print("You can now use the db_client module to query the MXP database.")
    print()
    print("Example usage:")
    print("  from src.shared.db_client import execute_query_dict, execute_scalar")
    print("  tables = execute_query_dict('SELECT * FROM INFORMATION_SCHEMA.TABLES')")
    print("  count = execute_scalar('SELECT COUNT(*) FROM dbo.Person_Amenities')")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
