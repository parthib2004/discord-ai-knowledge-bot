# 👥 CreoBot Group Reminder System

## Overview
The group reminder system allows you to set reminders for other members in your Discord server. Perfect for team coordination, project management, and ensuring everyone stays on track with important tasks and deadlines.

## Key Features

### 🎯 Team Coordination
- **Set reminders for anyone** in the server
- **Flexible permissions** - both creator and target can cancel
- **Clear attribution** - shows who set each reminder
- **Same time formats** as personal reminders

### 🔧 Smart Management
- **Separate commands** for viewing personal vs group reminders
- **Dual cancellation rights** - creator or target can cancel
- **Unique identification** - each reminder has a unique ID
- **Automatic cleanup** after delivery

## Commands

### Setting Group Reminders
```
/reminduser user:@teammate time:30m message:"Team meeting in 5 minutes"
```

### Viewing Group Reminders
```
/groupreminders          # Reminders you set for others
/reminders              # Reminders set for you (personal + group)
```

### Managing Group Reminders
```
/cancel abc123de        # Cancel any reminder (if you created it or it's for you)
```

## Use Cases

### 🏢 Business & Work
```
/reminduser user:@project_manager time:2h message:"Quarterly review meeting"
/reminduser user:@developer time:1d message:"Code review deadline tomorrow"
/reminduser user:@designer time:4h message:"Client feedback needed on mockups"
```

### 🎮 Gaming Communities
```
/reminduser user:@raid_leader time:30m message:"Guild raid starting soon"
/reminduser user:@tournament_player time:1h message:"Registration closes in 1 hour"
/reminduser user:@event_organizer time:6h message:"Community event setup"
```

### 📚 Study Groups
```
/reminduser user:@study_partner time:45m message:"Study session in library"
/reminduser user:@group_member time:1d message:"Assignment due tomorrow"
/reminduser user:@project_lead time:3h message:"Group presentation practice"
```

### 🎉 Events & Social
```
/reminduser user:@party_host time:2h message:"Party starts at 8 PM"
/reminduser user:@movie_buddy time:30m message:"Movie night in 30 minutes"
/reminduser user:@friend time:1d message:"Birthday party tomorrow"
```

## Permission System

### Who Can Set Group Reminders?
- **Anyone** in the server can set reminders for other members
- **No special permissions** required
- **Cannot set reminders for bots** (system prevents this)

### Who Can Cancel Group Reminders?
- **Reminder Creator**: The person who set the reminder
- **Reminder Target**: The person the reminder is for
- **Both parties** have equal cancellation rights

### Safety Features
- **Bot Protection**: System prevents setting reminders for bots
- **Self-Reminder Detection**: Suggests using `/remind` for self-reminders
- **Input Validation**: Same time limits as personal reminders (10s - 7 days)

## User Experience

### Setting a Group Reminder
When you use `/reminduser`, you'll see:
```
✅ Group Reminder Set
Team meeting in conference room

👤 For: @john
⏱️ Time: 30m
📍 Channel: #general
👨‍💼 Set by: @you
🆔 ID: abc123de

The user will be notified when the reminder triggers
```

### Receiving a Group Reminder
When a group reminder triggers, the target user sees:
```
⏰ Reminder
Team meeting in conference room

👤 For: @john
👨‍💼 Set by: @teammate
Reminder ID: abc123de
```

### Viewing Group Reminders You Created
Using `/groupreminders` shows:
```
👥 Your Group Reminders
You have 2 active group reminder(s)

⏰ Group Reminder 1
For: John Doe
Message: Team meeting in conference room
Time Left: 25m 30s
Channel: #general
ID: abc123de

⏰ Group Reminder 2
For: Sarah Smith
Message: Code review deadline
Time Left: 1h 45m
Channel: #development
ID: def456gh
```

### Canceling Group Reminders
Both creator and target can cancel:
```
🗑️ Group Reminder Cancelled
Team meeting in conference room

👤 Was for: @john
👨‍💼 Set by: @teammate
🗑️ Cancelled by: @john (target)

🆔 Cancelled ID: abc123de
```

## Best Practices

### 🎯 Effective Group Reminders
1. **Be Specific**: Include location, time, or context
   - ✅ "Team meeting in Room 5 at 2 PM"
   - ❌ "Meeting"

2. **Use Appropriate Timing**: Give people enough notice
   - ✅ 30 minutes for meetings
   - ✅ 1-2 hours for deadlines
   - ✅ 1 day for important events

3. **Include Action Items**: Make it clear what they need to do
   - ✅ "Submit your report to Sarah"
   - ✅ "Bring your laptop to the meeting"

### 🤝 Team Coordination
1. **Coordinate with Team**: Don't spam people with reminders
2. **Use Descriptive Messages**: Help people understand the context
3. **Respect Time Zones**: Consider when people will be online
4. **Follow Up**: Check if important reminders were received

### 🔧 Management Tips
1. **Regular Cleanup**: Use `/groupreminders` to check active reminders
2. **Cancel Outdated**: Remove reminders that are no longer needed
3. **Use Unique Messages**: Make it easy to identify different reminders
4. **Note the Channel**: Remember where reminders will be delivered

## Integration with Personal Reminders

### Unified Experience
- **Same time formats** work for both personal and group reminders
- **Same cancellation system** with `/cancel reminder_id`
- **Consistent interface** and embed styling
- **Combined viewing** in `/reminders` command

### Separate Management
- **`/reminders`**: Shows reminders FOR you (personal + group)
- **`/groupreminders`**: Shows reminders you SET for others
- **Clear distinction** between what you receive vs what you create

## Technical Details

### Storage & Performance
- **Memory-based storage** during bot runtime
- **Efficient lookup** by reminder ID
- **Automatic cleanup** after delivery
- **No performance impact** on other bot functions

### Error Handling
- **Invalid users**: Prevents reminding non-existent users
- **Bot protection**: Cannot set reminders for bots
- **Permission validation**: Proper access control
- **Time validation**: Same limits as personal reminders

### Limitations
- **Memory storage**: Reminders reset if bot restarts
- **Server-specific**: Cannot remind users from other servers
- **No recurring**: Each reminder is one-time only
- **Display limit**: Shows max 10 reminders in lists

## Future Enhancements

Potential features for future versions:
- **Persistent database storage**
- **Cross-server reminders**
- **Recurring group reminders**
- **Reminder templates for teams**
- **Bulk reminder operations**
- **Integration with calendar systems**
- **Reminder approval system**
- **Team reminder statistics**

## Troubleshooting

### Common Issues

**"Cannot set reminders for bots"**
- This is intentional - bots don't need reminders
- Use `/remind` for yourself or `/reminduser` for human users

**"You can only cancel your own reminders"**
- For group reminders, both creator and target can cancel
- Make sure you're using the correct reminder ID

**"Reminder not found"**
- Check the reminder ID spelling
- Reminder may have already triggered or been cancelled
- Use `/groupreminders` to see active reminders you created

### Getting Help
- Use `/help` to see all reminder commands
- Check `/reminders` and `/groupreminders` to see active reminders
- Reminder IDs are shown when you create reminders

---

**Ready to coordinate your team?** Try your first group reminder:
```
/reminduser user:@teammate time:5m message:"Test group reminder - it works!"
```