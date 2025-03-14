# Anagram Solver

A command-line tool to find anagrams from a given set of letters, with some features like excluding known words and generating sentences.

## Features
- Find all possible anagrams from input letters
- Exclude specific words to focus on remaining letters
- Set a minimum word length
- Display remaining letters after exclusions
- Generate sentences:
  - Partial match (up to 3 words)
  - Full match (uses all remaining letters exactly)

## Installation
1. Ensure Python 3.x is installed.
2. Clone or download this repository.
3. Provide a word list file (e.g., `words.txt`), one word per line. Common sources:
   - `/usr/share/dict/words` on Unix systems
   - Download from [english-words](https://github.com/dwyl/english-words)
   - Also already included in the demo wordlist folder.

## Usage
```bash
python anagram_solver.py LETTERS -w WORDLIST [OPTIONS]
