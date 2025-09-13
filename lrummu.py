from mmu import MMU

class LruMMU(MMU):
    def __init__(self, frames):
        self.time = 0
        super().__init__(frames)
        
    def read_memory(self, page_number):
        self.time += 1
        if (self.frame_list.count(page_number) > 0):
            # Page hit
            if self.debug:
                print(f"Page {page_number} hit in frame.")
            # Update the page's last used time
            self.page_table[page_number]['last_used'] = self.time
        else:
            # Page fault
            self.total_page_faults += 1
            self.total_disk_reads += 1
            if self.debug:
                print(f"Page {page_number} fault.")
            if len(self.frame_list) < self.frames:
                # There is still space in memory
                self.frame_list.append(page_number)
                self.page_table[page_number] = {'dirty': False, 'last_used': self.time}
                if self.debug:
                    print(f"Loaded page {page_number} into frame.")
            else:
                # Need to replace a page using LRU
                lru_page = min(self.page_table, key=lambda p: self.page_table[p]['last_used'])
                if self.page_table[lru_page]['dirty']:
                    self.total_disk_writes += 1
                    if self.debug:
                        print(f"Writing dirty page {lru_page} back to disk.")
                # Replace the LRU page with the new page
                self.frame_list.remove(lru_page)
                del self.page_table[lru_page]
                self.frame_list.append(page_number)
                self.page_table[page_number] = {'dirty': False, 'last_used': self.time}
                if self.debug:
                    print(f"Replaced page {lru_page} with page {page_number}.")

    def write_memory(self, page_number):
        self.time += 1
        if (self.frame_list.count(page_number) > 0):
            # Page hit
            if self.debug:
                print(f"Page {page_number} hit in frame.")
            # Mark the page as dirty and update last used time
            self.page_table[page_number]['dirty'] = True
            self.page_table[page_number]['last_used'] = self.time
        else:
            # Page fault
            self.total_page_faults += 1
            self.total_disk_reads += 1
            if self.debug:
                print(f"Page {page_number} fault.")
            if len(self.frame_list) < self.frames:
                # There is still space in memory
                self.frame_list.append(page_number)
                self.page_table[page_number] = {'dirty': True, 'last_used': self.time}
                if self.debug:
                    print(f"Loaded page {page_number} into frame and marked as dirty.")
            else:
                # Need to replace a page using LRU
                lru_page = min(self.page_table, key=lambda p: self.page_table[p]['last_used'])
                if self.page_table[lru_page]['dirty']:
                    self.total_disk_writes += 1
                    if self.debug:
                        print(f"Writing dirty page {lru_page} back to disk.")
                # Replace the LRU page with the new page
                self.frame_list.remove(lru_page)
                del self.page_table[lru_page]
                self.frame_list.append(page_number)
                self.page_table[page_number] = {'dirty': True, 'last_used': self.time}
                if self.debug:
                    print(f"Replaced page {lru_page} with page {page_number} and marked as dirty.")
        
