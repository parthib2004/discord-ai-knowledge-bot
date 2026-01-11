# ⏰ CreoBot Reminder System

## Overview
CreoBot includes a comprehensive reminder system that helps you stay organized and coordinate with your team. Set personal reminders for yourself or group reminders for other members to ensure everyone stays on track.

## Commands

### `/remind` - Set a Personal Reminder
Create a personal reminder that will be delivered to you after a specified time.

**Syntax:**
```
/remind time:"5m" message:"Your reminder message"
```

**Parameters:**
- `time` (required): When to remind you (see time formats below)
- `message` (required): What to remind you about

**Examples:**
```
/remind time:5m message:"Check the server status"
/remind time:2h message:"Team meeting in conference room"
/remind time:30s message:"Test reminder"
/remind time:1d message:"Submit weekly report"
```

### `/reminduser` - Set a Group Reminder
Create a reminder for another user in the server. Great for team coordination!

**Syntax:**
```
/reminduser user:@username time:"30m" message:"Your reminder message"
```

**Parameters:**
- `user` (required): The Discord user to remind (use @mention or select from dropdown)
- `time` (required): When to remind them (same formats as personal reminders)
- `message` (required): What to remind them about

**Examples:**
```
/reminduser user:@john time:30m message:"Team meeting in conference room"
/reminduser user:@sarah time:2h message:"Code review deadline"
/reminduser user:@mike time:1d message:"Submit weekly report"
```

### `/reminders` - View Your Personal Reminders
See all reminders set for you (both personal and group reminders others set for you).

**Syntax:**
```
/reminders
```

### `/groupreminders` - View Group Reminders You Created
See all reminders you've set for other users.

**Syntax:**
```
/groupreminders
```

### `/cancel` - Cancel a Reminder
Cancel a specific reminder using its ID. Works for both personal and group reminders.

**Syntax:**
```
/cancel reminder_id
```

**Permissions:**
- **Personal reminders**: Only you can cancel
- **Group reminders**: Both creator and target can cancel

**Example:**
```
/cancel abc123de
```

## Time Formats

### Supported Units
| Format | Unit | Example | Description |
|--------|------|---------|-------------|
| `s`, `sec`, `second`, `seconds` | Seconds | `30s` | 30 seconds |
| `m`, `min`, `minute`, `minutes` | Minutes | `5m` | 5 minutes |
| `h`, `hr`, `hour`, `hours` | Hours | `2h` | 2 hours |
| `d`, `day`, `days` | Days | `1d` | 1 day |

### Format Examples
```
5m          → 5 minutes
2h          → 2 hours  
30s         → 30 seconds
1d          → 1 day
45          → 45 minutes (plain number)
3 hours     → 3 hours (with space)
10 minutes  → 10 minutes (full word)
2 days      → 2 days (full word)
```

### Time Limits
- **Minimum**: 10 seconds
- **Maximum**: 7 days (604,800 seconds)
- **Plain Numbers**: Interpreted as minutes (1-10,080 range)

## Features

### 🎯 Personal & Group Reminders
- **Personal Reminders**: Set reminders for yourself with `/remind`
- **Group Reminders**: Set reminders for other users with `/reminduser`
- **Flexible Management**: View and cancel both types of reminders
- **Smart Permissions**: Both creator and target can cancel group reminders

### 🔧 Smart Management
- **Unique IDs**: Each reminder gets a unique 8-character ID
- **Separate Views**: `/reminders` for personal, `/groupreminders` for ones you created
- **Easy Cancellation**: Cancel any reminder with `/cancel id`
- **Auto-Cleanup**: Completed reminders are automatically removed

### 📱 Beautiful Display
- **Rich Embeds**: Professional-looking reminder notifications
- **Creator Attribution**: Group reminders show who set them
- **Time Formatting**: Human-readable time remaining (5m, 2h 30m, 1d 5h)
- **Status Indicators**: Clear confirmation when setting/canceling
- **Organized Lists**: Clean display of multiple reminders

### ⚡ Reliable Delivery
- **Channel-Specific**: Delivered in the channel where they were set
- **User Mentions**: Target users get pinged when reminders trigger
- **Async Processing**: Non-blocking reminder scheduling
- **Error Handling**: Graceful handling of edge cases
- **Accurate Timing**: Precise delivery at scheduled time

