"""
main.py
---------
Demonstrates the B+Tree implementation.

We show:
1. Inserting enough keys to trigger leaf and internal splits
2. Searching for existing and missing keys
3. Iterating through the tree in sorted order
4. Deleting keys with rebalancing
"""

from data_access import BPlusTree, BPlusTreeLeafPage


def showcase_bplustree():
    print("=== B+ Tree Index Demo ===")


    order = 3
    print(f"B+ Tree of Order: {order}")
    print(f"B+ Tree Max Keys: {order -1}")
    print(f"B+ Tree Min Keys: {int(order -1)/2}")


    # Small sizes force splits quickly
    tree = BPlusTree(order)

    # -------------------------------------------------
    # INSERTIONS
    # -------------------------------------------------
    values_to_insert = [10, 20, 5, 6, 12, 30, 7, 17, 3, 25, 15]
    print("\n>>> Inserting keys (triggers splits):")
    for val in values_to_insert:
        tree.insert(val, f"VALUE: {val}")
        print(f"Inserted {val} -> val{val}")
        tree.print_tree()

    print("\n>>> Tree structure after insertions:")
    tree.print_tree()


    # -------------------------------------------------
    # SEARCH
    # -------------------------------------------------
    print("\n>>> Search examples:")
    for key in [6, 15, 100]:
        result = tree.search(key)
        print(f"Search KEY {key}: {result}")


    # -------------------------------------------------
    # DELETIONS
    # -------------------------------------------------
    values_to_delete = [30, 10, 12, 25, 17, 20, 17, 15]
    print("\n>>> Deleting keys with rebalancing:")
    tree.print_tree() 

    for val in values_to_delete:
        print(f"Deleting {val}... ")
        deleted = tree.delete(val)
        print(f"Deleted? {deleted}")
        tree.print_tree() 

    # -------------------------------------------------
    # FINAL TREE CHECK
    # -------------------------------------------------
    print("\n>>> Root type after deletions:", type(tree.root).__name__)
    if isinstance(tree.root, BPlusTreeLeafPage):
        print(f"Root is leaf with keys: {tree.root.keys}")
    else:
        print(f"Root keys: {tree.root.keys}")

    print("\n=== Finished ===")


if __name__ == "__main__":
    showcase_bplustree()
