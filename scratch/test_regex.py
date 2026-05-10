import re

def test_regex():
    # Simulated ia_filterdb logic
    query = "haal"
    words = query.split()
    # Case 1: My previous broken one
    raw_pattern_broken = r'^' + r''.join(f'(?=.*\b{re.escape(word)}\b)' for word in words)
    # Case 2: My new one with \\b
    raw_pattern_fixed = r'^' + r''.join(f'(?=.*\\b{re.escape(word)}\\b)' for word in words)
    
    print(f"Broken pattern: {repr(raw_pattern_broken)}")
    print(f"Fixed pattern: {repr(raw_pattern_fixed)}")
    
    test_string = "Haal.2024.Malayalam.mkv"
    
    try:
        regex_broken = re.compile(raw_pattern_broken, flags=re.IGNORECASE)
        print(f"Broken match: {bool(regex_broken.match(test_string))}")
    except Exception as e:
        print(f"Broken error: {e}")
        
    try:
        regex_fixed = re.compile(raw_pattern_fixed, flags=re.IGNORECASE)
        print(f"Fixed match: {bool(regex_fixed.match(test_string))}")
    except Exception as e:
        print(f"Fixed error: {e}")

if __name__ == "__main__":
    test_regex()
