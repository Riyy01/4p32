[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/PxQysW19)
# Practical Assignment 01: Database Catalog 


The goal is to implement a naive database catalog in Python that:
- Stores table schemas (column names + types)
- Stores tables (relations) and their rows
- Allows row insertion and retrieval
- Enforces schema validation

This exercise introduces core database concepts:
- Data Catalog
- Relation Schemas
- Relation Instances
- Type validation
- In-memory data modeling


## Files

| File              | Purpose                                           |
|-------------------|---------------------------------------------------|
| `catalog.py`      | Your main implementation. Several `TODO`s to fill |
| `test_db_catalog.py` | Pytest tests to validate your code             |
| `main.py`        | Call the functions of the catalog                 |
| `README.md`       | This file                                         |



## Learning Objectives

- Practice class-based design in Python.
- Learn how DBMSs keep track of schemas and tables.
- Use `pytest` to validate correctness.
- Work with Python types (`int`, `str`, `float`, etc.).


## Instructions

1. Open `catalog.py`.
2. Look for `# TODO:` comments. Fill in the missing code.
3. Do NOT change function signatures.
4. Run the tests to check your work.


## Running Tests

You need `pytest` installed.

```bash
pip install pytest
pytest
```

All tests in test_db_catalog.py should pass when your implementation is correct.

## Tips

- You can inspect class docstrings to understand the role of each component.

- Think carefully about how to validate row length and type safety.

- Don’t forget to raise ValueError when validation fails.

## Deliverables

- A working db_catalog.py file with all TODOs implemented.
- All tests in test_catalog.py pass.

