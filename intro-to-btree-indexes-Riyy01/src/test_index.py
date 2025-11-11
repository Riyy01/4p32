import pytest
from data_access import BPlusTree, BPlusTreeLeafPage, BPlusTreeInternalPage

# ---------------------------
# Fixtures
# ---------------------------

@pytest.fixture
def small_tree():
    """Return a B+Tree of order 2 for testing."""
    return BPlusTree(2)

@pytest.fixture
def mid_tree():
    """Return a B+Tree of order 3 for testing."""
    return BPlusTree(order=3)

@pytest.fixture
def big_tree():
    """Return a B+Tree of order 4 for testing."""
    return BPlusTree(4)


# ---------------------------
# Basic Insert & Search
# ---------------------------

def test_single_insert_and_search(small_tree):
    small_tree.insert(10, "A")
    assert small_tree.search(10) == "A"
    assert small_tree.search(20) is None

def test_multiple_inserts_and_search(small_tree):
    keys = [10, 20, 5]
    for k in keys:
        small_tree.insert(k, str(k))
    for k in keys:
        assert small_tree.search(k) == str(k)

def test_insert_and_structure(mid_tree):
    """Insert keys and check tree structure and leaf order."""
    values_to_insert = [10, 20, 5, 6, 12, 30, 7, 17, 3, 25, 15]

    for val in values_to_insert:
        mid_tree.insert(val, f"val{val}")

    # Traverse leaves to get keys in order
    result = []
    node = mid_tree.root
    while isinstance(node, BPlusTreeInternalPage):
        node = node.children[0]

    while node:
        result.extend(node.keys)
        node = node.next

    # Check that all inserted keys are present
    expected_keys = sorted(values_to_insert)
    assert result == expected_keys

    # Check root type after insertions
    assert isinstance(mid_tree.root, (BPlusTreeInternalPage, BPlusTreeLeafPage))
    if isinstance(mid_tree.root, BPlusTreeInternalPage):
        assert len(mid_tree.root.children) > 1


def test_search(mid_tree):
    """Test searching existing and missing keys."""
    keys = [10, 20, 5, 6, 12, 30, 7, 17, 3, 25, 15]
    for k in keys:
        mid_tree.insert(k, f"val{k}")

    # Existing keys
    for k in keys:
        assert mid_tree.search(k) == f"val{k}"

    # Missing key
    assert mid_tree.search(100) is None


# ---------------------------
# Leaf Split
# ---------------------------

def test_leaf_split(small_tree):
    for k in [0, 1, 2, 3, 4]:
        small_tree.insert(k, str(k))

    # Traverse leaf nodes to get all keys in order
    result = []
    # Start from the leftmost leaf
    node = small_tree.root
    while isinstance(node, BPlusTreeInternalPage):
        node = node.children[0]

    # Follow the linked list of leaves
    while node:
        result.extend(node.keys)
        node = node.next

    assert result == [0, 1, 2, 3, 4]

    # Root should now be an internal node
    assert isinstance(small_tree.root, BPlusTreeInternalPage)
    # Root should have 2 children
    assert len(small_tree.root.children) == 2


# ---------------------------
# Internal Split
# ---------------------------

def test_internal_split(big_tree):
    for i in range(1, 20):
        big_tree.insert(i, str(i))

    # Traverse leaf nodes to get all keys in order
    result = []
    # Start from the leftmost leaf
    node = big_tree.root
    while isinstance(node, BPlusTreeInternalPage):
        node = node.children[0]

    # Follow the linked list of leaves
    while node:
        result.extend(node.keys)
        node = node.next

    assert result == list(range(1, 20))

    # Root should be internal
    assert isinstance(big_tree.root, BPlusTreeInternalPage)
    # Root should have at least 2 children
    assert len(big_tree.root.children) >= 2


# ---------------------------
# Deletion
# ---------------------------

def test_simple_delete(small_tree):
    for i in [1, 2, 3]:
        small_tree.insert(i, str(i))
    small_tree.delete(2)

    # Traverse leaf nodes to get all keys in order
    result = []
    # Start from the leftmost leaf
    node = small_tree.root
    while isinstance(node, BPlusTreeInternalPage):
        node = node.children[0]

    # Follow the linked list of leaves
    while node:
        result.extend(node.keys)
        node = node.next

    assert result == [1, 3]
    assert small_tree.search(2) is None

def test_delete_leaf_merge(small_tree):
    for i in [1, 2, 3, 4]:
        small_tree.insert(i, str(i))

    small_tree.delete(3)
    small_tree.delete(4)

    # Traverse leaf nodes to get all keys in order
    result = []
    # Start from the leftmost leaf
    node = small_tree.root
    while isinstance(node, BPlusTreeInternalPage):
        node = node.children[0]

    # Follow the linked list of leaves
    while node:
        result.extend(node.keys)
        node = node.next

    assert result == [1, 2]

def test_mass_insertion_and_deletion(big_tree):
    nums = list(range(1, 30))
    for n in nums:
        big_tree.insert(n, str(n))

    # Delete every 3rd key: 3, 6, 9, ...
    for n in nums[2::3]:  # indices 2, 5, 8,... correspond to values 3, 6, 9,...
        big_tree.delete(n)

    # Traverse leaf nodes to get all keys in order
    result = []
    node = big_tree.root
    while hasattr(node, "children") and node.children:
        node = node.children[0]

    while node:
        result.extend(node.keys)
        node = node.next

    # Expected keys: all except multiples of 3
    expected = [n for n in nums if n % 3 != 0]
    assert result == expected

def test_deletion_and_rebalance(mid_tree):
    """Delete keys and verify tree rebalances correctly."""
    values_to_insert = [10, 20, 5, 6, 12, 30, 7, 17, 3, 25, 15]
    for val in values_to_insert:
        mid_tree.insert(val, f"val{val}")

    values_to_delete = [30, 25, 20, 17, 15, 12, 10]
    for val in values_to_delete:
        deleted = mid_tree.delete(val)
        assert deleted is True
        # Optional: verify the key is no longer searchable
        assert mid_tree.search(val) is None

    # Traverse leaves to get remaining keys in order
    result = []
    node = mid_tree.root
    while isinstance(node, BPlusTreeInternalPage):
        node = node.children[0]

    while node:
        result.extend(node.keys)
        node = node.next

    # Remaining keys after deletions
    expected_keys = sorted(set(values_to_insert) - set(values_to_delete))
    assert result == expected_keys

    # Root should exist and be leaf or internal
    assert isinstance(mid_tree.root, (BPlusTreeLeafPage, BPlusTreeInternalPage))

# ---------------------------
# Edge Cases
# ---------------------------

def test_insert_duplicate(small_tree):
    small_tree.insert(1, "A")
    small_tree.insert(1, "B")  # duplicate insertion
    # Your B+Tree ignores duplicates
    assert small_tree.search(1) == "A"
