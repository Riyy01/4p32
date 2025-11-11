import os
import csv

from catalogy import Catalog
from ra_interpreter import RelationalAlgebraInterpreter
from typing import List


# -------------------------
# Load CSV into Relation
# -------------------------
def infer_column_types(rows: List[List[str]]) -> List[type]:
    """
    Infer Python types for each column based on sample data.
    Tries int, then float, then defaults to str.
    """
    if not rows:
        return []

    num_cols = len(rows[0])
    col_types = []

    for col_idx in range(num_cols):
        col_type = int  # start with int
        for row in rows:
            val = row[col_idx].strip()
            if val == "":
                continue  # skip empty cells
            try:
                int(val)
            except ValueError:
                try:
                    float(val)
                    col_type = float
                except ValueError:
                    col_type = str
                    break
        col_types.append(col_type)

    return col_types

def load_csv_to_relation(filename: str, catalog: Catalog, delimiter="\t") -> int:
    """
    Load a CSV file into a Relation and store in Catalog.
    Each row becomes a dict {column: value}.
    """
    with open(filename, "r", encoding="utf-8") as f:
        # Read all lines
        lines = f.readlines()
    
    # Split header manually
    header_line = lines[0].strip()
    header = [col.strip() for col in header_line.split(delimiter)]

    # Read rows using csv.reader
    reader = csv.reader(lines[1:], delimiter=delimiter)
    rows = [list(row) for row in reader]

    # Infer column types
    column_types = infer_column_types(rows)

    # Create schema with column types
    schema_id = catalog.createSchema(header, column_types)
    table_id = catalog.createTable(schema_id, filename)
    
    # Insert rows efficiently
    relation = catalog.getTableByID(table_id)
    if hasattr(relation, "insertRows"):
        relation.insertRows(rows)

    return table_id


current_path = os.getcwd()  
base_path = os.path.join(current_path, "data")
base_path = os.path.join(base_path, "IMDb_sample")

catalog = Catalog()

actors_id = load_csv_to_relation(os.path.join(base_path, "actors.csv"), catalog)
movies_id = load_csv_to_relation(os.path.join(base_path, "movies.csv"), catalog)
roles_id = load_csv_to_relation(os.path.join(base_path, "roles.csv"), catalog)


actors = catalog.getTableByID(actors_id)
# Access rows via catalog
print("Columns: ", actors.getSchema().getColumns())   # ['id', 'first_name', 'last_name', 'gender']
print("Data: ", actors.getRows()[:5]) # first 5 rows

ra = RelationalAlgebraInterpreter()

interpreter = RelationalAlgebraInterpreter()

print("\n Find all female actors:")
# SQL: SELECT * FROM actors WHERE gender = 'F';
female_actors_id = interpreter.selection(catalog, actors_id, "gender", "F", "==")
female_actors = catalog.getTableByID(female_actors_id)
print("\n".join(str(row) for row in female_actors.getRows()))


print("\nFind all actors whose id >= 800000")
# SQL: SELECT * FROM actors WHERE id >= 800000;
id_filter_id = interpreter.selection(catalog, actors_id, "id", 800000, ">=")
id_filter = catalog.getTableByID(id_filter_id)
print("\n".join(str(row) for row in id_filter.getRows()))


print("\nFind all actors whose id < 10000:")
# SQL: SELECT * FROM actors WHERE id < 10000;
id_filter_id = interpreter.selection(catalog, actors_id, "id", 10000, "<")
id_filter = catalog.getTableByID(id_filter_id)
print("\n".join(str(row) for row in id_filter.getRows()))


print("\nFind the last names of all actors named Chris")
# SQL: SELECT last_name FROM actors WHERE first_name = 'Chris';
chris_id = interpreter.selection(catalog, actors_id, "first_name", "Chris", "==")
chris_lastnames_id = interpreter.projection(catalog, chris_id,["last_name"])
chris_lastnames = catalog.getTableByID(chris_lastnames_id)
print("\n".join(str(row) for row in chris_lastnames.getRows()))


print("\nFind the name of movies released after 1998")
# SQL: SELECT name FROM movies WHERE year > 1998;
movies_after_1998_id = interpreter.selection(catalog, movies_id, "year", 1998, ">")
movies_title_id = interpreter.projection(catalog, movies_after_1998_id, ["name"])
movies_title = catalog.getTableByID(movies_title_id)
print("\n".join(str(row) for row in movies_title.getRows()))


print("Create a table with all actors (and extra actors) ")
# Union: Add extra actors
# SQL:
#   SELECT id, first_name, last_name, gender FROM actors
#   UNION
#   SELECT id, first_name, last_name, gender FROM extra_actors;

extra_actors_id = catalog.createTable(actors.getSchema().getSchemaID())
catalog.getTableByID(extra_actors_id).insertRows([
    ["109100", "Renata", "Dividino", "F"],
    ["481290", "Burnell", "Tucker", "M"],
    ["10963", "Chris", "Anastasio", "M"],
])

union_id = interpreter.union(catalog, actors_id, extra_actors_id)
print("\n".join(str(row) for row in catalog.getTableByID(union_id).getRows()[:10]))

print("Find the movies’ titles and roles each actor has been in.")
# SQL:
#   SELECT a.first_name, a.last_name, m.name AS movie_title, r.role
#   FROM actors a
#   JOIN roles r ON a.id = r.actor_id
#   JOIN movies m ON r.movie_id = m.id;

cp1 = interpreter.crossproduct(catalog, actors_id, roles_id)
# select rows where actors.id == roles.actor_id
join1 = interpreter.selection(catalog, cp1, "id", "actor_id", "==")
# join with movies
cp2 = interpreter.crossproduct(catalog, join1, movies_id)
#select rows where roles.movie_id == movies.id
join2 = interpreter.selection(catalog, cp2, "movie_id", "id_2", "==")
# projection: actor name, movie title, role
result_id = interpreter.projection(catalog, join2, ["first_name", "last_name", "name", "role"])
print("\n".join(str(row) for row in catalog.getTableByID(result_id).getRows()[:5]))
