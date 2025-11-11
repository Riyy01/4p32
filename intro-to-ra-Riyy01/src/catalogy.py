# catalog.py

from typing import List, Dict, Type, Any

class Catalog:
    """
    Catalog: Tracks metadata about schemas and tables.
    """

    def __init__(self):
        # Initialize schema and table counters and dictionaries
        self.table_id_count = 0
        self.tables_id2table: Dict[int, 'Relation'] = {}

        self.schema_id_count = 0
        self.schema_id2schema: Dict[int, 'Schema'] = {}

    def createSchema(self, header: List[str], column_types: List[Type]) -> int:
        """
        Create and register a new schema in the catalog.
        """
        schema_id = self.getNextSchemaID()
        schema = Schema(schema_id, header, column_types)
        self.schema_id2schema[schema_id] = schema
        return schema_id

    def createTable(self, schema_id: int, db_file: str = "in-memory") -> int:
        """
        Create a new Relation (table) and store it in the catalog.
        """
        table_id = self.getNextTableID()
        table = Relation(table_id, schema_id, db_file, self)
        self.tables_id2table[table_id] = table
        return table_id

    def getTableByID(self, table_id: int) -> 'Relation':
        """
        Return a Relation object given its ID.
        """
        return self.tables_id2table.get(table_id)

    def getSchemaByID(self, schema_id: int) -> 'Schema':
        """
        Return a Schema object given its ID.
        """
        return self.schema_id2schema.get(schema_id)

    def getNextTableID(self) -> int:
        """
        Generate and return the next unique table ID.
        """
        self.table_id_count += 1
        return self.table_id_count

    def getNextSchemaID(self) -> int:
        """
        Generate and return the next unique schema ID.
        """
        self.schema_id_count += 1
        return self.schema_id_count


class Schema:
    """
    Schema: Defines the structure of a relation (column names + types).
    """

    def __init__(self, schema_id: int, columns: List[str], column_types: List[Type]):
        if len(columns) != len(column_types):
            raise ValueError("Columns and column_types must have the same length.")
        self.schema_id = schema_id
        self.columns = columns
        self.column_types = column_types

    def getSchemaID(self) -> int:
        """Return schema ID."""
        return self.schema_id

    def getColumns(self) -> List[str]:
        """Return the list of column names."""
        return self.columns

    def getColumnTypes(self) -> List[Type]:
        """Return the list of column types."""
        return self.column_types

    def getColumnIdx(self, name: str) -> int:
        """Return the index of a column by name."""
        try:
            return self.columns.index(name)
        except ValueError:
            raise ValueError(f"Column '{name}' not found in schema ID={self.schema_id}.")

    def getColumnType(self, name: str) -> Type:
        """Return the Python type of the specified column."""
        idx = self.getColumnIdx(name)
        return self.column_types[idx]


class Relation:
    """
    Relation: Represents an actual dataset (rows + schema reference).
    """

    def __init__(self, table_id: int, schema_id: int, db_file: str, catalog: Catalog):
        self.table_id = table_id
        self.schema_id = schema_id
        self.db_file = db_file
        self.catalog = catalog
        self.rows: List[List[Any]] = []

    def getSchema(self) -> Schema:
        """Return schema of this relation (via Catalog)."""
        return self.catalog.getSchemaByID(self.schema_id)

    def getID(self) -> int:
        """Return table ID."""
        return self.table_id

    def insertRow(self, row: List[Any]):
        """Insert a single row into the relation."""
        schema = self.getSchema()
        if len(row) != len(schema.getColumns()):
            raise ValueError("Row does not match schema.")
        self.rows.append(row)

    def insertRows(self, rows: List[List[Any]]):
        """Insert multiple rows in batch (faster)."""
        if not rows:
            return
        schema = self.getSchema()
        expected = len(schema.getColumns())

        # Validate ALL rows first; do not partially insert on error
        for idx, row in enumerate(rows):
            if len(row) != expected:
                raise ValueError(
                    f"Row {idx} length {len(row)} does not match schema length {expected}."
                )

        # Only extend after validation succeeds for all rows
        self.rows.extend(rows)


    def getRows(self) -> List[List[Any]]:
        """Return all rows of the relation."""
        return self.rows
