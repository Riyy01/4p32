# main.py
"""
Main script to try out the naive DB Data Catalog.

Run this file to see how your implementation works.
"""

from catalog import Catalog

def main():
    # Create a new catalog instance
    catalog = Catalog()
    print("Catalog created")

    # Define a schema (columns + types)
    schema_id = catalog.createSchema(["id", "name", "age"], [int, str, int])
    schema = catalog.getSchemaByID(schema_id)
    print(f"Schema created with ID={schema_id}")
    print("Columns:", schema.getColumns())
    print("Types:", schema.getColumnTypes())

    # Create a table that uses this schema
    table_id = catalog.createTable(schema_id)
    table = catalog.getTableByID(table_id)
    print(f"Table created with ID={table_id}")

    # Insert a single row
    print("\n Inserting a single row...")
    table.insertRow([1, "Alice", 28])
    print("Current rows:", table.getRows())

    # Insert multiple rows
    print("\n Inserting multiple rows...")
    rows_to_insert = [
        [2, "Bob", 31],
        [3, "Charlie", 22]
    ]
    table.insertRows(rows_to_insert)
    print("Current rows:", table.getRows())

    # Try retrieving column type by name
    print("\n Column lookup:")
    print("Index of 'name':", schema.getColumnIdx("name"))
    print("Type of 'age':", schema.getColumnType("age"))

    # Uncomment to test an error (invalid row)
    print("\n Inserting invalid row (should raise error)...")
    #table.insertRow([4, "Invalid"])  # Missing 'age'

if __name__ == "__main__":
    main()
