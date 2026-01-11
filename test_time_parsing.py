"""
Test the time parsing functionality for the reminder system
"""

import re

def parse_time_input(time_str):
    """Parse various time input formats into seconds"""
    time_str = time_str.lower().strip()
    
    # Pattern for number + unit (e.g., "5m", "2h", "30s")
    pattern = r'^(\d+)\s*(s|sec|second|seconds|m|min|minute|minutes|h|hr|hour|hours|d|day|days)$'
    match = re.match(pattern, time_str)
    
    if match:
        number = int(match.group(1))
        unit = match.group(2)
        
        # Convert to seconds
        if unit in ['s', 'sec', 'second', 'seconds']:
            return number
        elif unit in ['m', 'min', 'minute', 'minutes']:
            return number * 60
        elif unit in ['h', 'hr', 'hour', 'hours']:
            return number * 3600
        elif unit in ['d', 'day', 'days']:
            return number * 86400
    
    # Try to parse as just minutes if it's a plain number
    try:
        minutes = int(time_str)
        if 1 <= minutes <= 10080:  # 1 minute to 1 week
            return minutes * 60
    except ValueError:
        pass
    
    return None

def format_time_remaining(seconds):
    """Format seconds into human-readable time"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    elif seconds < 86400:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if minutes > 0:
            return f"{hours}h {minutes}m"
        return f"{hours}h"
    else:
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        if hours > 0:
            return f"{days}d {hours}h"
        return f"{days}d"

# Test cases
test_cases = [
    # Valid formats
    ("5m", 300),
    ("2h", 7200),
    ("30s", 30),
    ("1d", 86400),
    ("120", 7200),  # 120 minutes
    ("3 hours", 10800),
    ("10 minutes", 600),
    ("2 days", 172800),
    
    # Invalid formats
    ("abc", None),
    ("5x", None),
    ("", None),
    ("0", None),  # Below minimum
    ("20000", None),  # Above maximum
]

def test_parsing():
    print("🧪 Testing Time Parsing Function\n")
    print("=" * 50)
    
    passed = 0
    total = len(test_cases)
    
    for input_str, expected in test_cases:
        result = parse_time_input(input_str)
        status = "✅" if result == expected else "❌"
        
        if result == expected:
            passed += 1
        
        print(f"{status} '{input_str}' → {result} seconds (expected: {expected})")
    
    print(f"\n{'=' * 50}")
    print(f"📊 Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    # Test formatting
    print(f"\n🎨 Testing Time Formatting:")
    format_tests = [30, 300, 3600, 7200, 86400, 90000]
    
    for seconds in format_tests:
        formatted = format_time_remaining(seconds)
        print(f"   {seconds:>6} seconds → {formatted}")

if __name__ == "__main__":
    test_parsing()