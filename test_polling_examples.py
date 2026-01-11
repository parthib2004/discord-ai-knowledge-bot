"""
CreoBot Polling System Examples
===============================

This file shows examples of how the new polling system works.
"""

# Example poll commands users can run:

POLL_EXAMPLES = [
    {
        "command": "/poll",
        "question": "What's your favorite programming language?",
        "options": "Python, JavaScript, Java, C++, Go",
        "duration": 60,
        "description": "Multi-option poll with 5 choices"
    },
    {
        "command": "/poll", 
        "question": "When should we have the team meeting?",
        "options": "Monday 9AM, Tuesday 2PM, Wednesday 10AM, Thursday 3PM",
        "duration": 120,
        "description": "Meeting scheduling poll"
    },
    {
        "command": "/quickpoll",
        "question": "Should we order pizza for lunch?",
        "duration": 30,
        "description": "Simple Yes/No decision"
    },
    {
        "command": "/quickpoll",
        "question": "Is the new feature ready for deployment?",
        "duration": 15,
        "description": "Quick team decision"
    }
]

def print_examples():
    print("🗳️  CreoBot Polling System Examples\n")
    print("=" * 50)
    
    for i, example in enumerate(POLL_EXAMPLES, 1):
        print(f"\n{i}. {example['description']}")
        print(f"   Command: {example['command']}")
        print(f"   Question: \"{example['question']}\"")
        
        if 'options' in example:
            print(f"   Options: \"{example['options']}\"")
        
        print(f"   Duration: {example['duration']} minutes")
        
        # Show full command
        if example['command'] == '/poll':
            full_cmd = f"/poll question:\"{example['question']}\" options:\"{example['options']}\" duration:{example['duration']}"
        else:
            full_cmd = f"/quickpoll question:\"{example['question']}\" duration:{example['duration']}"
        
        print(f"   Full Command: {full_cmd}")
    
    print(f"\n{'=' * 50}")
    print("🎯 Polling Features:")
    print("✅ Multi-option polls (2-10 options)")
    print("✅ Quick Yes/No polls")
    print("✅ Automatic vote counting")
    print("✅ Visual progress bars")
    print("✅ Timed duration (10 sec - 24 hours)")
    print("✅ Results with rankings (🥇🥈🥉)")
    print("✅ Emoji-based voting")
    print("✅ Auto-end with results")

if __name__ == "__main__":
    print_examples()