'''
* Interface for Memory Management Unit.
* The memory management unit should maintain the concept of a page table.
* As pages are read and written to, this changes the pages loaded into the
* the limited number of frames. The MMU keeps records, which will be used
* to analyse the performance of different replacement strategies implemented
* for the MMU.
*
'''
class MMU:
    def __init__(self, frames):
        self.frames = frames
        self.page_table = {}  # page_number -> frame info
        self.frame_list = []  # list of loaded page_numbers
        self.total_disk_reads = 0
        self.total_disk_writes = 0
        self.total_page_faults = 0
        self.debug = False

    def read_memory(self, page_number):
        raise NotImplementedError("Subclasses should implement this!")

    def write_memory(self, page_number):
        raise NotImplementedError("Subclasses should implement this!")

    def set_debug(self):
        self.debug = True

    def reset_debug(self):
        self.debug = False

    def get_total_disk_reads(self):
        return self.total_disk_reads

    def get_total_disk_writes(self):
        return self.total_disk_writes

    def get_total_page_faults(self):
        return self.total_page_faults
