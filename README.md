# Python File Sorter & Parallel Factorizer

This repository contains two independent Python projects demonstrating basic multithreading and multiprocessing concepts:

1. **File Sorter** — Organizes files from a source "junk" folder into a structured target folder by file extensions using multithreading.
2. **Factorizer** — Finds all divisors for a list of numbers using both synchronous and multiprocessing (parallel) approaches.

---

## Projects Overview

### 1. File Sorter (Threading)

Organizes a messy directory (`source/`) into a well-structured folder (`dist/`) by sorting files into subfolders based on their extensions.

- Uses Python's `threading` module for concurrent file operations.
- Handles non-existent or nested folders.
- Can be easily extended to process large folders faster.

> Located in: `file_sorter.py`

### 2. Factorizer (Multiprocessing)

Calculates the divisors (factors) of given integers in two ways:

- **Synchronous Version** — Basic iteration.
- **Parallel Version** — Uses `multiprocessing.Pool` to utilize all CPU cores.

Includes:
- Execution time comparison
- Logging from each process
- Optional support for command-line arguments

> Located in: `factorize_numbers.py`

---

## Requirements

- Python 3.10+
- No external libraries (uses only built-in modules)

---

## How to Run

```bash
# Synchronous and Parallel factorization
python factorize_numbers.py

# With your own numbers (optional)
python factorize_numbers.py 100 256 999999

# File sorting (run and provide paths as needed)
python file_sorter.py
