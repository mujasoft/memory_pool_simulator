# Memory Pool Simulator (Fixed & Variable Block Sizes)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen)
![Demo](https://img.shields.io/badge/demo-available-brightgreen)

A lightweight, terminal-based simulator that demonstrates how memory allocation works using both **fixed-size** and **variable-size** block strategies. Perfect for visual learners and systems programmers — I wish I had a tool like this when I was starting out!

## Demo
![Demo of the tool](demo.gif)

---

## Features

- **FixedBlockSizeMemoryPool**
  - Allocates memory using equal-sized blocks
- **VariableBlockSizeMemoryPool**
  - Allocates memory using tiered sizes (e.g., GB, MB, KB)
- **Rich terminal visualizations** powered by `rich`
-  System Summary Tables
-  MIT Licensed — simple, clean, and reusable

---

##  Why This Project?

- Useful for **RTOS students**, **embedded engineers**, and anyone curious about **heap allocation strategies**
- Helps visualize memory fragmentation and allocation efficiency
- Great as a **teaching aid**, **interview discussion project**, or personal **learning tool**

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
pip3 install -r requirements.txt
```
## Contributing

This is a focused educational tool — but PRs are welcome for:

- Improved formatting or UX
- More realistic allocation algorithms


## Related Projects

You might also like:

- [Git Log Analyser](https://github.com/mujasoft/git_log_analyser) – LLM-powered commit analyser
- [Jenkins AI Log Analyser](https://github.com/mujasoft/jenkins_ai_log_analyzer) – Pipeline log chunking + semantic search + analyser

## License

MIT License  
© 2025 [Mujaheed Khan](https://github.com/mujasoft)


