import pytest
from catalogy import Catalog
from ra_interpreter import RelationalAlgebraInterpreter


# ---------------------------
# Fixtures
# ---------------------------

@pytest.fixture
def catalog():
    return Catalog()

@pytest.fixture
def table1(catalog):
    schema_id = catalog.createSchema(['id', 'name', 'age'], [int, str, int])
    table_id = catalog.createTable(schema_id)
    table = catalog.getTableByID(table_id)
    table.insertRows([
        [1, 'Alice', 30],
        [2, 'Bob', 25],
        [3, 'Charlie', 35],
        [4, 'Alice', 28],
    ])
    return table_id

@pytest.fixture
def table2(catalog):
    schema_id = catalog.createSchema(['id', 'name', 'salary'], [int, str, float])
    table_id = catalog.createTable(schema_id)
    table = catalog.getTableByID(table_id)
    table.insertRows([
        [1, 'Alice', 50000.0],
        [2, 'Bob', 60000.0],
        [5, 'Eve', 70000.0],
    ])
    return table_id

@pytest.fixture
def table3(catalog):
    schema_id = catalog.createSchema(['id', 'name', 'age'], [int, str, int])
    table_id = catalog.createTable(schema_id)
    table = catalog.getTableByID(table_id)
    table.insertRows([
        [1, 'Alice', 28],
        [2, 'Bob', 35],
    ])
    return table_id

@pytest.fixture
def table4(catalog):
    schema_id = catalog.createSchema(['id', 'name', 'age'], [int, str, int])
    table_id = catalog.createTable(schema_id)
    table = catalog.getTableByID(table_id)
    table.insertRows([
        [3, "Charlie", 30],
        [4, "Dana", 40],
    ])
    return table_id

@pytest.fixture
def table5(catalog):
    schema_id = catalog.createSchema(["dept_id", "dept_name"], [int, str])
    table_id = catalog.createTable(schema_id)
    table = catalog.getTableByID(table_id)
    table.insertRows([
        [1, "HR"],
        [2, "IT"],
    ])
    return table_id

@pytest.fixture
def table6(catalog):
    schema_id = catalog.createSchema(["emp_id", "name", "dept_id"], [int, str, int])
    table_id = catalog.createTable(schema_id)
    table = catalog.getTableByID(table_id)
    table.insertRows([
       [10, "Alice", 1],
       [11, "Bob", 2]
    ])
    return table_id

@pytest.fixture
def table7(catalog):
    schema_id = catalog.createSchema(["id", "name", "group"], [int, str, int])
    table_id = catalog.createTable(schema_id)
    table = catalog.getTableByID(table_id)
    data = [[i, f"Name{i}", i % 50] for i in range(5000)]
    table.insertRows(data)
    return table_id

@pytest.fixture
def table8(catalog):
    schema_id = catalog.createSchema(["id", "value"], [int, str])
    table_id = catalog.createTable(schema_id)
    # leave empty table
    return table_id

@pytest.fixture
def table9(catalog):
    schema_id = catalog.createSchema(["id", "value"], [int, str])
    table_id = catalog.createTable(schema_id)
    table = catalog.getTableByID(table_id)
    table.insertRows([[1, "a"]])
    return table_id

@pytest.fixture
def table10(catalog):
    schema_id = catalog.createSchema(["id", "desc"], [int, str])
    table_id = catalog.createTable(schema_id)
    table = catalog.getTableByID(table_id)
    table.insertRows([[2, "b"]])
    return table_id

@pytest.fixture
def table11(catalog):
    schema_id = catalog.createSchema(["id", "name"], [int, str])
    table_id = catalog.createTable(schema_id)
    table = catalog.getTableByID(table_id)
    table.insertRows([[1, "Alice"]])
    return table_id

@pytest.fixture
def table12(catalog):
    schema_id = catalog.createSchema(["id", "name"], [int, str])
    table_id = catalog.createTable(schema_id)
    return table_id


# ---------------------------
# Selection Tests
# ---------------------------

def test_selection_literal(catalog, table1):
    new_id = RelationalAlgebraInterpreter.selection(catalog, table1, 'name', 'Alice', '==')
    rows = catalog.getTableByID(new_id).getRows()
    expected = [[1, 'Alice', 30], [4, 'Alice', 28]]
    assert sorted(rows) == sorted(expected)

def test_selection_column_to_column(catalog, table1):
    new_id = RelationalAlgebraInterpreter.selection(catalog, table1, 'id', 'age', '<')
    rows = catalog.getTableByID(new_id).getRows()
    assert sorted(rows) == sorted(catalog.getTableByID(table1).getRows())

def test_selection_invalid_column(catalog, table1):
    with pytest.raises(ValueError):
        RelationalAlgebraInterpreter.selection(catalog, table1, 'nonexistent', 'Alice', '==')


# ---------------------------
# Projection Tests
# ---------------------------

def test_projection_subset(catalog, table1):
    new_id = RelationalAlgebraInterpreter.projection(catalog, table1, ['name', 'age'])
    rows = catalog.getTableByID(new_id).getRows()
    expected = [['Alice', 30], ['Bob', 25], ['Charlie', 35], ['Alice', 28]]
    assert rows == expected

def test_projection_invalid_column(catalog, table1):
    with pytest.raises(ValueError):
        RelationalAlgebraInterpreter.projection(catalog, table1, ['nonexistent'])


# ---------------------------
# Rename Tests
# ---------------------------

def test_rename_multiple_columns(catalog, table1):
    rename_map = {'name': 'full_name', 'age': 'years'}
    new_id = RelationalAlgebraInterpreter.rename(catalog, table1, rename_map)
    table = catalog.getTableByID(new_id)
    assert table.getSchema().getColumns() == ['id', 'full_name', 'years']
    assert table.getRows()[0] == [1, 'Alice', 30]


