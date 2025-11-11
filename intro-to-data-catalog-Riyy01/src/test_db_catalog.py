# test_catalog.py
import pytest
from catalog import Catalog

def test_create_schema_and_table():
    catalog = Catalog()
    schema_id = catalog.createSchema(["id", "name"], [int, str])
    table_id = catalog.createTable(schema_id)

    assert schema_id == 1
    assert table_id == 1

    schema = catalog.getSchemaByID(schema_id)
    assert schema.getColumns() == ["id", "name"]

    table = catalog.getTableByID(table_id)
    assert table.getSchema().getSchemaID() == schema_id

def test_insert_and_retrieve_rows():
    catalog = Catalog()
    schema_id = catalog.createSchema(["id", "name"], [int, str])
    table_id = catalog.createTable(schema_id)

    table = catalog.getTableByID(table_id)
    table.insertRow([1, "Alice"])
    table.insertRow([2, "Bob"])

    rows = table.getRows()
    assert rows == [[1, "Alice"], [2, "Bob"]]

def test_invalid_row_length_single():
    catalog = Catalog()
    schema_id = catalog.createSchema(["id", "name"], [int, str])
    table_id = catalog.createTable(schema_id)
    table = catalog.getTableByID(table_id)

    with pytest.raises(ValueError):
        table.insertRow([1])  # too short


def test_invalid_row_length_batch():
    catalog = Catalog()
    schema_id = catalog.createSchema(["id", "name", "age"], [int, str, int])
    table_id = catalog.createTable(schema_id)
    table = catalog.getTableByID(table_id)

    # Second row is short — should raise and not insert anything
    with pytest.raises(ValueError):
        table.insertRows([[1, "Alice", 28], [2, "Bob"]])

    assert table.getRows() == []

    # First row too long — should also raise
    with pytest.raises(ValueError):
        table.insertRows([[3, "Charlie", 22, "EXTRA"]])

    assert table.getRows() == []

    # Valid batch should work
    table.insertRows([[4, "Dana", 30], [5, "Evan", 27]])
    assert table.getRows() == [[4, "Dana", 30], [5, "Evan", 27]]
