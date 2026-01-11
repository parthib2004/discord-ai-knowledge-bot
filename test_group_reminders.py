"""
CreoBot Group Reminder System Examples
======================================

This file shows examples of how the new group reminder system works.
"""

# Example group reminder commands users can run:

GROUP_REMINDER_EXAMPLES = [
    {
        "command": "/reminduser",
        "user": "@john",
        "time": "30m",
        "message": "Team meeting in conference room",
        "description": "Remind team member about meeting"
    },
    {
        "command": "/reminduser",
        "user": "@sarah",
        "time": "2h",
        "message": "Code review deadline",
        "description": "Remind colleague about deadline"
    },
    {
        "command": "/reminduser",
        "user": "@mike",
        "time": "1d",
        "message": "Submit weekly report",
        "description": "Daily reminder for reports"
    },
    {
        "command": "/reminduser",
        "user": "@team_lead",
        "time": "15m",
        "message": "Client call in 5 minutes",
        "description": "Urgent meeting reminder"
    },
    {
        "command": "/reminduser",
        "user": "@designer",
        "time": "4h",
        "message": "Design review feedback needed",
        "description": "Project collaboration reminder"
    }
]

MANAGEMENT_EXAMPLES = [
    {
        "command": "/groupreminders",
        "description": "View all reminders you've set for others"
    },
    {
        "command": "/reminders", 
        "description": "View reminders set for you (personal + group)"
    },
    {
        "command": "/cancel abc123de",
        "description": "Cancel a reminder (works for both personal and group)"
    }
]

def print_examples():
    print("👥 CreoBot Group Reminder System Examples\n")
    print("=" * 60)
    
    print("\n📝 Group Reminder Commands:")
    for i, example in enumerate(GROUP_REMINDER_EXAMPLES, 1):
        print(f"\n{i}. {example['description']}")
        full_cmd = f"/reminduser user:{example['user']} time:{example['time']} message:\"{example['message']}\""
        print(f"   Command: {full_cmd}")
    
    print(f"\n{'=' * 60}")
    print("🔧 Management Commands:")
    for example in MANAGEMENT_EXAMPLES:
        print(f"• {example['command']} - {example['description']}")
    
    print(f"\n{'=' * 60}")
    print("🎯 Group Reminder Features:")
    print("✅ Set reminders for any server member")
    print("✅ Same flexible time formats (5m, 2h, 30s, 1d)")
    print("✅ Both creator and target can cancel")
    print("✅ Shows who set the reminder")
    print("✅ Separate management commands")
    print("✅ Beautiful embed notifications")
    print("✅ Prevents setting reminders for bots")
    print("✅ Suggests using /remind for self-reminders")
    print("✅ Channel-specific delivery")
    print("✅ Unique IDs for easy management")
    
    print(f"\n🔐 Permission System:")
    print("• Anyone can set reminders for others")
    print("• Reminder creator can cancel their group reminders")
    print("• Reminder target can cancel reminders set for them")
    print("• Cannot set reminders for bots")
    print("• Suggests /remind for self-reminders")
    
    print(f"\n💡 Use Cases:")
    print("🏢 Team Coordination:")
    print("  • Meeting reminders for colleagues")
    print("  • Deadline notifications")
    print("  • Task follow-ups")
    
    print("🎮 Gaming & Events:")
    print("  • Raid reminders for guild members")
    print("  • Tournament notifications")
    print("  • Event coordination")
    
    print("📚 Study Groups:")
    print("  • Assignment due dates")
    print("  • Study session reminders")
    print("  • Group project deadlines")
    
    print(f"\n📱 What Users See:")
    print("When setting a group reminder:")
    print("✅ Group Reminder Set")
    print("Team meeting in conference room")
    print("👤 For: @john")
    print("⏱️ Time: 30m")
    print("📍 Channel: #general")
    print("👨‍💼 Set by: @you")
    print("🆔 ID: abc123de")
    
    print("\nWhen receiving a group reminder:")
    print("⏰ Reminder")
    print("Team meeting in conference room")
    print("👤 For: @john")
    print("👨‍💼 Set by: @you")

if __name__ == "__main__":
    print_examples()