class PageReplacer:
    """
    A class to represent the page replacer
    The Replacer keeps track of when Page objects are accessed so that it can decide which one to 
    evict when it must free a frame to make room for copying a new physical page from disk.


    Methods
    -------
    victim():
        return which frame should be evicted from the BufferPool. 
    pin(page_id):
        pin a page in the BufferPool
    unpin():
        unpin a page in the buffer pool
    replacerSize():
        returns the number of frames that are currently in the Replacer.

    """
    def __init__(self):
        pass

    def victim(self):
        pass

    def pin(self, page_id):
        pass
    
    def unpin(self, page_id):
        pass

    def replacerSize(self):
        pass

    
class LRUReplacer:
    """
    LRU Replacer keeps track of unpinned pages and selects the least recently used page to evict.

    Responsibilities:
      - Maintain list of free frames (unpinned pages)
      - Pin a page → remove from free_frames
      - Unpin a page → add back to free_frames
      - Victim() → select LRU page for eviction

    Attributes:
      - free_frames : list of page_ids eligible for eviction
    """

    def __init__(self):
        ## TODO: initialize free_frames list
        self.free_frames = []
        

    def replacerSize(self):
        ## TODO: return number of pages currently in free_frames
        return len(self.free_frames)
        

    def getFreeFrames(self):
        ## TODO: return the free_frames list
        return self.free_frames
        

    def pin(self, page_id):
        """
        Pin a page:
          - Remove page_id from free_frames (it cannot be evicted while pinned)
        """
        ## TODO: implement pin logic
        if page_id in self.free_frames:
            self.free_frames.remove(page_id)
    

    def unpin(self, page_id):
        """
        Unpin a page:
          - Add page_id to free_frames if not already present
          - Usually add to the front (most recently unpinned)
        """
        ## TODO: implement unpin logic
        if page_id not in self.free_frames:
            self.free_frames.insert(0, page_id)
        

    def victim(self):
        """
        Select a victim page for eviction:
          - Return the least recently used page_id from free_frames
          - Remove it from free_frames
          - If free_frames is empty → return False / None
        """
        ## TODO: implement victim selection
        if not self.free_frames:
            return None
        return self.free_frames.pop()
        