# ============================================
# STORAGE + BUFFER MANAGER 
# ============================================

from .disk_manager import DiskManager
from .page_replacer import LRUReplacer

class BufferManager:
    """
    BufferPoolManager <-> Disk pages
    
    Responsibilities:
      - Fetch pages from DiskManager
      - Store pages in memory (buffer pool)
      - Write dirty pages to disk before reuse
      - Evict pages using LRU replacer when needed

    Rules:
      - Pinned pages cannot be evicted
      - Dirty pages must be written to disk before eviction
      - Use LRU policy for replacement
    """

    def __init__(self, no_of_frames: int):
        ## TODO: initialize buffer_pool, page_table, disk_manager, replacer, and buffer_total_no_of_frames
        self.buffer_total_no_of_frames = no_of_frames
        self.buffer_pool = {}          # page_id -> Page object
        self.page_table = {}           # page_id -> frame index
        self.disk_manager = DiskManager()
        self.replacer = LRUReplacer()
        pass

    # -----------------------------
    # Getters
    # -----------------------------
    def getBufferPool(self):
        ## TODO: return the list of pages in the buffer pool
        return list(self.buffer_pool.values())


    def getPageTable(self):
        ## TODO: return the list of page_ids currently in the buffer pool
        return list(self.page_table.keys())
    

    def getReplacer(self):
        ## TODO: return the replacer object
        return self.replacer
    

    def getDiskManager(self):
        ## TODO: return the disk manager object
        return self.disk_manager
        

    # -----------------------------
    # Core operations
    # -----------------------------
    def fetchPage(self, page_id):
        """
        Fetch a page into the buffer pool.
        
        Instructions:
          - Case 1: Page is already in buffer
              * Pin the page
              * Increment pin count
              * Update replacer
              * Return page
          - Case 2: Page is not in buffer
              * If buffer has space: load page from disk and pin
              * Else (buffer full):
                  - Ask replacer for a victim
                  - If no victim available → return error / None
                  - If victim is dirty → write back to disk
                  - Replace victim with new page
        """
        ## TODO: implement fetchPage logic
        
        if page_id in self.buffer_pool:
            page = self.buffer_pool[page_id]
            page.incrementPinCount()
            self.replacer.pin(page_id)
            return page
 
        if len(self.buffer_pool) >= self.buffer_total_no_of_frames:
            victim_id = self.replacer.victim()
            if victim_id is None:
                raise Exception("No victim aval")

            victim_page = self.buffer_pool[victim_id]
            if victim_page.isDirty():
                self.disk_manager.writePage(victim_page)
            del self.buffer_pool[victim_id]
            del self.page_table[victim_id]
      
        new_page = self.disk_manager.readPage(page_id)
        if new_page is None:
            raise Exception(f"Page {page_id} not found on disk")

        new_page.incrementPinCount()
        self.buffer_pool[page_id] = new_page
        self.page_table[page_id] = page_id
    
        return new_page
        

    def newPage(self, page_id):
        """
        Load a page from disk.
        
        Instructions:
          - Check if page exists in DiskManager
          - If it exists:
              * Pin page
              * Update replacer
              * Return page
          - Else return None
        """
        ## TODO: implement newPage
        new_page = self.disk_manager.readPage(page_id)
        if new_page is None:
            raise Exception(f"Page {page_id} not found on disk")

        new_page.incrementPinCount()
        self.buffer_pool[page_id] = new_page
        self.page_table[page_id] = page_id
    
        return new_page
        

    def deletePage(self, page_id):
        """
        Delete a page from buffer pool and disk.
        
        Instructions:
          - Only delete if page is unpinned
          - If pinned → print error and return False
          - Remove page from buffer_pool, page_table, and disk
        """
        ## TODO: implement deletePage
        if page_id not in self.buffer_pool:
            self.disk_manager.deletePage(page_id)
            return True

        page = self.buffer_pool[page_id]
        if page.getPinCount() > 0:
            raise Exception("Cant delete pined page")

        del self.buffer_pool[page_id]
        del self.page_table[page_id]
        self.disk_manager.deletePage(page_id)
        return True
        

    def unpinPage(self, page_id, is_dirty):
        """
        Unpin a page in the buffer pool.
        
        Instructions:
          - Decrement page pin count
          - If is_dirty=True → mark page as dirty
          - If pin_count == 0 → add page back to replacer
        """
        ## TODO: implement unpinPage
        if page_id not in self.buffer_pool:
            raise Exception("Page not found in buffer")

        page = self.buffer_pool[page_id]
        page.decrementPinCount()
        if is_dirty:
            page.dirty = True
        if page.getPinCount() == 0:
            # Now eligible for eviction; add to replacer
            self.replacer.unpin(page_id)
        return True
        

    def flushPage(self, page_id):
        """
        Force write a page to disk.
        
        Instructions:
          - Write page to disk
          - Mark page as clean
        """
        ## TODO: implement flushPage
        if page_id not in self.buffer_pool or page_id not in self.disk_manager.pages:
            raise Exception("Invalid")

        page = self.buffer_pool[page_id]
        self.disk_manager.writePage(page)
        page.dirty = False
        return True
        

    def flushAllPages(self):
        """
        Force write all pages in buffer to disk.
        
        Instructions:
          - Iterate over all pages in buffer pool
          - Write each to disk
          - Mark all as clean
        """
        ## TODO: implement flushAllPages
        for page in self.buffer_pool.values():
            self.disk_manager.writePage(page)
            page.dirty = False
        


