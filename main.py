# Copyright (c) 2025 Mujaheed Khan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import uuid


def get_human_readable_memory_size(size):
    """Get human readable sizes.

    Args:
        size (int): block size

    Returns:
        str: a nice human readable string. E.g. "4kb instead 4096".
    """
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    while size >= 1024 and i < len(suffixes) - 1:
        size //= 1024
        i += 1
    return f"{size} {suffixes[i]}"


class FixedBlockSizeMemoryPool:
    def __init__(self, size, block_size):
        """Simulate a memory pool with single block size.

        Args:
            size (int): Total amount of memory
            block_size (int): allocate chunks of this much
        """

        self.block_size = block_size
        self.size = size
        no_of_blocks = int(size/block_size)
        self.remaining_no_of_blocks = no_of_blocks
        self.total_no_of_blocks = no_of_blocks

        # Initialize block table.
        block_table = []
        for x in range(no_of_blocks):
            block_table.append({"allocated": False, "id": x, "owner": None})
        self.block_table = block_table

    def allocate(self, size, owner):
        """Allocate a portion of memory.

        Args:
            size (int): Size of memory to request
            owner (string): Calling process name

        Returns:
            bool: True on success and False on failure
        """

        if size > self.size:
            return False

        num_of_blocks = int(size/self.block_size)

        if self.remaining_no_of_blocks == 0:
            return False
        elif self.remaining_no_of_blocks < num_of_blocks:
            return False

        allocated_blocks_so_far = 0
        for block in self.block_table:
            if block["allocated"] is False:
                block["allocated"] = True
                block["owner"] = owner
                allocated_blocks_so_far = allocated_blocks_so_far + 1
                self.remaining_no_of_blocks = self.remaining_no_of_blocks - 1
            if allocated_blocks_so_far == num_of_blocks:
                break

        self.print_table()
        return True

    def free_all(self, owner):
        """Free up memory owned by requestor.

        Args:
            owner (string): name of requesting process or thread

        Returns:
            bool: True on success and False on failure
        """

        fails = 0
        for block in self.block_table:
            if block["owner"] == owner:
                if not self.free(block["id"], owner):
                    fails = fails + 1

        if fails > 0:
            return False
        return True

    def free(self, block_id, owner):
        """Specify which block to free.

        Args:
            block_id (int): index of block to free
            owner (string): name of process

        Returns:
            Bool: True on success and False on failure
        """
        if block_id > self.total_no_of_blocks - 1:
            return False
        if self.block_table[block_id]["allocated"] is False:
            return False
        elif self.block_table[block_id]["owner"] != owner:
            return False
        else:
            self.block_table[block_id]["allocated"] = False
            self.block_table[block_id]["owner"] = None

        self.remaining_no_of_blocks = self.remaining_no_of_blocks + 1

        self.print_table()
        return True

    def print_summary_table(self):
        """Print a summary of the table.
        """

        print("Fixed Block Size Memory Pool Summary:")
        print("-"*30)
        print(f"Free memory:     {self.remaining_no_of_blocks}/\
{self.total_no_of_blocks} blocks")
        print(f"Total Memory:    {self.size}")
        print(f"BlockSize:       {self.block_size}")
        print("")

    def print_total_memory_belonging_to_owner(self, owner):
        """Print a summary of total memory usage for a certain owner.

        Args:
            owner (string): name of owner
        """

        print(f"Total memory belonging to \"{owner}\":")
        print("-"*30)
        total = 0
        for block in self.block_table:
            if owner == block["owner"]:
                total = total + 1
                print(f"Block ID: {block['id']}")

        total_memory = total*self.block_size
        print(f"Total = {total} blocks or {total_memory}")
        print("")

    def print_table(self):
        """Print a visualization of the current state of all blocks."""
        print("Fixed Block Memory Pool Table:")
        print("{:<6} {:<15} {:<4}".format("ID", "OWNER", "USE"))
        print("-" * 26)

        for block in self.block_table:
            block_id = block['id']
            owner = block['owner'] if block['owner'] else "-"
            use = "■" if block['allocated'] else "▢"
            print("{:<6} {:<15} {:<4}".format(block_id, owner, use))
        print("")


