import argparse
from collections import Counter
import random

ABOUT_TEXT = """
Anagram Finder
Version: 1.0
Created: March 14, 2025
Author: [@asymmetry1]
Description: A command-line tool to find anagrams from given letters, with options to exclude words, set minimum word length, and generate sentences (partial or full-match).
Dependencies: Python 3.12.8
License: MIT
"""

def load_word_list(filename):
    """load words from a file"""
    try:
        with open(filename, 'r') as file:
            return set(word.strip().lower() for word in file)
    except FileNotFoundError:
        print(f"Error: Word list file '{filename}' nor found.")
        exit(1)

def subtract_letters(letter_count, word):
    """subtract letters of a word from letters counter"""
    word_count = Counter(word.lower())
    remaining = letter_count.copy()
    for char in word_count:
        if char in remaining:
            remaining[char] -= word_count[char]
            if remaining[char] <= 0:
                del remaining[char]
            if remaining[char] < 0:
                raise ValueError(f"Word '{word}' uses more '{char}' than available")
    return remaining

def is_valid_anagram(letters_count, word):
    """check if word can be formed"""
    word_count = Counter(word)
    return all(word_count[char] <= letters_count.get(char, 0) for char in word_count)

def find_anagrams(letters, word_list, min_length=1, exclude_words=None):
    """Find all anagrams possible from the given letters."""
    letters = letters.replace(" ", "").lower()
    letters_count = Counter(letters)
    
    # Subtract excluded words if provided
    if exclude_words:
        for word in exclude_words:
            try:
                letters_count = subtract_letters(letters_count, word)
            except ValueError as e:
                print(f"Error: {e}")
                return [], letters_count
    
    anagrams = []
    for word in word_list:
        if (len(word) <= sum(letters_count.values()) and 
            len(word) >= min_length and 
            is_valid_anagram(letters_count, word)):
            anagrams.append(word)
    
    return sorted(anagrams, key=lambda x: (-len(x), x)), letters_count

def generate_sentence(anagrams, remaining_letters, full_match=False):
    """Generate a sentence from available anagrams."""
    if not anagrams:
        return "No sentence possible."
    
    available_words = sorted(anagrams, key=len, reverse=True)
    sentence_words = []
    used_letters = Counter()
    
    if full_match:
        # Try to find combinations that use all remaining letters exactly
        target_count = remaining_letters.copy()
        def find_full_match(words, current_words, remaining):
            if not remaining and current_words:
                return current_words
            if not words:
                return None
            for i, word in enumerate(words):
                word_count = Counter(word)
                if all(word_count[c] <= remaining.get(c, 0) for c in word_count):
                    new_remaining = subtract_letters(remaining, word)
                    result = find_full_match(words[i+1:], current_words + [word], new_remaining)
                    if result:
                        return result
            return None
        
        result = find_full_match(available_words, [], target_count)
        if result:
            sentence_words = result
        else:
            return "No full-match sentence possible."
    else:
        # Original mode: use up to 3 words without requiring all letters
        for word in available_words:
            word_count = Counter(word)
            if all((used_letters[char] + word_count[char]) <= remaining_letters.get(char, 0) 
                   for char in word_count):
                sentence_words.append(word)
                used_letters.update(word_count)
            if len(sentence_words) >= 3:
                break
    
    if not sentence_words:
        return "No sentence possible."
    
    # Construct sentence
    if len(sentence_words) == 1:
        return sentence_words[0].capitalize() + "."
    elif len(sentence_words) == 2:
        return f"{sentence_words[0].capitalize()} {sentence_words[1]}."
    else:
        return f"{sentence_words[0].capitalize()} {' '.join(sentence_words[1:])}."

def main():
    parser = argparse.ArgumentParser(
        description="Find anagrams from given letters.",
        epilog="Use --about for more information."
    )
    parser.add_argument(
        "letters",
        nargs="?",
        help="Input Letters to find anagrams"
    )
    parser.add_argument(
        "-w", "--wordlist",
        help="Path to wordlist file."
    )
    parser.add_argument(
        "-m", "--min-length",
        type=int,
        default=1,
        help="Minimum length of words to find (default: 1)"
    )
    parser.add_argument(
        "-e", "--exclude",
        nargs='+',
        help="Words to exclude from the letters before finding anagrams."
    )
    parser.add_argument(
        "-s", "--sentence",
        action="store_true",
        help="Generate a sentence from found anagrams (partial match)"
    )
    parser.add_argument(
        "-f", "--full-sentence",
        action="store_true",
        help="Generate a sentence using all remaining letters exactly"
    )
    parser.add_argument(
        "--about",
        action="store_true",
        help="Display information about this tool."
    )
    
    args = parser.parse_args()

    #--about
    if args.about:
        print(ABOUT_TEXT)
        return
    
    if not args.letters or not args.wordlist:
        parser.error("Both 'letters' and '--wordlist' are required unless using --about")

    #Load wordlist
    word_list = load_word_list(args.wordlist)
    #find anagram and remaining letters
    anagrams, remaining_letters = find_anagrams(args.letters, word_list, args.min_length, args.exclude)

    #Display remaining letters
    if args.exclude:
        print(f"\nAfter excluding: {' '.join(args.exclude)}")
        remaining_str = ''.join(f"{char}({count})" if count > 1 else char 
                              for char, count in sorted(remaining_letters.items()))
        print(f"Remaining letters: {remaining_str if remaining_str else 'none'}")

    #Display result
    if anagrams:
        print(f"\nFound {len(anagrams)} anagrams:")
        if args.exclude:
            print(f"(After excluding: {' '.join(args.exclude)})")
        for anagram in anagrams:
            print(anagram)    
    else:
        print("No anagrams found.")

    # Generate and display sentence
    if args.sentence or args.full_sentence:
        mode = "Full-match" if args.full_sentence else "Partial"
        sentence = generate_sentence(anagrams, remaining_letters, full_match=args.full_sentence)
        print(f"\n{mode} sentence: {sentence}")

if __name__ == "__main__":
    main()
