# ============================================
# PAGE AND LRU REPLACER
# ============================================

class Page:
    """
    A class to represent an in-memory page.

    Responsibilities:
      - Track pin count (how many threads/pages are using it)
      - Track if the page is dirty (modified)

    Attributes:
      - page_id : int
      - pin_count : int
      - dirty : bool

    Methods:
      - incrementPinCount(): increase pin_count by 1
      - decrementPinCount(): decrease pin_count by 1
      - isDirty(): returns True if page is dirty
      - getPinCount(): returns current pin_count
    """

    def __init__(self, id):
        ## TODO: initialize page_id, pin_count, and dirty flag
        self.page_id = id
        self.pin_count = 0
        self.dirty = False
        

    def incrementPinCount(self):
        ## TODO: increase pin_count by 1
        self.pin_count += 1
        

    def decrementPinCount(self):
        ## TODO: decrease pin_count by 1      
            self.pin_count -= 1 
        

    def isDirty(self):
        ## TODO: return True if page is dirty
        return self.dirty
        

    def getPinCount(self):
        ## TODO: return current pin_count
        return self.pin_count
        

    def __repr__(self):
        return f"Page(id={self.page_id}, pin={self.pin_count}, dirty={self.dirty})"
