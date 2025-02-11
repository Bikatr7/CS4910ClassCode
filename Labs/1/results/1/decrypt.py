from collections import Counter
import re

SUBSTITUTIONS = {
    'y': 't',
    't': 'h',
    'n': 'e',
    'v': 'a',
    'p': 'd',
    'm': 'i',
    'u': 'n',
    'x': 'o',
    'b': 'f',
    'l': 'w',
    'q': 's',
    'h': 'r',
    'r': 'g',
    'g': 'b',
    'i': 'l',
    'c': 'm',
    'z': 'u',
    'd': 'y',
    'a': 'c',
    'e': 'p',
    'f': 'v',
    's': 'k',
    'k': 'x',
    'j': 'q',
    'o': 'j',
    'w': 'z',
}

## validate the substitutions, ensuring no collisions
def validate_substitutions(subs):
        
    ## ensure each character maps to only one other character
    mapped_chars = set(v for v in subs.values())
    if(len(mapped_chars) != len(subs)):
        raise ValueError("Substitutions are not injective, one or more characters map to multiple others")
    
    ## ensure each character is mapped
    if(len(mapped_chars) != len(subs)):
        raise ValueError("Substitutions are not surjective, one or more characters are not mapped")
    
    ## ensure correct amount of mappings, 26
    if(len(subs) != 26):
        raise ValueError("Incorrect amount of mappings, should be 26, found " + str(len(subs)))

def load_words():
    """Load the English word list"""
    with open('./Labs/1/Files/words.txt', 'r') as f:
        return set(word.strip().lower() for word in f)

def apply_substitutions(text, subs):
    """Apply substitution cipher mappings to text"""
    result = ''
    for char in text.lower():
        result += subs.get(char, char)
    return result

def find_common_patterns(text, length=3):
    """Find common patterns of specified length in text"""
    patterns = []
    for i in range(len(text) - length + 1):
        pattern = text[i:i+length]
        if(pattern.isalpha()):
            patterns.append(pattern)
    return Counter(patterns).most_common(20)

def analyze_unmapped_chars(text, subs):
    """Analyze frequency of characters that haven't been mapped yet"""
    unmapped = []
    for char in text.lower():
        if(char.isalpha() and char not in subs):
            unmapped.append(char)
    return Counter(unmapped).most_common()

def find_possible_words(text, english_words):
    """Find partially decrypted words that might match English words"""
    possible_matches = []
    words = text.split()
    
    for word in words:
        if(not word.isalpha()):
            continue
        
        ## Create pattern where unknown letters are replaced with '.'
        pattern = ''
        unknown_positions = []
        for i, char in enumerate(word):
            if char in SUBSTITUTIONS.values():
                pattern += char
            else:
                pattern += '.'
                unknown_positions.append(i)
        
        pattern = '^' + pattern + '$'
        matches = [w for w in english_words if len(w) == len(word) and re.match(pattern, w)]
        
        if(matches and len(matches) < 5):
            possible_matches.append((word, matches))
    
    return possible_matches

def compare_with_known_plaintext(decrypted_text):
    """Compare decrypted text with known plaintext, ignoring case and non-alphanumeric chars"""
    with open('./Labs/1/results/1/discovered_plaintext.txt', 'r') as f:
        known_plaintext = f.read()
    
    def clean_text(text):
        return ''.join(c.lower() for c in text if c.isalnum())
    
    clean_decrypted = clean_text(decrypted_text)
    clean_known = clean_text(known_plaintext)
    
    print("\n=== Plaintext Comparison ===")
    if(clean_decrypted == clean_known):
        print("Texts match perfectly after cleaning!")
        return
    
    min_len = min(len(clean_decrypted), len(clean_known))
    for i in range(min_len):
        if(clean_decrypted[i] != clean_known[i]):
            start = max(0, i - 20)
            end = min(min_len, i + 20)
            print(f"\nMismatch at position {i}:")
            print(f"Decrypted: ...{clean_decrypted[start:end]}...")
            print(f"Expected:  ...{clean_known[start:end]}...")
            print(f"              {' ' * (i-start)}^")
    
    if(len(clean_decrypted) != len(clean_known)):
        print(f"\nLength mismatch: Decrypted ({len(clean_decrypted)}) vs Expected ({len(clean_known)})")

def main():
    validate_substitutions(SUBSTITUTIONS)

    with open('./Labs/1/Files/ciphertext.txt', 'r') as f:
        ciphertext = f.read()

    english_words = load_words()

    decrypted = apply_substitutions(ciphertext, SUBSTITUTIONS)

    compare_with_known_plaintext(decrypted)
    
    print("=== Complete Decryption ===")
    print(decrypted)
    print("\n=== Substitution Key ===")
    print("Ciphertext -> Plaintext")
    for k, v in sorted(SUBSTITUTIONS.items()):
        print(f"{k} -> {v}")
    print()

    print("=== Unmapped Characters (by frequency) ===")
    unmapped = analyze_unmapped_chars(ciphertext, SUBSTITUTIONS)
    for char, count in unmapped:
        print(f"{char}: {count}")
    print()

    print("=== Common Patterns (3 letters) ===")
    patterns = find_common_patterns(ciphertext)
    for pattern, count in patterns:
        decrypted_pattern = apply_substitutions(pattern, SUBSTITUTIONS)
        print(f"{pattern} ({count}) → {decrypted_pattern}")
    print()

    print("=== Possible Word Matches ===")
    possible_words = find_possible_words(decrypted, english_words)
    for encrypted, matches in possible_words:
        print(f"{encrypted}: {matches}")

if(__name__ == "__main__"):
    main()