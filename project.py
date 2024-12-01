import hashlib
import itertools
from datetime import datetime, timedelta
import time
import string

def hash_password(password):
    return hashlib.sha1(str(password).encode()).hexdigest()

def load_passwords(filename):
    passwords = {}
    with open(filename, 'r') as f:
        for line in f:
            user_id, hash_value = line.strip().split()
            passwords[user_id] = hash_value
    return passwords

def load_dictionary(filename):
    with open(filename, 'r') as f:
        return [word.strip().lower() for word in f]

def get_leet_variations(text):
    leet_chars = {
        'a': ['@', '4', '/\\'],
        'b': ['8', '6', '13'],
        'e': ['3'],
        'g': ['9', '6'],
        'i': ['1', '!', '|'],
        'l': ['1', '|', '7'],
        'o': ['0', '()'],
        's': ['5', '$', 'z'],
        't': ['7', '+'],
        'z': ['2']
    }
    
    results = {text}
    chars_to_replace = [c for c in text.lower() if c in leet_chars]
    for num_chars in range(1, min(4, len(chars_to_replace) + 1)):
        for chars in itertools.combinations(chars_to_replace, num_chars):
            current = text.lower()
            for char in chars:
                for replacement in leet_chars[char]:
                    current = current.replace(char, replacement)
                    results.add(current)
    return list(results)[:50]

def try_numeric_patterns(passwords, found):
    for length in range(3, 9):
        for i in range(10 ** length):
            password = str(i).zfill(length)
            hash_value = hash_password(password)
            for user_id, stored_hash in passwords.items():
                if user_id not in found and hash_value == stored_hash:
                    found[user_id] = password
                    print(f"Found: User {user_id} = {password}")

    for area in range(100, 1000):
        for number in range(0, 10000, 10):
            patterns = [f"{area}{number:04d}", f"{area}-{number:04d}"]
            for pattern in patterns:
                hash_value = hash_password(pattern)
                for user_id, stored_hash in passwords.items():
                    if user_id not in found and hash_value == stored_hash:
                        found[user_id] = pattern
                        print(f"Found: User {user_id} = {pattern}")

def try_advanced_dates(passwords, found):
    for year in range(1950, 2025):
        year_str = str(year)
        year_short = year_str[2:]
        
        for month in range(1, 13):
            month_str = str(month).zfill(2)
            month_name = datetime(2000, month, 1).strftime('%b').lower()
            
            for day in range(1, 32):
                day_str = str(day).zfill(2)
                formats = [
                    f"{year}{month_str}{day_str}",
                    f"{day_str}{month_str}{year}",
                    f"{month_str}{day_str}{year}",
                    f"{year_short}{month_str}{day_str}",
                    f"{day_str}{month_str}{year_short}",
                    f"{month_name}{year_short}"
                ]
                
                for date_format in formats:
                    hash_value = hash_password(date_format)
                    for user_id, stored_hash in passwords.items():
                        if user_id not in found and hash_value == stored_hash:
                            found[user_id] = date_format
                            print(f"Found: User {user_id} = {date_format}")

def try_word_variations(passwords, dictionary_words, found):
    short_numbers = [str(i).zfill(2) for i in range(100)]
    medium_numbers = [str(i) for i in range(1000) if len(str(i)) <= 3]
    years = [str(i) for i in range(1950, 2025)]
    
    for word in dictionary_words:
        if len(word) <= 10:
            base_variations = get_leet_variations(word)
            base_variations.extend([
                word,
                word.capitalize(),
                word.upper(),
                word.title(),
                word[::-1],
                word + word
            ])
            
            for variation in base_variations:
                hash_value = hash_password(variation)
                for user_id, stored_hash in passwords.items():
                    if user_id not in found and hash_value == stored_hash:
                        found[user_id] = variation
                        print(f"Found: User {user_id} = {variation}")
                
                if len(variation) <= 8:
                    for num in short_numbers + medium_numbers + years:
                        if len(variation) + len(num) <= 12:
                            patterns = [f"{variation}{num}", f"{num}{variation}"]
                            for pattern in patterns:
                                hash_value = hash_password(pattern)
                                for user_id, stored_hash in passwords.items():
                                    if user_id not in found and hash_value == stored_hash:
                                        found[user_id] = pattern
                                        print(f"Found: User {user_id} = {pattern}")

def try_word_combinations(passwords, dictionary_words, found):
    short_words = [w for w in dictionary_words if len(w) <= 6]
    very_short_words = [w for w in dictionary_words if len(w) <= 4]
    prefixes = ['my', 'the', 'a', 'i', 'you', 'our', 'his', 'her']
    
    for word1 in short_words:
        for word2 in short_words[:500]:
            if len(word1) + len(word2) <= 12:
                combo = word1 + word2
                hash_value = hash_password(combo)
                for user_id, stored_hash in passwords.items():
                    if user_id not in found and hash_value == stored_hash:
                        found[user_id] = combo
                        print(f"Found: User {user_id} = {combo}")
    
    for prefix in prefixes:
        for word in dictionary_words:
            if len(prefix) + len(word) <= 12:
                combo = prefix + word
                hash_value = hash_password(combo)
                for user_id, stored_hash in passwords.items():
                    if user_id not in found and hash_value == stored_hash:
                        found[user_id] = combo
                        print(f"Found: User {user_id} = {combo}")
    
    for word1 in short_words[:1000]:
        partial1 = word1[:4]
        for word2 in short_words[:1000]:
            partial2 = word2[:4]
            if len(partial1) + len(partial2) <= 8:
                for num in range(100):
                    combo = f"{partial1}{partial2}{num:02d}"
                    hash_value = hash_password(combo)
                    for user_id, stored_hash in passwords.items():
                        if user_id not in found and hash_value == stored_hash:
                            found[user_id] = combo
                            print(f"Found: User {user_id} = {combo}")

def main():
    start_time = time.time()
    max_runtime = 8 * 60 * 60  
    
    passwords = load_passwords('passwords.txt')
    dictionary_words = load_dictionary('dictionary.txt')
    found = {}
    
    print("Starting password cracking ...")
    
    strategies = [
        try_numeric_patterns,
        try_advanced_dates,
        lambda p, f: try_word_variations(p, dictionary_words, f),
        lambda p, f: try_word_combinations(p, dictionary_words, f)
    ]
    
    for strategy in strategies:
        if time.time() - start_time < max_runtime:
            strategy_start = time.time()
            strategy(passwords, found)
            print(f"\nPasswords found so far: {len(found)} out of {len(passwords)}")
            print(f"Time elapsed: {(time.time() - start_time) / 60:.1f} minutes")
        else:
            print("\nTime limit reached!")
            break
    
    print("\nFinal Results:")
    print("=============")
    for user_id in sorted(found.keys(), key=lambda x: int(x)):
        print(f"User {user_id}: {found[user_id]}")
    
    print(f"\nTotal passwords cracked: {len(found)} out of {len(passwords)}")
    print("Remaining uncracked users:", sorted(set(passwords.keys()) - set(found.keys())))
    print(f"Total runtime: {(time.time() - start_time) / 60:.1f} minutes")

if __name__ == "__main__":
    main()
