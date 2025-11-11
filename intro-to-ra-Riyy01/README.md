[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/tWvsLU2v)
# Practical Assignment 02: Relational Algebra Interpreter 

## Overview
In this assignment, you will implement **basic relational algebra operators** in Python:

- Selection (σ)
- Projection (π)
- Rename (ρ)
- Cross Product (×)
- Union (∪)
- Intersection (∩)
- Difference (−)

We use a simple `Catalog` interface to simulate database tables and schemas.   The implementation is intentionally naive  to help you focus on relational algebra concepts.


## Learning Goals
- Understand the semantics of relational algebra operators.
- Learn how to manipulate tables using Python lists and sets.
- Gain practice writing modular code.
- Connect abstract DB theory with concrete Python implementations.


## Instructions
1. Open `ra_interpreter.py`.
2. For each operator, fill in the `TODO` parts:
   - Get data from the catalog
   - Perform the correct operation
   - Return a new table ID
3. Use the provided `pytest` tests to check your implementation:
   ```bash
   pytest
   ```


## Example
Projection (π) keeps only specified columns:

# Original Students table

| id   | name | age |
| -------- | ------- | ------- |
| 1  | Aline    |22|
| 2 | Bob     |25|
| 3    | Charlie    |25|


π_{name, age}(Students)

| name | age |
| ------- | ------- |
| Aline    |22|
| Bob     |25|
| Charlie    |25|


## Tips
Use Python sets for union, intersection, difference.

For crossproduct, use a nested loop (for r1 in rows1: for r2 in rows2:).

Always create a new schema and new table ID for results.

## Rules & Guidelines

- Do not modify the `Catalog`, `Schema`, or `Relation` classes.
- Do not modify the pytest suite.
- Focus on completing the sections marked as `TODO`.
- You may use Python standard libraries but do not use external libraries for RA operations.
