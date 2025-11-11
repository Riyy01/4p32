import math
from typing import List, Any, Optional
from .b_tree_page import BPlusTreePage, BPlusTreeInternalPage, BPlusTreeLeafPage


# ---------------------------
# B+Tree Implementation
# ---------------------------
class BPlusTree:
    """
    A B+ Tree implementation with support for search, insert, and delete operations.
    
    Key properties of B+ trees:
    - All data is stored in leaf nodes
    - Internal nodes contain only keys for navigation
    - Leaf nodes are linked together for range queries
    - Tree remains balanced through splits and merges
    """
    
    def __init__(self, order=4):
        """
        Initialize a B+ tree with the specified order.
        
        Args:
            order: Maximum number of children an internal node can have
                  Also determines max keys = order - 1
        """
        self.order = order
        self.internal_size = order - 1  # Max keys per internal node
        # Start with a single leaf node as root
        self.root: BPlusTreePage = BPlusTreeLeafPage(self.internal_size)

    # ---------------------------
    # Search Operations
    # ---------------------------
    def search(self, key) -> Optional[Any]:
        """
        Search for a key in the B+ tree and return its associated value.
        
        Args:
            key: The key to search for
            
        Returns:
            The value associated with the key, or None if not found
        """
        node = self.root
        
        # TODO: Traverse down through internal nodes to find the correct leaf
        while isinstance(node, BPlusTreeInternalPage):
            idx = self._find_child_index(node.keys, key)
            node = node.children[idx]
        
        # Now we're at a leaf node - check if key exists
        if key in node.keys:
            return node.values[node.keys.index(key)]
        return None
    
    # ---------------------------
    # Insert Operations
    # ---------------------------
    def insert(self, key, value):
        """
        Insert a key-value pair into the B+ tree.
        Handles root splitting when necessary.
        
        Args:
            key: The key to insert
            value: The value associated with the key
        """
        # Recursively insert starting from root
        split = self._insert_recursive(self.root, key, value)
        
        # If root was split, create new root
        if split:
            promoted_key, new_child = split
            new_root = BPlusTreeInternalPage(self.internal_size)
            new_root.keys = [promoted_key]
            new_root.children = [self.root, new_child]
            
            # Update parent pointers
            self.root.parent = new_root
            new_child.parent = new_root
            self.root = new_root
            new_root.size += 1
    
    def _insert_recursive(self, node, key, value):
        """
        Recursively insert a key-value pair into the tree.
        
        Args:
            node: Current node being processed
            key: Key to insert
            value: Value to insert
            
        Returns:
            None if no split occurred, or (promoted_key, new_node) if split occurred
        """
        
        if isinstance(node, BPlusTreeLeafPage):
            # TODO: insert into leaf node
            # TODO: Check if leaf is now overfull and needs splitting
            insert_idx = 0
            while insert_idx < len(node.keys) and node.keys[insert_idx] < key:
                insert_idx += 1

           
            if insert_idx < len(node.keys) and node.keys[insert_idx] == key:
            
                return None

            node.keys.insert(insert_idx, key)
            node.values.insert(insert_idx, value)
            node.size = len(node.keys)
            if len(node.keys) > node.max_size:
                return self._split_leaf(node)
            
            return None

        # Recursive case: navigate to appropriate child
        idx = self._find_child_index(node.keys, key) #TODO
        child = node.children[idx]
        split = self._insert_recursive(child, key, value)
        
        # Handle child split by promoting key to this internal node
        if split:
            promoted_key, new_child = split
            node.keys.insert(idx, promoted_key)
            node.children.insert(idx + 1, new_child)
            new_child.parent = node
            node.size += 1
            
            # TODO: Check if this internal node is now overfull
            if len(node.keys) > node.max_size:
                return self._split_internal(node)
            
        return None

    # ---------------------------
    # Node Splitting Operations
    # ---------------------------
    def _split_leaf(self, leaf: BPlusTreeLeafPage):
        """
        Split a full leaf node into two nodes.
        
        Args:
            leaf: The leaf node to split
            
        Returns:
            (promoted_key, new_leaf): Key to promote and the new right leaf
        """
        mid = len(leaf.keys) // 2
        new_leaf = BPlusTreeLeafPage(leaf.max_size)
        
        # TODO: Move right half of keys/values to new leaf
        new_leaf.keys = leaf.keys[mid:]
        new_leaf.values = leaf.values[mid:]
        new_leaf.size = len(new_leaf.keys)

        # TODO: Keep left half in original leaf
        leaf.keys = leaf.keys[:mid]
        leaf.values = leaf.values[:mid]
        leaf.size = len(leaf.keys)

        # TODO: Update doubly-linked list pointers for leaf nodes
        # This enables efficient range queries
        new_leaf.next = leaf.next
        new_leaf.prev = leaf
        if leaf.next:
            leaf.next.prev = new_leaf
        leaf.next = new_leaf

        # TODO: Set parent pointer for new leaf
        new_leaf.parent = leaf.parent

        # In B+ trees, we promote the first key of the right leaf
        # (not the middle key like in B trees)
        return new_leaf.keys[0], new_leaf

    def _split_internal(self, internal: BPlusTreeInternalPage):
        """
        Split a full internal node into two nodes.
        
        Args:
            internal: The internal node to split
            
        Returns:
            (promoted_key, new_internal): Key to promote and the new right internal node
        """
        mid = len(internal.keys) // 2
        new_internal = BPlusTreeInternalPage(internal.max_size)
        
        # TODO: Move right half of keys/children to new internal node
        new_internal.keys = internal.keys[mid + 1:]
        new_internal.children = internal.children[mid + 1:]
        new_internal.size = len(new_internal.keys)
        
        # TODO: Update parent pointers for moved children
        for child in new_internal.children:
            child.parent = new_internal
        new_internal.parent = internal.parent

        # The middle key gets promoted to parent (not copied)
        promoted_key = internal.keys[mid]

        # TODO: Keep left half in original internal node
        internal.keys = internal.keys[:mid]
        internal.children = internal.children[:mid + 1]
        internal.size = len(internal.keys)
    
        return promoted_key, new_internal
    
    # ---------------------------
    # Delete Operations
    # ---------------------------
    def delete(self, key) -> bool:
        """
        Delete a key from the B+ tree.
        
        Args:
            key: The key to delete
            
        Returns:
            True if the key was found and deleted, False otherwise
        """
        deleted = self._delete_recursive(self.root, key)
        
        # Handle root collapse - if root is internal with only one child
        if isinstance(self.root, BPlusTreeInternalPage) and len(self.root.children) == 1:
            self.root = self.root.children[0]
            self.root.parent = None
            
        return deleted

    def _delete_recursive(self, node, key) -> bool:
        """
        Recursively delete a key from the tree.
        
        Args:
            node: Current node being processed
            key: Key to delete
            
        Returns:
            True if deletion was successful, False if key not found
        """
        if isinstance(node, BPlusTreeLeafPage):
            return self._delete_from_leaf(node, key)
        elif isinstance(node, BPlusTreeInternalPage):
            return self._delete_from_internal(node, key)
        return False

    def _delete_from_leaf(self, leaf: BPlusTreeLeafPage, key) -> bool:
        """
        Delete a key from a leaf node and handle underflow.
        
        Args:
            leaf: The leaf node to delete from
            key: The key to delete
            
        Returns:
            True if deletion was successful, False if key not found
        """
        # Check if key exists in this leaf
        if key not in leaf.keys:
            return False
            
        # TODO: Remove the key-value pair
        idx = leaf.keys.index(key)
        leaf.keys.pop(idx)
        leaf.values.pop(idx)
        leaf.size = len(leaf.keys)

        # Calculate minimum number of keys required
        min_keys = math.ceil(leaf.max_size / 2)
        
        # If leaf has enough keys or is root, we're done
        if leaf.size >= min_keys or leaf == self.root:
            return True

        # Handle underflow by borrowing or merging
        prev_leaf = leaf.prev
        next_leaf = leaf.next

        # Try to borrow from left sibling
        if prev_leaf and prev_leaf.parent == leaf.parent and prev_leaf.size > min_keys:
            # Move last key-value from previous leaf to beginning of current leaf
            leaf.keys.insert(0, prev_leaf.keys.pop(-1))
            leaf.values.insert(0, prev_leaf.values.pop(-1))
            leaf.size += 1
            prev_leaf.size -= 1
            
            # Update parent key that separates these leaves
            self._update_parent_key_after_borrow(leaf, leaf.keys[0])
            return True

        # Try to borrow from right sibling
        if next_leaf and next_leaf.parent == leaf.parent and next_leaf.size > min_keys:
            # Move first key-value from next leaf to end of current leaf
            leaf.keys.append(next_leaf.keys.pop(0))
            leaf.values.append(next_leaf.values.pop(0))
            leaf.size += 1
            next_leaf.size -= 1
            
            # Update parent key that separates these leaves
            self._update_parent_key_after_borrow(next_leaf, next_leaf.keys[0])
            return True

        # Try to merge with left sibling
        if prev_leaf and prev_leaf.parent == leaf.parent:
            # Merge current leaf into previous leaf
            prev_leaf.keys.extend(leaf.keys)
            prev_leaf.values.extend(leaf.values)
            prev_leaf.size = len(prev_leaf.keys)
            
            # Update linked list pointers
            prev_leaf.next = leaf.next
            if leaf.next:
                leaf.next.prev = prev_leaf
                
            # Remove current leaf from parent
            self._remove_leaf_from_parent(leaf)
            return True

        # Try to merge with right sibling
        if next_leaf and next_leaf.parent == leaf.parent:
            # Merge next leaf into current leaf
            leaf.keys.extend(next_leaf.keys)
            leaf.values.extend(next_leaf.values)
            leaf.size = len(leaf.keys)
            
            # Update linked list pointers
            leaf.next = next_leaf.next
            if next_leaf.next:
                next_leaf.next.prev = leaf
                
            # Remove next leaf from parent
            self._remove_leaf_from_parent(next_leaf)
            return True

        return True

    def _update_parent_key_after_borrow(self, leaf, new_first_key):
        """
        Update parent keys after borrowing between leaf nodes.
        
        Args:
            leaf: The leaf whose first key changed
            new_first_key: The new first key of the leaf
        """
        parent = leaf.parent
        if not parent:
            return
            
        # TODO: Find the index of this leaf in parent's children
        leaf_idx = parent.children.index(leaf)
        
        # Update the separator key (the key that points to this leaf)
        if leaf_idx > 0:
            parent.keys[leaf_idx - 1] = new_first_key

    def _remove_leaf_from_parent(self, leaf):
        """
        Remove a leaf node from its parent and handle the resulting changes.
        
        Args:
            leaf: The leaf node to remove
        """
        parent = leaf.parent
        if not parent:
            # Removing root leaf - tree becomes empty
            if leaf == self.root:
                self.root = BPlusTreeLeafPage(self.internal_size)
            return
            
        # TODO: Find position of leaf in parent
        leaf_idx =parent.children.index(leaf)
        parent.children.pop(leaf_idx)
        
        # Remove corresponding separator key
        # The key at index i-1 separates children i-1 and i
        if leaf_idx > 0 and parent.keys:
            parent.keys.pop(leaf_idx - 1)
        elif parent.keys:
            parent.keys.pop(0)
            
        parent.size = len(parent.keys)  # Update size after key removal
        
        # Check what to do with parent after removal
        self._handle_internal_after_child_removal(parent)

    def _delete_from_internal(self, node: BPlusTreeInternalPage, key) -> bool:
        """
        Handle deletion that passes through an internal node.
        
        Args:
            node: The internal node
            key: The key to delete
            
        Returns:
            True if deletion was successful, False if key not found
        """
        # TODO: Find which child should contain the key
        idx = self._find_child_index(node.keys, key)
        child = node.children[idx]
        
        # Recursively delete from child
        deleted = self._delete_recursive(child, key)
        if not deleted:
            return False
            
        # Check if this internal node needs rebalancing
        min_children = math.ceil((node.max_size + 1) / 2)
        if len(node.children) < min_children and node != self.root:
            self._rebalance_internal(node)
        
        return True

    def _handle_internal_after_child_removal(self, internal_node):
        """
        Handle an internal node after one of its children has been removed.
        Decides whether to remove the node entirely or rebalance it.
        
        Args:
            internal_node: The internal node to handle
        """
        # If node has no children, it should be removed entirely
        if len(internal_node.children) == 0:
            if internal_node == self.root:
                # Root is empty, create new empty tree
                self.root = BPlusTreeLeafPage(self.internal_size)
                return
            else:
                # Remove this empty internal node from its parent
                parent = internal_node.parent
                if parent:
                    node_idx = parent.children.index(internal_node)
                    parent.children.pop(node_idx)
                    
                    # Remove corresponding separator key
                    if node_idx > 0 and parent.keys:
                        parent.keys.pop(node_idx - 1)
                    elif parent.keys:
                        parent.keys.pop(0)
                    
                    parent.size = len(parent.keys)
                    # Recursively handle the parent
                    self._handle_internal_after_child_removal(parent)
                return
        
        # Node has children, check if it needs rebalancing
        min_children = math.ceil((internal_node.max_size + 1) / 2)
        if len(internal_node.children) < min_children and internal_node != self.root:
            self._rebalance_internal(internal_node)

    def _rebalance_internal(self, node: BPlusTreeInternalPage):
        """
        Rebalance an internal node that has too few children.
        
        Args:
            node: The internal node to rebalance
        """
        parent = node.parent
        min_children = math.ceil((node.max_size + 1) / 2)#TODO
        
        # If this is root, handle special cases
        if parent is None:
            if len(node.children) == 1:
                self.root = node.children[0]
                self.root.parent = None
            elif len(node.children) == 0:
                # Root is empty, create new empty tree
                self.root = BPlusTreeLeafPage(self.internal_size)
            return

        # Verify node is still in parent's children (safety check)
        if node not in parent.children:
            return

        # Find siblings
        node_idx = parent.children.index(node)
        left_sibling = parent.children[node_idx - 1] if node_idx > 0 else None
        right_sibling = parent.children[node_idx + 1] if node_idx + 1 < len(parent.children) else None

        # Try to borrow from left sibling
        if left_sibling and len(left_sibling.children) > min_children:
            # Move separator key from parent down to current node
            separator_key = parent.keys[node_idx - 1]
            node.keys.insert(0, separator_key)
            
            # Move last child from left sibling to current node
            borrowed_child = left_sibling.children.pop()
            borrowed_child.parent = node
            node.children.insert(0, borrowed_child)
            
            # Move last key from left sibling up to parent as new separator
            parent.keys[node_idx - 1] = left_sibling.keys.pop()
            left_sibling.size = len(left_sibling.keys)
            node.size = len(node.keys)
            return
            
        # Try to borrow from right sibling
        if right_sibling and len(right_sibling.children) > min_children:
            # Move separator key from parent down to current node
            separator_key = parent.keys[node_idx]
            node.keys.append(separator_key)
            
            # Move first child from right sibling to current node
            borrowed_child = right_sibling.children.pop(0)
            borrowed_child.parent = node
            node.children.append(borrowed_child)
            
            # Move first key from right sibling up to parent as new separator
            parent.keys[node_idx] = right_sibling.keys.pop(0)
            right_sibling.size = len(right_sibling.keys)
            node.size = len(node.keys)
            return
            
        # Try to merge with left sibling
        if left_sibling:
            # Move separator key from parent down to left sibling
            separator_key = parent.keys.pop(node_idx - 1)
            left_sibling.keys.append(separator_key)
            
            # Move all keys and children from current node to left sibling
            left_sibling.keys.extend(node.keys)
            left_sibling.children.extend(node.children)
            
            # Update parent pointers for moved children
            for child in node.children:
                child.parent = left_sibling
                
            # Remove current node from parent
            parent.children.pop(node_idx)
            left_sibling.size = len(left_sibling.keys)
            parent.size = len(parent.keys)
            
            # Handle parent after this merge
            self._handle_internal_after_child_removal(parent)
            return
            
        # Try to merge with right sibling
        if right_sibling:
            # Move separator key from parent down to current node
            separator_key = parent.keys.pop(node_idx)
            node.keys.append(separator_key)
            
            # Move all keys and children from right sibling to current node
            node.keys.extend(right_sibling.keys)
            node.children.extend(right_sibling.children)
            
            # Update parent pointers for moved children
            for child in right_sibling.children:
                child.parent = node
                
            # Remove right sibling from parent
            parent.children.pop(node_idx + 1)
            node.size = len(node.keys)
            parent.size = len(parent.keys)
            
            # Handle parent after this merge
            self._handle_internal_after_child_removal(parent)
            return

    # ---------------------------
    # Utility Methods
    # ---------------------------
    def _find_child_index(self, keys: List[Any], key: Any) -> int:
        """
        Find the index of the child pointer to follow for a given key.
        
        In a B+ tree, if we have keys [k1, k2, k3], we have children [c0, c1, c2, c3]
        where:
        - c0 contains keys < k1
        - c1 contains keys >= k1 and < k2  
        - c2 contains keys >= k2 and < k3
        - c3 contains keys >= k3
        
        Args:
            keys: List of keys in the internal node
            key: The key we're searching for
            
        Returns:
            Index of the child to follow
        """
        for i, k in enumerate(keys):
            if key < k:
                return i
        return len(keys)

    # ---------------------------
    # Tree Visualization
    # ---------------------------
    def print_tree(self):
        """
        Print a visual representation of the B+ tree structure.
        Shows each level of the tree with node contents.
        """
        if not self.root:
            print("Empty tree")
            return
            
        queue = [(self.root, 0)]
        current_level = 0
        print("\n=== B+ Tree Structure ===")
        
        while queue:
            node, level = queue.pop(0)
            
            # Print level separator
            if level != current_level:
                print("")
                current_level = level
                
            # Print node contents
            if isinstance(node, BPlusTreeLeafPage):
                print(f"[Leaf: {node.keys}]", end="  ")
            else:
                print(f"[Internal: {node.keys}]", end="  ")
                # Add children to queue for next level
                for child in node.children:
                    queue.append((child, level + 1))
                    
        print("\n=======================\n")

    def print_leaves(self):
        """
        Print all leaf nodes in order by following the linked list.
        Useful for verifying the leaf-level linked list structure.
        """
        print("=== Leaf Node Chain ===")
        
        # Find leftmost leaf
        node = self.root
        while isinstance(node, BPlusTreeInternalPage):
            node = node.children[0]
            
        # Follow the linked list
        while node:
            print(f"[{node.keys}]", end=" -> " if node.next else "\n")
            node = node.next
            
        print("=======================\n")
        