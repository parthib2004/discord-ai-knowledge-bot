# 🗳️ CreoBot Polling System

## Overview
CreoBot now includes a powerful polling and voting system that makes it easy to gather opinions and make decisions in your Discord server.

## Commands

### `/poll` - Multi-Option Polls
Create polls with 2-10 custom options.

**Syntax:**
```
/poll question:"Your question here" options:"Option1, Option2, Option3" duration:60
```

**Parameters:**
- `question` (required): The poll question
- `options` (required): Comma-separated list of options (2-10 options)
- `duration` (optional): Duration in minutes (default: 60, range: 10-1440)

**Examples:**
```
/poll question:"What's your favorite programming language?" options:"Python, JavaScript, Java, C++" duration:120

/poll question:"When should we have the meeting?" options:"Monday 9AM, Tuesday 2PM, Wednesday 10AM" duration:30
```

### `/quickpoll` - Yes/No Polls
Create simple Yes/No polls for quick decisions.

**Syntax:**
```
/quickpoll question:"Your yes/no question" duration:30
```

**Parameters:**
- `question` (required): The yes/no question
- `duration` (optional): Duration in minutes (default: 30, range: 10-1440)

**Examples:**
```
/quickpoll question:"Should we order pizza for lunch?" duration:15

/quickpoll question:"Is everyone ready for the deployment?" duration:5
```

## Features

### 🎯 Smart Voting System
- **Emoji Reactions**: Users vote by clicking emoji reactions
- **Multi-option**: Number emojis (1️⃣2️⃣3️⃣) for regular polls
- **Yes/No**: ✅❌ emojis for quick polls
- **One Vote Per User**: Discord's reaction system prevents duplicate voting

### 📊 Automatic Results
- **Live Counting**: Votes are counted from message reactions
- **Visual Progress**: Progress bars show vote distribution
- **Rankings**: Winners get medals (🥇🥈🥉)
- **Percentages**: Shows vote percentages for each option
- **Auto-End**: Polls automatically end and show results

### ⏰ Flexible Timing
- **Custom Duration**: Set polls from 10 seconds to 24 hours
- **Auto-Scheduling**: Polls end automatically after the set time
- **Time Display**: Shows remaining time and creator info

### 🎨 Beautiful Display
- **Rich Embeds**: Colorful, professional-looking poll displays
- **Clear Options**: Easy-to-read option lists
- **Status Updates**: Different colors for active vs completed polls
- **User Attribution**: Shows who created each poll

## Use Cases

### 🏢 Business Decisions
```
/poll question:"Which feature should we prioritize next?" options:"User Dashboard, API Integration, Mobile App, Analytics" duration:180
```

### 🍕 Team Coordination
```
/quickpoll question:"Should we have the standup at 9 AM or 10 AM?" duration:60
```

### 🎮 Community Engagement
```
/poll question:"What game should we play this weekend?" options:"Among Us, Minecraft, Valorant, Fall Guys" duration:120
```

### 📅 Event Planning
```
/poll question:"Best day for the team outing?" options:"Saturday, Sunday, Next Friday" duration:240
```

## Technical Details

### Validation
- ✅ Minimum 2 options, maximum 10 options
- ✅ Duration between 10 seconds and 24 hours (1440 minutes)
- ✅ Automatic input sanitization
- ✅ Error handling with helpful messages

### Vote Counting
- Counts reactions on the poll message
- Excludes the bot's own reactions
- Handles users removing/changing votes
- Real-time accurate counting

### Results Display
- Sorted by vote count (highest first)
- Visual progress bars using block characters
- Percentage calculations
- Medal system for top 3 options
- Total vote count display

## Tips for Best Results

1. **Clear Questions**: Make your poll questions specific and easy to understand
2. **Reasonable Options**: Keep options concise and distinct
3. **Appropriate Duration**: 
   - Quick decisions: 10-30 minutes
   - Team decisions: 1-3 hours
   - Community polls: 6-24 hours
4. **Option Limits**: Use 2-5 options for best engagement
5. **Timing**: Post polls when your target audience is most active

## Error Handling

The system provides helpful error messages for:
- Too few options (< 2)
- Too many options (> 10)
- Invalid duration (< 10 seconds or > 24 hours)
- Malformed option lists
- Permission issues

## Future Enhancements

Potential features for future versions:
- Anonymous voting options
- Poll templates
- Recurring polls
- Vote export/analysis
- Integration with calendar systems
- Multi-server poll synchronization

---

**Ready to start polling?** Try creating your first poll with:
```
/quickpoll question:"Is this polling system awesome?" duration:5
```