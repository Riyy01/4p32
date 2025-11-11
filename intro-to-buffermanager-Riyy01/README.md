[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/1zbaEuIN)
# Practical Assignmet 03: Buffer Manager Assignment

## Overview

In this assignment, you will implement a naive Buffer Manager that interacts with a Disk Manager and an LRU Page Replacer. This is a simplified version of what happens inside a real database system, but it teaches fundamental concepts:

- Memory vs disk management
- Page pinning and unpinning
- Dirty page handling
- Page replacement using LRU (Least Recently Used) policy

The goal is to write Python code that correctly manages a buffer pool, handles evictions, and ensures pages are safely written to disk.


## Assignment Tasks

You will implement the following:

### 1. BufferManager

- `fetchPage(page_id)`  
  Fetch a page from the buffer pool. If the page is not in memory:
  - If there is space, load it from disk.
  - If buffer is full, select a victim page using LRU replacer and evict it (if pinned, handle appropriately).
  - Update pin counts and return the page object.

- `newPage(page_id)`  
  Load a page from disk and pin it. Return `None` if page does not exist.

- `deletePage(page_id)`  
  Delete a page from buffer and disk. Only delete if page is unpinned.

- `unpinPage(page_id, is_dirty)`  
  Decrement the page’s pin count. Mark as dirty if modified. If pin count reaches 0, make it eligible for replacement.

- `flushPage(page_id)`  
  Write a page to disk immediately and mark it clean.

- `flushAllPages()`  
  Write all pages in the buffer pool to disk and mark them clean.


### 2. Page

Implement a class to represent in-memory pages. Each page should track:

- `page_id` – unique identifier
- `pin_count` – number of times the page is pinned
- `dirty` – whether the page has been modified

Methods:

- `incrementPinCount()`
- `decrementPinCount()`
- `isDirty()`
- `getPinCount()`


### 3. LRUReplacer

Implement the LRU replacement policy:

- Maintain a list of **free frames** (unpinned pages).
- `pin(page_id)` → remove page from free frames.
- `unpin(page_id)` → add page to free frames.
- `victim()` → select the least recently used page to evict. Return `False` if no pages can be evicted.


## Instructions

1. **Implement all functions marked with `## TODO:`** in `buffer_manager.py`, `page.py`, and `page_replacer.py`.
2. Make sure the **pin count and dirty flags** are handled correctly.
3. Test your implementation using **pytest** in the `tests/` folder:

```bash
pytest test_buffer_manager.py
```

Run main.py to see an example of the buffer manager in action.

## Rules and  Tips
- A pinned page cannot be evicted.
- A dirty page must be written back before eviction.
- Follow the LRU policy strictly when selecting a victim.
- Keep the page table and buffer pool lists aligned.
- Carefully manage pin counts to avoid eviction errors.

