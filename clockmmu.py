from mmu import MMU


class ClockMMU(MMU):
    def __init__(self, frames):
        super().__init__(frames)
        self.pointer = 0

    def read_memory(self, page_number):
        if (self.frame_list.count(page_number) > 0):
            # Page hit
            if self.debug:
                print(f"Page {page_number} hit in frame.")
            # Set the use bit
            self.page_table[page_number]['use_bit'] = 1
        else:
            # Page fault
            self.total_page_faults += 1
            self.total_disk_reads += 1
            if self.debug:
                print(f"Page {page_number} fault.")
            if len(self.frame_list) < self.frames:
                # There is still space in memory
                self.frame_list.append(page_number)
                self.page_table[page_number] = {'dirty': False, 'use_bit': 1}
                if self.debug:
                    print(f"Loaded page {page_number} into frame.")
            else:
                # Need to replace a page using Clock Replacement
                while True:
                    current_page = self.frame_list[self.pointer]
                    if self.page_table[current_page]['use_bit'] == 0:
                        # Replace this page
                        if self.page_table[current_page]['dirty'] == 1:
                            self.total_disk_writes += 1
                            if self.debug:
                                print(f"Writing dirty page {current_page} back to disk.")
                        # Replace the page
                        del self.page_table[current_page]
                        self.frame_list[self.pointer] = page_number
                        self.page_table[page_number] = {'dirty': False, 'use_bit': 1}
                        if self.debug:
                            print(f"Replaced page {current_page} with page {page_number}.")
                        # Move pointer
                        self.pointer = (self.pointer + 1) % self.frames
                        break
                    else:
                        # Give a second chance
                        self.page_table[current_page]['use_bit'] = 0
                        self.pointer = (self.pointer + 1) % self.frames

    def write_memory(self, page_number): 
        if (self.frame_list.count(page_number) > 0):
            # Page hit
            if self.debug:
                print(f"Page {page_number} hit in frame.")
            # Set the use bit and dirty bit
            self.page_table[page_number]['use_bit'] = 1
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
                self.page_table[page_number] = {'dirty': True, 'use_bit': 1}
                if self.debug:
                    print(f"Loaded page {page_number} into frame and marked as dirty.")
            else:
                # Need to replace a page using Clock Replacement
                while True:
                    current_page = self.frame_list[self.pointer]
                    if self.page_table[current_page]['use_bit'] == 0:
                        # Replace this page
                        if self.page_table[current_page]['dirty'] == 1:
                            self.total_disk_writes += 1
                            if self.debug:
                                print(f"Writing dirty page {current_page} back to disk.")
                        # Replace the page
                        del self.page_table[current_page]
                        self.frame_list[self.pointer] = page_number
                        self.page_table[page_number] = {'dirty': True, 'use_bit': 1}
                        if self.debug:
                            print(f"Replaced page {current_page} with page {page_number} and marked as dirty.")
                        # Move pointer
                        self.pointer = (self.pointer + 1) % self.frames
                        break
                    else:
                        # Give a second chance
                        self.page_table[current_page]['use_bit'] = 0
                        self.pointer = (self.pointer + 1) % self.frames

