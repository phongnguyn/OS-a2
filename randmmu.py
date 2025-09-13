from mmu import MMU

class RandMMU(MMU):
    def __init__(self, frames):
        super().__init__(frames)    

    def read_memory(self, page_number):
        if (self.frame_list.count(page_number) > 0):
            # Page hit
            if self.debug:
                print(f"Page {page_number} hit in frame.")
        else:
            # Page fault
            self.total_page_faults += 1
            self.total_disk_reads += 1
            if self.debug:
                print(f"Page {page_number} fault.")
            if len(self.frame_list) < self.frames:
                # There is still space in memory
                self.frame_list.append(page_number)
                self.page_table[page_number] = {'dirty': False}
                if self.debug:
                    print(f"Loaded page {page_number} into frame.")
            else:
                # Need to replace a page using Random Replacement
                import random
                rand_index = random.randint(0, self.frames - 1)
                rand_page = self.frame_list[rand_index]
                if self.page_table[rand_page]['dirty']:
                    self.total_disk_writes += 1
                    if self.debug:
                        print(f"Writing dirty page {rand_page} back to disk.")
                # Replace the random page with the new page
                self.frame_list[rand_index] = page_number
                del self.page_table[rand_page]
                self.page_table[page_number] = {'dirty': False}
                if self.debug:
                    print(f"Replaced page {rand_page} with page {page_number}.")

    def write_memory(self, page_number):
        if (self.frame_list.count(page_number) > 0):
            # Page hit
            if self.debug:
                print(f"Page {page_number} hit in frame.")
            # Mark the page as dirty
            self.page_table[page_number]['dirty'] = True
        else:
            # Page fault
            self.total_page_faults += 1
            self.total_disk_reads += 1
            if self.debug:
                print(f"Page {page_number} fault.")
            if len(self.frame_list) < self.frames:
                # There is still space in memory
                self.frame_list.append(page_number)
                self.page_table[page_number] = {'dirty': True}
                if self.debug:
                    print(f"Loaded page {page_number} into frame and marked as dirty.")
            else:
                # Need to replace a page using Random Replacement
                import random
                rand_index = random.randint(0, self.frames - 1)
                rand_page = self.frame_list[rand_index]
                if self.page_table[rand_page]['dirty']:
                    self.total_disk_writes += 1
                    if self.debug:
                        print(f"Writing dirty page {rand_page} back to disk.")
                # Replace the random page with the new page
                self.frame_list[rand_index] = page_number
                del self.page_table[rand_page]
                self.page_table[page_number] = {'dirty': True}
                if self.debug:
                    print(f"Replaced page {rand_page} with page {page_number} and marked as dirty." )