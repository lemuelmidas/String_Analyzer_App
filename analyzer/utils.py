import hashlib
from collections import Counter

def analyze_string(text):
    clean_text = text.strip()
    return {
        'length': len(clean_text),
        'is_palindrome': clean_text.lower() == clean_text[::-1].lower(),
        'unique_characters': len(set(clean_text)),
        'word_count': len(clean_text.split()),
        'sha256_hash': hashlib.sha256(clean_text.encode()).hexdigest(),
        'character_frequency_map': dict(Counter(clean_text))
    }