class VariableBlockSizeMemoryPool:
    def __init__(self, size, block_sizes):
        """Simulate a memory pool with multiple block sizes.

        Args:
            size (int): Total amount of memory
            block_sizes (int list): allocate in chunks of these lengths
        """

        # Since block sizes are variable, this implementation will
        # focus on tracking the actual amount of memory.
        self.block_sizes = block_sizes
        self.size = size
        self.remaining_size = size
        self.block_table = []

    def allocate_single_block_size(self, size, owner, block_size):
        """Allocate a portion of memory using a single block size.

        Args:
            size (int): Size of memory to request
            owner (string): Calling process name

        Returns:
            list of dicts: Returns list of metadata of allocated blocks.
                           E.g. {"id":"1234..", "owner": "foo",
                                 "allocated": True}
        """

        if size > self.size:
            return False

        if block_size not in self.block_sizes:
            return False

        if self.remaining_size == 0:
            return False
        elif self.remaining_size < size:
            return False

        # This is the easiest usecase. Single block size.
        num_of_blocks = int(size/block_size)

        results = []
        for x in range(num_of_blocks):
            id = str(uuid.uuid4())
            self.block_table.append({"id": id,
                                     "size": block_size, "owner": owner,
                                     "allocated": True})
            results.append({"id": id,
                            "size": block_size, "owner": owner,
                            "allocated": True})
            self.remaining_size = self.remaining_size - block_size
        return results

    def allocate(self, size, owner):
        """Smartly allocates efficiently.

        Args:
            size (int): Size in bytes
            owner (string): Name of owner
        """

        block_sizes = self.block_sizes
        sorted(self.block_sizes, reverse=True)
        results = []
        for block_size in block_sizes:

            if size == 0:
                break

            if size < block_sizes[-1]:
                allocatable_size = block_sizes[-1]
            else:
                allocatable_size = int(size/block_size)*block_size
            results.extend(self.allocate_single_block_size(allocatable_size,
                                                           owner,
                                                           block_size))
            size = size - allocatable_size

        return results

    def free_all(self, owner):
        """Free up memory owned by requestor

        Args:
            owner (string): name of requesting process or thread

        Returns:
            bool: True on success and False on failure
        """

        fails = 0
        blocks_to_remove = []
        for block in self.block_table:
            if block["owner"] == owner:
                blocks_to_remove.append(block['id'])

        for block in blocks_to_remove:

            if not self.free(block, owner):
                fails = fails + 1

        if fails > 0:
            return False
        return True

    def free(self, block_id, owner):
        """Specify which block to free.

        Args:
            block_id (int): index of block to free
            owner (string): name of process

        Returns:
            Bool: True on success and False on failure
        """

        for i, block in enumerate(self.block_table):
            if block['id'] == block_id and block['owner'] == owner:
                self.remaining_size += block["size"]
                del self.block_table[i]
                return True
        return False

    def print_summary_table(self):
        """Print a summary of the table.
        """

        print("Summary of Entire System:")
        print("-"*30)
        print(f"Free memory   {self.remaining_size}")
        print(f"Total Memory  {self.size}")
        print()

    def print_total_memory_belonging_to_owner(self, owner):
        """Print a summary of total memory usage for a certain owner.

        Args:
            owner (string): name of owner
        """

        print(f"Total memory belonging to \"{owner}\":")
        print("{:<8} {:<15}".format("ID", "SIZE"))
        print("-"*30)
        total = 0
        total_mem = 0
        for block in self.block_table:
            if owner == block["owner"]:
                total = total + 1
                print("{:<8} {:<15}".format(block['id'][:6], block['size']))
                total_mem = total_mem + block["size"]

        print(f"\nTotal = {total_mem} consisting of {total} block(s)")
        print("")

    def print_table(self):
        """Print a visualization of the current state of all the blocks."""
        print("Variable Block Memory Pool Table:")
        print("{:<8} {:<15} {:<8} {:<4}".format("ID", "OWNER", "SIZE", "USE"))
        print("-" * 36)

        for block in self.block_table:
            short_id = block['id'][:6]  # Truncate UUID for readability
            owner = block['owner'] if block['owner'] else "-"
            size = get_human_readable_memory_size(block['size'])
            use = "■" if block['allocated'] else "▢"
            print("{:<8} {:<15} {:<8} {:<4}".format(short_id, owner, size,
                                                    use))
        print()


def main():
    print("*** Fixed Block Size Memory Pool Demo ***")
    fixed_memory_pool = FixedBlockSizeMemoryPool(4096, 1024)
    fixed_memory_pool.allocate(1024, "initGuest")
    fixed_memory_pool.allocate(2048, "lidarReader")
    fixed_memory_pool.free(3, "radarReader")
    fixed_memory_pool.print_table()
    fixed_memory_pool.print_summary_table()
    fixed_memory_pool.print_total_memory_belonging_to_owner("lidarReader")

    print("*** Variable Block Size Memory Pool Demo ***")
    var_memory_pool = VariableBlockSizeMemoryPool(17179869184,
                                                  [2147483648, 2097152,
                                                   4096])
    results = var_memory_pool.allocate(10737418240, "initGuest")
    var_memory_pool.allocate(2097152, "sensorReader")
    var_memory_pool.print_table()
    var_memory_pool.free(results[0]['id'], "initGuest")
    var_memory_pool.print_table()
    var_memory_pool.print_summary_table()
    var_memory_pool.print_total_memory_belonging_to_owner("sensorReader")


main()
