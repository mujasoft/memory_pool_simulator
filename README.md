
# Memory Pool Simulator (Fixed & Variable Block Size)

A lightweight, console-based memory pool simulation in Python.  
Implements both **fixed** and **variable block size allocation strategies** — useful for understanding how low-level memory management works.

## Demo

![Demo of the tool](demo.gif)

---

## Features

- **FixedBlockSizeMemoryPool**: A simple allocator using uniform block sizes  
- **VariableBlockSizeMemoryPool**: A smart allocator using tiered block sizes (e.g., GB, MB, KB)  
- **Live visualization** of memory allocation and ownership  
- Memory freeing by block or by process name  
- Summary reports on memory usage per owner  
- MIT licensed and ready for reuse

---

## Why This Project?

- Designed for **systems programming students**, **embedded engineers**, or anyone interested in how **heap-style memory allocation** can be abstracted and simulated.
- Very relevant to the RTOS world!
- Helps visualize how allocation and fragmentation work.
- Small, focused, and easy to understand.


## Usage

Run the script to see both allocators in action:

```bash
python3 main.py
```

You will see terminal output like this:

```
Fixed Block Memory Pool Table:
ID     OWNER           USE
--------------------------
0      initGuest       ■
1      lidarReader     ■
...
```

---

## Example Output (Variable Block Size)

```bash
Variable Block Memory Pool Table:
ID      OWNER           SIZE     USE
------------------------------------
5a1f3a  initGuest       2 GB     ■
73c2e7  sensorReader    2 MB     ■
```

---

## License

MIT License  
© 2025 Mujaheed Khan

---

## Contributing

This is a small educational tool, but PRs are welcome for:
- Improvements in output formatting
- More realistic allocation strategies
- Integration with GUI or web visualizer

