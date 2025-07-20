# Memory Pool Simulator (Fixed & Variable Block Sizes)

A lightweight, terminal-based simulator that demonstrates how memory allocation works using both **fixed-size** and **variable-size** block strategies. This is perfect for visual learners and systems programmers. I sure wish I had something like this when I was starting out!

## Demo
![Demo of the tool](demo.gif)

---

## Features

- **FixedBlockSizeMemoryPool**
  - Allocates memory using equal-sized blocks
- **VariableBlockSizeMemoryPool**
  - Allocates memory using tiered sizes (e.g., GB, MB, KB)
- **Rich terminal visualizations** powered by `rich`
-  Supports freeing memory by block ID or by process name
-  Summary tables showing memory usage per owner
-  MIT Licensed — simple, clean, and reusable

---

##  Why This Project?

- Useful for **RTOS students**, **embedded engineers**, and anyone curious about **heap allocation strategies**
- Helps visualize memory fragmentation and allocation efficiency
- Great as a **teaching aid**, **interview discussion project**, or personal **learning tool**
- Fully CLI-based and easy to extend

---

## Usage

### Run the main demo

```bash
python3 main.py
```

## Dependencies

- Python 3.8+
- [`rich`](https://github.com/Textualize/rich) for styled terminal output
- [`humanize`](https://github.com/jmoiron/humanize) for readable memory sizes

Install dependencies:

```bash
pip install -r requirements.txt
```
## Contributing

This is a focused educational tool — but PRs are welcome for:

- Improved formatting or UX
- More realistic allocation algorithms
- GUI or web visualization extensions (e.g., with Tkinter or Plotly Dash)


## Related Projects

You might also like:

- [Git Log Analyser](https://github.com/mujasoft/git_log_analyser) – LLM-powered commit analyser
- [Jenkins AI Log Analyser](https://github.com/mujasoft/jenkins_ai_log_analyzer) – Pipeline log chunking + semantic search + analyser

## License

MIT License  
© 2025 [Mujaheed Khan](https://github.com/mujasoft)


