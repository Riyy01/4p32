[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/tx4WLITP)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21345484&assignment_repo_type=AssignmentRepo)
# Practical Assignment 04: Implementing a Simple Database Index

## Overview
In this assignment, you will implement a database index B+ tree in Python.  A B+ Tree is a balanced tree data structure commonly used in databases and file systems for efficient search, insertion, and deletion.

Indexes are a crucial part of databases: they allow us to quickly locate records without scanning the entire table.  

You will:
1. Understand the role of indexes in query processing.
2. Implement a simple single-attribute index (similar to a B-Tree or Hash index, but simplified).
3. Test your index on a toy dataset.
4. Compare query performance with and without the index.


Your task is to fill in the missing parts of the implementation (marked with `#TODO`) and make sure the tree behaves correctly under:
- Search operations
- Insertions (with node splits when needed)
- Deletions (with rebalancing by borrowing/merging)

The tree should remain balanced and all data should live in the leaves.


## Files Provided
- `b_tree.py` → Contains the `BPlusTree` class with incomplete functions (`#TODO` markers).
- `b_tree_page.py` → Defines page structures:
  - `BPlusTreePage` (base class)
  - `BPlusTreeInternalPage`
  - `BPlusTreeLeafPage`
- `tests/` → Includes pytest test cases to verify correctness.

## Getting Started
1. Clone or download the project repository.
2. Install dependencies (only `pytest` is required):
   ```bash
   pip install pytest
   ```

3. Run the tests:

   ```bash
   pytest -v
   ```

   Initially, many tests will fail because the `#TODO` sections are incomplete.

## Tasks

You need to complete the following methods inside `BPlusTree`:

### Search

* `search(self, key)`

  * Traverse down through internal nodes to find the correct leaf.
  * Look for the `key` inside the leaf’s `keys`.
  * Return its value if found, otherwise return `None`.


### Insert

* `_insert_recursive(self, node, key, value)`

  * Base case: if `node` is a leaf, insert `(key, value)` in sorted order.
  * If overfull → call `_split_leaf()`.
  * Recursive case: if `node` is internal, navigate to the correct child using `_find_child_index()`.
  * If child splits → promote a key to this internal node.
  * If internal node becomes overfull → call `_split_internal()`.

* `_split_leaf(self, leaf)`

  * Split the leaf into two nodes.
  * Keep left half in original, move right half to a new leaf.
  * Update linked list pointers (`prev`, `next`).
  * Return `(promoted_key, new_leaf)`.

* `_split_internal(self, internal)`

  * Split internal node around the middle key.
  * Left half stays in original, right half moves to new internal.
  * Promote the middle key (do not keep it in either node).
  * Update parent pointers.

### Delete

* `_delete_from_leaf(self, leaf, key)`

  * Remove key/value from the leaf.
  * If underflow occurs:

    * Try borrowing from left or right sibling.
    * If borrowing is not possible → merge with sibling.
  * Update parent keys if necessary.

* `_delete_from_internal(self, node, key)`

  * Find the child where the key should be.
  * Recursively delete from that child.
  * If the child underflows → rebalance or merge.
  * Update parent keys if needed.


## Tips

* Always maintain sorted order of keys in nodes.
* Remember: internal nodes don’t store values, only navigation keys.
* Use `self.print_tree()` and `self.print_leaves()` to debug your implementation.