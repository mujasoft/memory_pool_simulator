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
import time

from humanize import naturalsize
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table


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

    def print_summary_table(self, rich_text: bool = True):
        """Print a summary of the table.
        """

        if not rich_text:
            print("Fixed Block Size Memory Pool Summary:")
            print("-"*30)
            print(f"Free memory:  {self.remaining_no_of_blocks}/\
    {self.total_no_of_blocks} blocks")
            print(f"Total Memory: {naturalsize(self.size, binary=True)}")
            print(f"BlockSize:    {naturalsize(self.block_size, binary=True)}")
            print("")

        if rich_text:
            console = Console()

            table = Table(title="\n System Summary")
            table.add_column("Free no. of blocks", style="green")
            table.add_column("Total no. of blocks", style="cyan")
            table.add_column("BlockSize", style="blue")
            table.add_column("Total", style="magenta")

            table.add_row(str(self.remaining_no_of_blocks),
                          str(self.total_no_of_blocks),
                          naturalsize(self.block_size, binary=True),
                          naturalsize(self.size, binary=True))
            console.print(table)

    def print_total_memory_belonging_to_owner(self, owner: str,
                                              rich_text: bool = True):
        """Print a summary of total memory usage for a certain owner.

        Args:
            owner (string): name of owner
        """

        if not rich_text:
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

        if rich_text:
            console = Console()

            total = 0
            block_ids = []
            for block in self.block_table:
                if owner == block["owner"]:
                    total = total + 1
                    block_ids.append(str(block['id']))

            total_memory = naturalsize(total*self.block_size, binary=True)
            lines = [f"Block ID: {bid}" for bid in block_ids]
            body = "\n".join(lines + [f"\n[bold]Total = {len(block_ids)} "
                                      f"blocks[/] or [cyan]{total_memory}[/]"])

            print("")
            console.print(Panel(body, title="Total memory belonging to" +
                                f" '[green]{owner}[/green]'",
                                border_style="blue"))
            print()

    def print_table(self, rich_text: bool = True):
        """Print a visualization of the current state of all blocks."""

        if not rich_text:
            print("Fixed Block Memory Pool Table:")
            print("{:<6} {:<15} {:<4}".format("ID", "OWNER", "USE"))
            print("-" * 26)

            for block in self.block_table:
                block_id = block['id']
                owner = block['owner'] if block['owner'] else "-"
                use = "■" if block['allocated'] else "▢"
                print("{:<6} {:<15} {:<4}".format(block_id, owner, use))
            print("")

        if rich_text:
            console = Console()

            table = Table(title="\nMemory Block Table")
            table.add_column("ID", style="blue")
            table.add_column("OWNER", style="cyan")
            table.add_column("SIZE", style="magenta")
            table.add_column("USE", style="purple")

            for block in self.block_table:
                block_id = block['id']
                owner = block['owner'] if block['owner'] else "-"
                use = "■" if block['allocated'] else "▢"
                if block['allocated']:
                    table.add_row(str(block_id), owner,
                                  naturalsize(self.size, binary=True),
                                  use)
                else:
                    table.add_row(str(block_id), owner,
                                  naturalsize(self.size, binary=True),
                                  use)
            console.print(table)
            print()


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

    def print_summary_table(self, rich_text: bool = True):
        """Print a summary of the table.
        """

        if not rich_text:
            print("Summary of Entire System:")
            print("-"*30)
            print(f"Free memory   {self.remaining_size}")
            print(f"Total Memory  {self.size}")
            print()

        if rich_text:

            free_percentage = round(100*(self.remaining_size/self.size))
            console = Console()

            table = Table(title="\nSystem Summary")
            table.add_column("FREE", style="green")
            table.add_column("TOTAL", style="cyan")

            table.add_row(naturalsize(self.remaining_size, binary=True)
                          + f" ({free_percentage}%)",
                          naturalsize(self.size, binary=True))

            console.print(table)
            print()

    def print_total_memory_belonging_to_owner(self, owner: str,
                                              rich_text: bool = True):
        """Print a summary of total memory usage for a certain owner.

        Args:
            owner (string): name of owner
        """

        if not rich_text:
            print(f"Total memory belonging to '{owner}':")
            print("{:<8} {:<15}".format("ID", "SIZE"))
            print("-"*30)
            total = 0
            total_mem = 0
            for block in self.block_table:
                if owner == block["owner"]:
                    total = total + 1
                    print("{:<8} {:<15}".format(block['id'][:6],
                                                block['size']))
                    total_mem = total_mem + block["size"]

        if rich_text:
            console = Console()

            table = Table(title=f"\nTotal memory belonging to '{owner}'")
            table.add_column("ID", style="magenta")
            table.add_column("SIZE", justify="right", style="blue")

            total = 0
            total_mem = 0
            for block in self.block_table:
                if owner == block["owner"]:
                    total = total + 1
                    table.add_row(block['id'], naturalsize(block['size'],
                                  binary=True))
                    total_mem = total_mem + block["size"]

            console.print(table)

        print(f"\nTotal = {naturalsize(total_mem, binary=True)}"
              + f" consisting of {total} block(s)")
        print("")

    def print_table(self, rich_text: bool = True):
        """Print a visualization of the current state of all the blocks."""

        if not rich_text:
            print("Variable Block Memory Pool Table:")
            print("{:<8} {:<15} {:<8} {:<4}".format("ID", "OWNER", "SIZE",
                                                    "USE"))
            print("-" * 36)

            for block in self.block_table:
                short_id = block['id'][:6]  # Truncate UUID for readability
                owner = block['owner'] if block['owner'] else "-"
                size = get_human_readable_memory_size(block['size'])
                use = "■" if block['allocated'] else "▢"
                print("{:<8} {:<15} {:<8} {:<4}".format(short_id, owner, size,
                                                        use))
            print()

        if rich_text:
            console = Console()

            table = Table(title="\nVariable Block Memory Pool Table")
            table.add_column("ID", style="magenta")
            table.add_column("OWNER", style="cyan")
            table.add_column("SIZE", justify="right", style="blue")

            for block in self.block_table:
                table.add_row(str(block['id']), block['owner'],
                              naturalsize(block['size'], binary=True))

            console.print(table)
            print()