# ---------------------------
# Cross Product Tests
# ---------------------------

def test_crossproduct_schema_and_size(catalog, table1, table2):
    new_id = RelationalAlgebraInterpreter.crossproduct(catalog, table1, table2)
    table = catalog.getTableByID(new_id)
    schema = table.getSchema().getColumns()
    assert 'id_2' in schema
    assert 'name_2' in schema
    assert len(table.getRows()) == 4 * 3


# ---------------------------
# Set Operation Tests
# ---------------------------

def test_union_basic(catalog, table1):
    schema_id = catalog.getTableByID(table1).getSchema().getSchemaID()
    t2_id = catalog.createTable(schema_id)
    t2 = catalog.getTableByID(t2_id)
    t2.insertRows([[3, 'Charlie', 35], [5, 'Eve', 40]])
    new_id = RelationalAlgebraInterpreter.union(catalog, table1, t2_id)
    rows = catalog.getTableByID(new_id).getRows()
    expected = [
        [1, 'Alice', 30],
        [2, 'Bob', 25],
        [3, 'Charlie', 35],
        [4, 'Alice', 28],
        [5, 'Eve', 40]
    ]
    assert sorted(rows) == sorted(expected)

def test_intersection_basic(catalog, table1):
    schema_id = catalog.getTableByID(table1).getSchema().getSchemaID()
    t2_id = catalog.createTable(schema_id)
    t2 = catalog.getTableByID(t2_id)
    t2.insertRows([[3, 'Charlie', 35], [4, 'Alice', 28]])
    new_id = RelationalAlgebraInterpreter.intersection(catalog, table1, t2_id)
    rows = catalog.getTableByID(new_id).getRows()
    expected = [[3, 'Charlie', 35], [4, 'Alice', 28]]
    assert sorted(rows) == sorted(expected)

def test_difference_basic(catalog, table1):
    schema_id = catalog.getTableByID(table1).getSchema().getSchemaID()
    t2_id = catalog.createTable(schema_id)
    t2 = catalog.getTableByID(t2_id)
    t2.insertRows([[1, 'Alice', 30], [3, 'Charlie', 35]])
    new_id = RelationalAlgebraInterpreter.difference(catalog, table1, t2_id)
    rows = catalog.getTableByID(new_id).getRows()
    expected = [[2, 'Bob', 25], [4, 'Alice', 28]]
    assert sorted(rows) == sorted(expected)

def test_union_schema_mismatch(catalog, table1, table2):
    with pytest.raises(ValueError):
        RelationalAlgebraInterpreter.union(catalog, table1, table2)

def test_intersection_schema_mismatch(catalog, table1, table2):
    with pytest.raises(ValueError):
        RelationalAlgebraInterpreter.intersection(catalog, table1, table2)

def test_difference_schema_mismatch(catalog, table1, table2):
    with pytest.raises(ValueError):
        RelationalAlgebraInterpreter.difference(catalog, table1, table2)


# ---------------------------
# Integration & Edge Cases
# ---------------------------

def test_chained_operations(catalog, table3, table4):
    sel1_id = RelationalAlgebraInterpreter.selection(catalog, table3, "age", 30, ">")
    sel2_id = RelationalAlgebraInterpreter.selection(catalog, table4, "age", 30, ">")
    proj1_id = RelationalAlgebraInterpreter.projection(catalog, sel1_id, ["name"])
    proj2_id = RelationalAlgebraInterpreter.projection(catalog, sel2_id, ["name"])
    union_id = RelationalAlgebraInterpreter.union(catalog, proj1_id, proj2_id)
    rows = catalog.getTableByID(union_id).getRows()
    assert sorted(rows) == [["Bob"], ["Dana"]]


def test_join_via_crossproduct_and_selection(catalog, table5, table6):
    cp_id = RelationalAlgebraInterpreter.crossproduct(catalog, table5, table6)
    joined_id = RelationalAlgebraInterpreter.selection(catalog, cp_id, "dept_id", "dept_id_2", "==")
    result_id = RelationalAlgebraInterpreter.projection(catalog, joined_id, ["name", "dept_name"])
    rows = catalog.getTableByID(result_id).getRows()
    assert sorted(rows) == [["Alice", "HR"], ["Bob", "IT"]]


def test_large_dataset(catalog, table7):
    sel_id = RelationalAlgebraInterpreter.selection(catalog, table7, "group", 25, "==")
    rows = catalog.getTableByID(sel_id).getRows()
    assert all(row[2] == 25 for row in rows)
    assert len(rows) == 5000 // 50


def test_empty_table_selection_and_projection(catalog, table8):
    sel_id = RelationalAlgebraInterpreter.selection(catalog, table8, "id", 1, "==")
    proj_id = RelationalAlgebraInterpreter.projection(catalog, table8, ["value"])
    assert catalog.getTableByID(sel_id).getRows() == []
    assert catalog.getTableByID(proj_id).getRows() == []


def test_crossproduct_schema_conflict(catalog, table9, table10):
    cp_id = RelationalAlgebraInterpreter.crossproduct(catalog, table9, table10)
    cp_table = catalog.getTableByID(cp_id)
    schema = cp_table.getSchema().getColumns()
    assert "id" in schema
    assert "id_2" in schema


def test_projection_nonexistent_column(catalog, table11):
    with pytest.raises(ValueError):
        RelationalAlgebraInterpreter.projection(catalog, table11, ["nonexistent"])


def test_insert_invalid_row_length(catalog, table12):
    table = catalog.getTableByID(table12)
    with pytest.raises(ValueError):
        table.insertRows([[1]])  # missing column
