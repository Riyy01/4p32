from storage_manager import BufferManager, Page

def main():
    # Initialize buffer manager with only 2 frames (forces eviction quickly)
    bpm = BufferManager(no_of_frames=2)

    # Preload pages on disk
    for i in range(1, 5):
        bpm.disk_manager.writePage(Page(i))

    # -----------------------------
    # Fetch pages
    # -----------------------------
    print("\n--- Fetch page 1 ---")
    page1 = bpm.fetchPage(1)
    print(f"Page 1 pin count: {page1.getPinCount()}")

    print("\n--- Fetch page 2 ---")
    page2 = bpm.fetchPage(2)
    print(f"Page 2 pin count: {page2.getPinCount()}")

    print("\n--- Fetch page 3 (forces eviction) ---")
    try:
        page3 = bpm.fetchPage(3)
        print(f"Page 3 fetched, buffer pool: {[p.page_id for p in bpm.getBufferPool()]}")
    except RuntimeError as e:
        print("Failed to fetch page 3:", e)

    # -----------------------------
    # Unpin pages
    # -----------------------------
    print("\n--- Unpin page 2 (mark dirty) ---")
    bpm.unpinPage(2, is_dirty=True)
    print(f"Page 2 dirty: {page2.isDirty()}, pin count: {page2.getPinCount()}")

    print("\n--- Unpin page 1 ---")
    bpm.unpinPage(1, is_dirty=False)
    print(f"Page 1 pin count: {page1.getPinCount()}")

    # -----------------------------
    # Flush pages
    # -----------------------------
    print("\n--- Flush all pages ---")
    bpm.flushAllPages()
    print("All pages flushed. Dirty flags reset.")

    # -----------------------------
    # Delete pages
    # -----------------------------
    print("\n--- Delete page 1 ---")
    try:
        bpm.deletePage(1)
        print("Page 1 deleted.")
    except RuntimeError as e:
        print("Failed to delete page 1:", e)

    # -----------------------------
    # Invalid page operations
    # -----------------------------
    print("\n--- Attempt to fetch invalid page 1 ---")
    try:
        page_invalid = bpm.fetchPage(1)
        print("Fetched page:", page_invalid.page_id)
    except Exception as e:
        print("Error:", e)

    print("\n--- Attempt to unpin invalid page 999 ---")
    try:
        bpm.unpinPage(1, is_dirty=True)
    except Exception as e:
        print("Error:", e)

    print("\n--- Attempt to flush invalid page 999 ---")
    try:
        bpm.flushPage(1)
    except Exception as e:
        print("Error:", e)
    # -----------------------------
    # Final state
    # -----------------------------
    print("\nFinal buffer pool:", [p.page_id for p in bpm.getBufferPool()])
    print("Disk contents:", list(bpm.disk_manager.pages.keys()))

if __name__ == "__main__":
    main()
