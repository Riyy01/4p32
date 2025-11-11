# catalog.py
from typing import List, Dict, Type, Any

class Catalog:
    """
    Catalog: Tracks metadata about schemas and tables.

    Purpose
    -------
    The Catalog is a simple metadata manager that:
      - assigns unique IDs to schemas and tables,
      - stores schemas (column names + types),
      - stores relations (tables with rows),
      - allows table and schema lookup by ID.
    """

    def __init__(self):
        # Unique counters for assigning IDs
        self.table_id_count = 0
        self.tables_id2table: Dict[int, 'Relation'] = {}

        self.schema_id_count = 0
        self.schema_id2schema: Dict[int, 'Schema'] = {}

    def createSchema(self, header: List[str], column_types: List[Type]) -> int:
        """
        Create and register a new schema in the catalog.

        Returns
        -------
        int: schema_id assigned to the new schema.
        """
        # TODO: Generate a new schema ID and create a Schema object.
        schema_id = self.getNextSchemaID()
        
        schema_obj = Schema(schema_id=schema_id,columns=header,column_types=column_types)
      
        # TODO: Store it in self.schema_id2schema.
        self.schema_id2schema[schema_id] = schema_obj
        
        # TODO: Return the new schema ID.
        return schema_id
      
        pass

    def createTable(self, schema_id: int, db_file: str = "in-memory") -> int:
        """
        Create a new Relation (table) and store it in the catalog.
        """
        
        # TODO: Generate a new table ID.
        table_id = self.getNextTableID()
        
        # TODO: Create a Relation object with the given schema_id and db_file.
        relation_obj = Relation(table_id=table_id,schema_id=schema_id,db_file=db_file,catalog=self)
        
        # TODO: Store it in self.tables_id2table.
        self.tables_id2table[table_id] = relation_obj
        
        # TODO: Return the new table ID.
        return table_id
        pass

    def getTableByID(self, table_id: int) -> 'Relation':
        """Return a Relation object given its ID."""
        return self.tables_id2table.get(table_id)

    def getSchemaByID(self, schema_id: int) -> 'Schema':
        """Return a Schema object given its ID."""
        return self.schema_id2schema.get(schema_id)

    def getNextTableID(self) -> int:
        """Generate and return the next unique table ID."""
        self.table_id_count += 1
        return self.table_id_count

    def getNextSchemaID(self) -> int:
        """Generate and return the next unique schema ID."""
        self.schema_id_count += 1
        return self.schema_id_count


class Schema:
    """
    Schema: Defines the structure of a relation.

    Purpose
    -------
    A Schema describes the structure of a table: 
      - column names
      - column types
    """

    def __init__(self, schema_id: int, columns: List[str], column_types: List[Type]):
        # TODO: Validate that columns and column_types have the same length.
        if len(columns) != len(column_types) : raise ValueError("do not hv same length")
        # TODO: Assign schema_id, columns, and column_types to instance variables.
        self.schema_id = schema_id
        self.columns = columns
        self.column_types = column_types
        pass

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

    Purpose
    -------
    A Relation is a container for:
      - rows (list of values, one per column)
      - a reference to a schema (via schema_id in Catalog)
      - an optional file reference (CSV path, etc.)
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
        """
        Insert a single row into the relation.
        Validate that the row matches the schema.
        """
        schema = self.getSchema()
        # TODO: Check that row length matches schema length.
        if len(row) != len(schema.columns) : raise ValueError("length doesnt match")
        # TODO: Append row to self.rows.
        self.rows.append(row)
        pass

    def insertRows(self, rows: List[List[Any]]):
        """
        Insert multiple rows in batch (faster).
        All rows must match schema length.
        """
        if not rows:
            return
        schema = self.getSchema()
        # TODO: Validate that ALL rows have the same number of values as schema columns.
        for row in rows:
         if len(row) != len(schema.columns): raise ValueError("dont have same number of value")
        # TODO: Extend self.rows with new rows.
        self.rows.extend(rows)
        pass
        
    def getRows(self) -> List[List[Any]]:
        """Return all rows of the relation."""
        return self.rows
