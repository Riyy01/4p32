class DiskManager:
    """
    A DiskManager that simulates persistent storage using a dictionary.

    In a real DBMS this would handle raw file I/O (read/write blocks from disk).
    For teaching purposes, we store Page objects in memory.
    """

    def __init__(self):
        # Simulated disk storage: maps page_id -> Page
        self.pages = {}
        # Track explicitly invalidated (deleted) pages
        self.invalid = []

    def writePage(self, page):
        """Write a page object to 'disk' (dictionary)."""
        print(f"[DiskManager] Writing page {page.page_id} to disk.")
        self.pages[page.page_id] = page

    def readPage(self, page_id: int):
        """Read a page from disk if it exists and is not invalidated."""
        print(f"[DiskManager] Reading page {page_id} from disk.")
        if page_id in self.invalid:
            print(f"[DiskManager] Page {page_id} is invalid.")
            return None
        return self.pages.get(page_id, None)

    def deletePage(self, page_id: int):
        """Delete a page from disk by page_id."""
        print(f"[DiskManager] Deleting page {page_id} from disk.")
        if page_id in self.pages:
            del self.pages[page_id]
            self.invalid.append(page_id)

    def hasPage(self, page_id: int) -> bool:
        """Check if a page exists on disk (and is not invalid)."""
        return page_id in self.pages and page_id not in self.invalid
