"""
CreoBot Reminder System Examples
================================

This file shows examples of how the new reminder system works.
"""

# Example reminder commands users can run:

REMINDER_EXAMPLES = [
    {
        "command": "/remind",
        "time": "5m",
        "message": "Check the server status",
        "description": "5-minute reminder"
    },
    {
        "command": "/remind",
        "time": "2h",
        "message": "Team meeting in conference room",
        "description": "2-hour reminder"
    },
    {
        "command": "/remind",
        "time": "30s",
        "message": "Test reminder",
        "description": "30-second test"
    },
    {
        "command": "/remind",
        "time": "1d",
        "message": "Submit weekly report",
        "description": "Daily reminder"
    },
    {
        "command": "/remind",
        "time": "120",
        "message": "Lunch break",
        "description": "Plain number (minutes)"
    }
]

TIME_FORMAT_EXAMPLES = [
    ("5m", "5 minutes"),
    ("2h", "2 hours"),
    ("30s", "30 seconds"),
    ("1d", "1 day"),
    ("45", "45 minutes (plain number)"),
    ("3 hours", "3 hours (with space)"),
    ("10 minutes", "10 minutes (full word)"),
    ("2 days", "2 days (full word)")
]

def print_examples():
    print("⏰ CreoBot Reminder System Examples\n")
    print("=" * 50)
    
    print("\n📝 Basic Reminder Commands:")
    for i, example in enumerate(REMINDER_EXAMPLES, 1):
        print(f"\n{i}. {example['description']}")
        full_cmd = f"/remind time:{example['time']} message:\"{example['message']}\""
        print(f"   Command: {full_cmd}")
    
    print(f"\n{'=' * 50}")
    print("⏱️ Time Format Examples:")
    for time_format, description in TIME_FORMAT_EXAMPLES:
        print(f"   {time_format:<12} → {description}")
    
    print(f"\n{'=' * 50}")
    print("🎯 Reminder Features:")
    print("✅ Flexible time formats (5m, 2h, 30s, 1d)")
    print("✅ Plain numbers default to minutes")
    print("✅ Range: 10 seconds to 7 days")
    print("✅ Personal reminders (only you see them)")
    print("✅ Unique reminder IDs for management")
    print("✅ View all active reminders")
    print("✅ Cancel reminders by ID")
    print("✅ Beautiful embed notifications")
    print("✅ Channel-specific delivery")
    print("✅ Automatic cleanup after delivery")
    
    print(f"\n🔧 Management Commands:")
    print("• `/reminders` - View all your active reminders")
    print("• `/cancel abc123de` - Cancel reminder by ID")
    
    print(f"\n💡 Usage Tips:")
    print("• Reminders are personal - only you receive them")
    print("• They're delivered in the channel where you set them")
    print("• Use short, clear messages for best results")
    print("• IDs are shown when you create reminders")
    print("• Maximum 10 reminders shown in `/reminders` command")

if __name__ == "__main__":
    print_examples()