def main():
    print("*** Fixed Block Size Memory Pool Demo ***")
    fixed_memory_pool = FixedBlockSizeMemoryPool(4096, 1024)
    fixed_memory_pool.allocate(1024, "initGuest")
    fixed_memory_pool.allocate(2048, "lidarReader")
    fixed_memory_pool.free(1, "lidarReader")
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


def print_demo(user_string: str, color: str = "yellow",
               style: str = "bold"):
    """Punchy looking output for demo"""

    print(f"[{color}]{user_string} [/{color}]")
    print()


def demo(sleep_interval: int = 3):
    """Slow down the output so that the audience can follow"""

    print(Rule("[bold green]*** Fixed Block Size Memory "
               "Pool Demo ***[/bold green]"))
    print("-> Creating a Fixed Block Memory Pool of 4 MiB with"
          " blocksize 1 MiB\n")
    fixed_memory_pool = FixedBlockSizeMemoryPool(4096, 1024)
    time.sleep(sleep_interval)

    print("-> Allocating 1 MiB to 'initGuest'")
    time.sleep(sleep_interval)
    fixed_memory_pool.allocate(1024, "initGuest")
    time.sleep(sleep_interval)

    print("-> Allocating 2 MiB to 'lidarReader'")
    time.sleep(sleep_interval)
    fixed_memory_pool.allocate(2048, "lidarReader")
    time.sleep(sleep_interval)

    print("-> Allocating 1 MiB to 'radarReader'")
    time.sleep(sleep_interval)
    fixed_memory_pool.allocate(1024, "radarReader")
    time.sleep(sleep_interval)

    print("-> Freeing up fourth block")
    time.sleep(sleep_interval)
    fixed_memory_pool.free(3, "radarReader")
    time.sleep(sleep_interval)

    fixed_memory_pool.print_total_memory_belonging_to_owner("lidarReader")
    time.sleep(sleep_interval)

    print(Rule("[green]*** Variable Block Size Memory Pool Demo  ***[/green]"))
    time.sleep(sleep_interval)
    print("-> Creating Variable Block Sized Pool of 16 GiB with block sizes"
          " of 2 GiB, 2 MiB and 4 KiB.\n")
    var_memory_pool = VariableBlockSizeMemoryPool(17179869184,
                                                  [2147483648, 2097152,
                                                   4096])
    time.sleep(sleep_interval)

    print("-> Allocating 10 GiB to 'initGuest'")
    results = var_memory_pool.allocate(10737418240, "initGuest")
    time.sleep(sleep_interval)
    var_memory_pool.print_table()
    time.sleep(sleep_interval)

    print("-> Allocating 2 MiB to 'sensorReader'")
    time.sleep(sleep_interval)
    var_memory_pool.allocate(2097152, "sensorReader")
    time.sleep(sleep_interval)
    var_memory_pool.print_table()
    time.sleep(sleep_interval)

    print("-> Allocating 2 GiB to 'sensorReader'")
    time.sleep(sleep_interval)
    var_memory_pool.allocate(2147483648, "sensorReader")
    time.sleep(sleep_interval)
    var_memory_pool.print_table()
    time.sleep(sleep_interval)

    print("-> Freeing up first block allocated to 'initGuest'")
    var_memory_pool.free(results[0]['id'], "initGuest")
    time.sleep(sleep_interval)
    var_memory_pool.print_table()
    time.sleep(sleep_interval)

    var_memory_pool.print_summary_table()
    time.sleep(sleep_interval)
    var_memory_pool.print_total_memory_belonging_to_owner("sensorReader")
    print("Notice only 2 blocks had to be allocated instead of 524,800!")


demo(3)
