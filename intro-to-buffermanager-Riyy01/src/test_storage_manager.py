# test_buffer_manager.py
import pytest
from storage_manager import BufferManager, Page

@pytest.fixture
def bpm():
    bpm = BufferManager(no_of_frames=2)
    # Preload disk with 3 pages
    for i in range(1, 4):
        bpm.disk_manager.writePage(Page(i))
    return bpm

# -----------------------------
# Fetching pages
# -----------------------------
def test_fetch_existing_page(bpm):
    page1 = bpm.fetchPage(1)
    assert page1.page_id == 1
    assert page1.getPinCount() == 1
    assert 1 in bpm.getPageTable()

def test_fetch_non_existing_page_raises(bpm):
    with pytest.raises(Exception):
        bpm.fetchPage(99)

# -----------------------------
# Pin / Unpin operations
# -----------------------------
def test_unpin_and_repin(bpm):
    page1 = bpm.fetchPage(1)
    bpm.unpinPage(1, is_dirty=False)
    assert page1.getPinCount() == 0
    bpm.fetchPage(1)
    assert page1.getPinCount() == 1

def test_unpin_invalid_page_raises(bpm):
    with pytest.raises(Exception):
        bpm.unpinPage(99, is_dirty=True)

# -----------------------------
# Dirty pages & flush
# -----------------------------
def test_mark_dirty_and_flush(bpm):
    page1 = bpm.fetchPage(1)
    bpm.unpinPage(1, is_dirty=True)
    assert page1.isDirty() is True
    bpm.flushPage(1)
    assert page1.isDirty() is False

def test_flush_all_pages(bpm):
    p1 = bpm.fetchPage(1)
    bpm.unpinPage(1, is_dirty=True)
    bpm.flushAllPages()
    assert p1.isDirty() is False

def test_flush_invalid_page_raises(bpm):
    with pytest.raises(Exception):
        bpm.flushPage(99)

# -----------------------------
# Delete pages
# -----------------------------
def test_delete_unpinned_page(bpm):
    page1 = bpm.fetchPage(1)
    bpm.unpinPage(1, is_dirty=False)
    bpm.deletePage(1)
    assert 1 not in bpm.disk_manager.pages

def test_delete_pinned_page_raises(bpm):
    bpm.fetchPage(1)  # pinned
    with pytest.raises(Exception):
        bpm.deletePage(1)
    assert 1 in bpm.disk_manager.pages

# -----------------------------
# Buffer eviction tests
# -----------------------------
def test_buffer_eviction_when_all_pinned_raises(bpm):
    bpm.fetchPage(1)
    bpm.fetchPage(2)
    with pytest.raises(Exception):
        bpm.fetchPage(3)

def test_buffer_eviction_with_unpinned_page(bpm):
    page1 = bpm.fetchPage(1)
    page2 = bpm.fetchPage(2)
    bpm.unpinPage(1, is_dirty=False)
    assert page1.getPinCount() == 0

    page3 = bpm.fetchPage(3)
    assert page3.page_id == 3
    
    assert 3 in bpm.getPageTable()
    assert 2 in bpm.getPageTable()
    assert 1 not in bpm.getPageTable()
    assert len(bpm.getPageTable()) == 2

# -----------------------------
# Replacer-specific tests
# -----------------------------
def test_lru_order(bpm):
    page1 = bpm.fetchPage(1)
    page2 = bpm.fetchPage(2)
    bpm.unpinPage(1, is_dirty=False)  # 1 becomes free (LRU)
    bpm.unpinPage(2, is_dirty=False)  # 2 becomes MRU
    page3 = bpm.fetchPage(3)          # Should evict page1
    assert page3.page_id == 3
    assert 1 not in bpm.getPageTable()
    assert 2 in bpm.getPageTable()
