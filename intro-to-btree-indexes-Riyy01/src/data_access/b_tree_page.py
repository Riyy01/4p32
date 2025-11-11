from typing import List, Any, Optional
# ===================================================
# Base Page
# ===================================================
class BPlusTreePage:
    """
    Base class for B+Tree pages.
    Both leaf and internal pages inherit from this class.
    Stores metadata common to all pages:
    - size: number of value in this page
    - max_size: maximum number of value allowed
    """
    def __init__(self, max_size: int):
        self.size = 0
        self.max_size = max_size
        self.parent: Optional['BPlusTreeInternalPage'] = None  # parent pointer

    def is_full(self):
        """
        Check whether the page is full.
        Returns True if the number of values has reached max_size.
        """
        return self.size > self.max_size
    
    def __str__(self):
        return f"[Node: {self.keys}, Size: {self.size}]"
    

# ===================================================
# Leaf Page
# ===================================================
class BPlusTreeLeafPage(BPlusTreePage):
    """
    Leaf page stores actual key-value pairs.
    - keys: sorted list of keys
    - values: list of corresponding values (e.g., RIDs)
    - next: pointer to the next leaf page (used for in-order iteration)
    """
    def __init__(self, max_size: int):
        super().__init__(max_size)
        self.keys: List[Any] = []
        self.values: List[Any] = []

        # we are using doubly-linked list pointers for leaf nodes!!!
        self.next: Optional['BPlusTreeLeafPage'] = None
        self.prev: Optional['BPlusTreeLeafPage'] = None

    def get(self, idx):
        return self.keys[idx], self.values[idx]
    
    def insert(self, key, value):
        """
        Insert a key into the leaf page.
        Keeps keys sorted using linear search.
        Returns False if key already exists (duplicate), True otherwise.
        """

        # Find correct position using linear search
        idx = 0
        while idx < len(self.keys) and self.keys[idx] < key:
            idx += 1

        # Check for duplicate key
        if idx < len(self.keys) and self.keys[idx] == key:
            print('Duplicated Keys')
            return False  # duplicate key

        # Insert key and value at the found position
        self.keys.insert(idx, key)
        self.values.insert(idx, value)
        self.size += 1
        return True

    def delete(self, key):
        """
        Delete a key from the leaf page.
        Returns True if deleted, False if key not found.
        """
        if key in self.keys:
            idx = self.keys.index(key)
            self.keys.pop(idx)
            self.values.pop(idx)
            self.size -= 1
            return True
        return False
    
    def find_index(self, key) -> int:
        """
        Linear search to find the index for a given key.
        Returns index i such that the key should go between keys[i-1] and keys[i].
        """
        idx = 0
        while idx < len(self.keys) and key >= self.keys[idx]:
            idx += 1
        return idx

# ===================================================
# Internal Page
# ===================================================
class BPlusTreeInternalPage(BPlusTreePage):
    """
    Internal page stores keys and child pointers.
    - keys: list of keys used for guiding search
    - children: list of child pages (one more than keys)
    """
    def __init__(self, max_size: int):
        super().__init__(max_size)
        self.keys: List[Any] = []
        self.children: List[Any] = []

    def delete(self, child):
        """
        Delete a child from the internal page.
        Returns True if deleted, False if key not found.
        """
        idx = self.children.index(child)
        self.children.pop(idx)

        # Remove corresponding separator key
        # The key at index i-1 separates children i-1 and i
        if idx > 0 and self.keys:
            self.keys.pop(idx - 1)
        elif self.keys:
            self.keys.pop(0)

        self.size -= 1
    
    def find_child_index_by_key(self, key):
        """
        Linear search to find the child index to follow for a given key.
        Returns index i such that the key should go between keys[i-1] and keys[i].
        """
        idx = 0
        while idx < len(self.keys) and key >= self.keys[idx]:
            idx += 1
        return idx
    
    def find_child_index(self, child):
        """
        Linear search to find the child index to follow for a given key.
        Returns index i such that the key should go between keys[i-1] and keys[i].
        """
        return self.children.index(child)
   
        
