from typing import List, Any
from catalogy import Catalog


class RelationalAlgebraInterpreter:
    """
    Naive Relational Algebra Interpreter.

    Implements the following operators:
      - selection (σ)
      - projection (π)
      - rename (ρ)
      - cross product (×)
      - union (∪)
      - intersection (∩)
      - difference (−)

    Each operator takes input tables from the Catalog and produces
    a new table (with a new ID).
    """

    # --------------------
    # Selection (σ)
    # --------------------
    @staticmethod
    def selection(catalog: Catalog, table_id: int, col_name: str, value: Any, op: str) -> int:
        """
        Selection (σ): Filter rows of a table based on a condition.
        Example: σ_{age > 25}(Students)

        Parameters:
            catalog : Catalog manager
            table_id : ID of the table we apply selection on
            col_name : The column to check
            value : Value or column to compare with
            op : Operator (==, !=, <, <=, >, >=)

        Returns:
            new_table_id : ID of the resulting table
        """
        ops = {
            '==': lambda x, y: x == y,
            '!=': lambda x, y: x != y,
            '<': lambda x, y: x < y,
            '<=': lambda x, y: x <= y,
            '>': lambda x, y: x > y,
            '>=': lambda x, y: x >= y
        }

        # TODO:
        # 1. Get table and schema
        table = catalog.getTableByID(table_id)
        schema = catalog.getSchemaByID(table.schema_id)

        # 2. Find column index and type

        col_idx = schema.getColumnIdx(col_name)
        
        # 3. Apply the operator to filter rows
        filter_rows = []
        oparator = ops[op]
        if isinstance(value, str) and value in schema.getColumns():
            val_idx = schema.getColumnIdx(value)
            for row in table.getRows():
                if oparator(row[col_idx], row[val_idx]):
                    filter_rows.append(row)
        else:
            for row in table.getRows():
                if oparator(row[col_idx], value):
                    filter_rows.append(row)

        # 4. Create new table with results
        newtable_id = catalog.createTable(schema.getSchemaID())
        newtable = catalog.getTableByID(newtable_id)
        newtable.insertRows(filter_rows)
        return newtable_id

    # --------------------
    # Projection (π)
    # --------------------
    @staticmethod
    def projection(catalog: Catalog, table_id: int, col_names: List[str]) -> int:
        """
        Projection (π): Select specific columns from a table.
        Example: π_{name, age}(Students)

        Removes other columns and may reduce duplicates.
        """
        # TODO:
        table = catalog.getTableByID(table_id)
        schema = catalog.getSchemaByID(table.schema_id)

        # 1. Find column indices
        col_indices = []
        col_types = []
        for c in col_names:
            idx = schema.getColumnIdx(c)
            type = schema.getColumnType(c)
            col_indices.append(idx)
            col_types.append(type)

        # 2. Build new rows with only those columns
        new_rows = []
        for row in table.getRows():
            new_row = []
            for i in col_indices:
                new_row.append(row[i])
            new_rows.append(new_row)

        # 3. Create new schema + table
        new_schema = catalog.createSchema(col_names, col_types)
        newtable_id = catalog.createTable(new_schema)
        newtable = catalog.getTableByID(newtable_id)
        newtable.insertRows(new_rows)
        return newtable_id

    # --------------------
    # Rename (ρ)
    # --------------------
    @staticmethod
    def rename(catalog: Catalog, table_id: int, rename_map: dict) -> int:
        """
        Rename (ρ): Change column names of a relation.
        Example: ρ_{newName/oldName}(Students)

        Useful when joining/crossing tables with duplicate column names.
        """
        # TODO:
        table = catalog.getTableByID(table_id)
        schema = catalog.getSchemaByID(table.schema_id)
        col_type = schema.getColumnTypes()

        # 1. Map old column names to new ones
        new_col = []
        for c in schema.getColumns():
            if c in rename_map:
                new_col.append(rename_map[c])
            else:
                new_col.append(c)

        # 2. Create new schema + table
        new_schema = catalog.createSchema(new_col, col_type)
        newtable_id = catalog.createTable(new_schema)
        newtable = catalog.getTableByID(newtable_id)
        newtable.insertRows(table.getRows())
        return newtable_id

    # --------------------
    # Cross Product (×)
    # --------------------
    @staticmethod
    def crossproduct(catalog: Catalog, table_id1: int, table_id2: int) -> int:
        """
        Cross Product (×): Combine every row of table1 with every row of table2.
        Example: Students × Courses

        Produces a "cartesian product" of rows.
        """

        # 1. Handle duplicate column names (hint: use rename)
        table1 = catalog.getTableByID(table_id1)
        table2 = catalog.getTableByID(table_id2)
        schema1 = catalog.getSchemaByID(table1.schema_id)
        schema2 = catalog.getSchemaByID(table2.schema_id)

        rename_map = {}
        for c in schema2.getColumns():
            if c in schema1.getColumns():
                rename_map[c] = f"{c}_2"
        if rename_map:  
            table_id2 = RelationalAlgebraInterpreter.rename(catalog, table_id2, rename_map)
            table2 = catalog.getTableByID(table_id2)
            schema2 = catalog.getSchemaByID(table2.schema_id)

        # 2. Compute cartesian product
        rows = []
        for r1 in table1.getRows():
            for r2 in table2.getRows():
                rows.append(r1 + r2)

        # 3. Create new schema + table
        new_schema = catalog.createSchema(
            schema1.getColumns() + schema2.getColumns(),
            schema1.getColumnTypes() + schema2.getColumnTypes()
        )
        newtable_id = catalog.createTable(new_schema)
        catalog.getTableByID(newtable_id).insertRows(rows)
        return newtable_id

    # --------------------
    # Helper: Schema Check
    # --------------------
    @staticmethod
    def _check_schema_compatibility(table1, table2):
        """Ensure schemas are identical before set operations."""
        if table1.getSchema().getColumns() != table2.getSchema().getColumns():
            raise ValueError("Schemas do not match for set operation.")

    # --------------------
    # Union (∪)
    # --------------------
    @staticmethod
    def union(catalog: Catalog, table_id1: int, table_id2: int) -> int:
        """
        Union (∪): Keep all distinct rows from both tables.
        Example: Students_CA ∪ Students_US
        """
        # TODO:
        # 1. Check schema compatibility
        table1 = catalog.getTableByID(table_id1)
        table2 = catalog.getTableByID(table_id2)
        RelationalAlgebraInterpreter._check_schema_compatibility(table1, table2)

        # 2. Compute union using Python sets
        rows = set()
        for r in table1.getRows():
            rows.add(tuple(r))
        for r in table2.getRows():
            rows.add(tuple(r))
            
        # 3. Insert results into new table
        newtable_id = catalog.createTable(table1.schema_id)
        newtable = catalog.getTableByID(newtable_id)
        changed_rows = []
        for r in rows:
            changed_rows.append(list(r))
        newtable.insertRows(changed_rows)
        return newtable_id
    # --------------------
    # Intersection (∩)
    # --------------------

    @staticmethod
    def intersection(catalog: Catalog, table_id1: int, table_id2: int) -> int:
        """
        Intersection (∩): Keep only rows that appear in both tables.
        Example: Students_CA ∩ Students_US
        """
        # TODO:
        # 1. Check schema compatibility
        table1 = catalog.getTableByID(table_id1)
        table2 = catalog.getTableByID(table_id2)
        RelationalAlgebraInterpreter._check_schema_compatibility(table1, table2)

        # 2. Compute intersection
        row1 = set()
        for r in table1.getRows():
            row1.add(tuple(r))

        row2 = set()
        for r in table2.getRows():
            row2.add(tuple(r))

        rows = row1.intersection(row2)

        # 3. Insert results into new table
        newtable_id = catalog.createTable(table1.schema_id)
        newtable = catalog.getTableByID(newtable_id)
        changed_rows = []
        for r in rows:
            changed_rows.append(list(r))
        newtable.insertRows(changed_rows)
        return newtable_id

    # --------------------
    # Difference (−)
    # --------------------

    @staticmethod
    def difference(catalog: Catalog, table_id1: int, table_id2: int) -> int:
        """
        Difference (−): Keep rows in table1 that are not in table2.
        Example: Students_CA − Students_US
        """
        # TODO:
        # 1. Check schema compatibility
        table1 = catalog.getTableByID(table_id1)
        table2 = catalog.getTableByID(table_id2)
        RelationalAlgebraInterpreter._check_schema_compatibility(table1, table2)

        # 2. Compute difference
        row1 = set()
        for r in table1.getRows():
            row1.add(tuple(r))

        row2 = set()
        for r in table2.getRows():
            row2.add(tuple(r))

        rows = row1.difference(row2)

        # 3. Insert results into new table
        newtable_id = catalog.createTable(table1.schema_id)
        newtable = catalog.getTableByID(newtable_id)
        changed_rows = []
        for r in rows:
            changed_rows.append(list(r))
        newtable.insertRows(changed_rows)
        return newtable_id