### 🛡️ Safety Features
- **Bot Protection**: Cannot set reminders for bots
- **Self-Reminder Suggestion**: Suggests `/remind` when trying to remind yourself
- **Permission Validation**: Proper access control for cancellation
- **Input Validation**: Prevents invalid time formats and ranges

## Example Workflows

### 🏢 Work Reminders (Personal)
```
/remind time:30m message:"Stand-up meeting in 5 minutes"
/remind time:2h message:"Code review deadline"
/remind time:1d message:"Submit timesheet"
```

### 👥 Team Coordination (Group)
```
/reminduser user:@john time:30m message:"Team meeting in conference room"
/reminduser user:@sarah time:2h message:"Code review deadline"
/reminduser user:@mike time:1d message:"Submit weekly report"
```

### 🎮 Gaming & Events
```
/reminduser user:@guild_leader time:15m message:"Raid starts soon - get ready!"
/reminduser user:@team_captain time:1h message:"Tournament registration closes"
```

### 📚 Study & Learning
```
/reminduser user:@study_buddy time:25m message:"Break time - Pomodoro session"
/reminduser user:@project_partner time:3h message:"Review today's notes"
```

### 🍕 Personal Tasks
```
/remind time:10m message:"Check the oven"
/remind time:45m message:"Call mom"
/remind time:6h message:"Take evening medication"
```

## Reminder Notifications

When a reminder triggers, you'll see:

```
⏰ Reminder
Your reminder message here

👤 For: @YourUsername
Reminder ID: abc123de
```

## Management Examples

### View All Reminders
```
📝 Your Active Reminders
You have 3 active reminder(s)

⏰ Reminder 1
Message: Check the server status
Time Left: 3m 45s
Channel: #general
ID: abc123de

⏰ Reminder 2  
Message: Team meeting in conference room
Time Left: 1h 23m
Channel: #work
ID: def456gh
```

### Cancel a Reminder
```
🗑️ Reminder Cancelled
Team meeting in conference room

🆔 Cancelled ID: def456gh
```

## Error Handling

### Invalid Time Format
```
❌ Invalid Time Format

Valid formats:
• 5m or 5 minutes
• 2h or 2 hours  
• 30s or 30 seconds
• 1d or 1 day
• 120 (plain number = minutes)
```

### Time Out of Range
```
❌ Error: Minimum reminder time is 10 seconds.
❌ Error: Maximum reminder time is 7 days.
```

### Reminder Not Found
```
❌ Error: Reminder abc123de not found.
```

### Permission Error
```
❌ Error: You can only cancel your own reminders.
```

## Tips for Best Results

### 🎯 Writing Good Reminders
1. **Be Specific**: "Team meeting in Room 5" vs "Meeting"
2. **Include Context**: "Submit Q4 report to Sarah" vs "Submit report"
3. **Use Action Words**: "Call", "Check", "Submit", "Review"
4. **Keep It Short**: Messages over 50 chars are truncated in lists

### ⏰ Timing Strategy
1. **Buffer Time**: Set reminders 5-10 minutes before actual deadlines
2. **Multiple Reminders**: Set both early warning and final reminders
3. **Reasonable Intervals**: Don't spam yourself with too many reminders
4. **Consider Context**: Set work reminders during work hours

### 🔧 Management Best Practices
1. **Regular Cleanup**: Check `/reminders` periodically
2. **Cancel Outdated**: Remove reminders that are no longer needed
3. **Use Descriptive Messages**: Make it easy to identify reminders
4. **Note the Channel**: Remember where reminders will be delivered

## Technical Details

### Storage
- Reminders are stored in memory during bot runtime
- For production use, consider implementing database storage
- Reminders are lost if the bot restarts (temporary limitation)

### Performance
- Lightweight async implementation
- No impact on other bot functions
- Efficient memory usage with automatic cleanup

### Limitations
- Maximum 10 reminders shown in `/reminders` (all still work)
- Memory-based storage (not persistent across restarts)
- Personal reminders only (no group reminders yet)

## Future Enhancements

Potential features for future versions:
- Persistent database storage
- Recurring reminders (daily, weekly, monthly)
- Group reminders for teams
- Reminder templates
- Snooze functionality
- Integration with calendar systems
- Reminder statistics and analytics

---

**Ready to stay organized?** Try your first reminder:
```
/remind time:1m message:"Test reminder - it works!"
```