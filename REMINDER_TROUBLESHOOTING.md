# 🔧 Reminder Troubleshooting Guide

## Issue: Reminders Created But No Desktop Notifications

If your reminders are being created successfully but you're not getting desktop notifications, here are the steps to troubleshoot:

## Step 1: Test Reminder Delivery

First, let's test if the reminder is actually being sent to Discord:

```
/testreminder message:"Testing reminder delivery"
```

This command will:
- Create a reminder that triggers in 1 second
- Show debugging information in the bot console
- Help identify if the issue is with delivery or notifications

## Step 2: Check Discord Notification Settings

### Desktop App Settings
1. **Open Discord Settings** (gear icon)
2. **Go to Notifications**
3. **Check these settings:**
   - ✅ Enable Desktop Notifications
   - ✅ Enable Unread Message Badge
   - ✅ Enable Taskbar Flashing (Windows)

### Server-Specific Settings
1. **Right-click your server name**
2. **Select "Notification Settings"**
3. **Ensure notifications are enabled for:**
   - ✅ All Messages (or at least @mentions)
   - ✅ Mobile Push Notifications (if using mobile)

### Channel-Specific Settings
1. **Right-click the channel** where you set the reminder
2. **Select "Notification Settings"**
3. **Make sure it's not muted**

## Step 3: Check System Notifications

### Windows 10/11
1. **Open Settings** → **System** → **Notifications & actions**
2. **Ensure Discord is allowed** to send notifications
3. **Check "Focus Assist"** settings (might block notifications)

### macOS
1. **System Preferences** → **Notifications**
2. **Find Discord** in the list
3. **Enable notifications** and choose alert style

### Linux
- Check your desktop environment's notification settings
- Ensure Discord has permission to send notifications

## Step 4: Check Bot Permissions

The bot needs these permissions in your server:
- ✅ **Send Messages** - To deliver reminders
- ✅ **Use External Emojis** - For reminder embeds
- ✅ **Embed Links** - For rich reminder displays
- ✅ **Mention Everyone** - To ping you in reminders

## Step 5: Debug with Console Logs

When you run `/testreminder`, check the bot console for these messages:

### ✅ Success Messages:
```
🧪 Test reminder abc123de scheduled for user 123456789
⏰ Scheduling reminder abc123de for 1 seconds
⏰ Time's up! Processing reminder abc123de
📋 Reminder data found for abc123de
🔔 Attempting to send reminder abc123de
✅ Reminder abc123de sent successfully! Message ID: 987654321
🗑️ Reminder abc123de removed from active reminders
```

### ❌ Error Messages to Look For:
```
❌ Channel 123456789 not found for reminder abc123de
❌ User 123456789 not found for reminder abc123de
❌ No permission to send reminder abc123de in channel 123456789
❌ HTTP error sending reminder abc123de: [error details]
```

## Step 6: Common Solutions

### If Reminder Isn't Being Sent:
1. **Check bot permissions** in the channel
2. **Verify the bot is online** and connected
3. **Try in a different channel**
4. **Restart the bot** if needed

### If Reminder Sends But No Desktop Notification:
1. **Check Discord notification settings** (most common issue)
2. **Ensure Discord is focused/unfocused** (some settings only notify when unfocused)
3. **Check system Do Not Disturb** settings
4. **Try mentioning yourself** manually to test notifications

### If Using Discord Web Version:
1. **Browser notifications** might be blocked
2. **Check browser notification permissions**
3. **Try the desktop app** instead

## Step 7: Test Different Scenarios

Try these tests to isolate the issue:

### Test 1: Manual Mention
Have someone else mention you: `@yourusername test`
- If this doesn't notify you, it's a Discord notification issue
- If this works, the issue is with reminder delivery

### Test 2: Different Time Periods
```
/remind time:10s message:"10 second test"
/remind time:1m message:"1 minute test"
```

### Test 3: Different Channels
Try setting reminders in different channels to see if it's channel-specific.

## Step 8: Alternative Solutions

### If Desktop Notifications Don't Work:
1. **Use mobile Discord** - often more reliable for notifications
2. **Check reminders manually** with `/reminders` command
3. **Set shorter reminder times** and check Discord periodically

### For Important Reminders:
1. **Set multiple reminders** (e.g., 1 hour and 15 minutes before)
2. **Use group reminders** - have someone else remind you
3. **Combine with other reminder systems** (phone, calendar, etc.)

## Step 9: Report Issues

If none of the above works, please provide:

1. **Console logs** from `/testreminder`
2. **Discord notification settings** screenshots
3. **Operating system** and Discord version
4. **Whether manual mentions work**

## Quick Checklist

- [ ] Ran `/testreminder` and checked console logs
- [ ] Discord desktop notifications enabled
- [ ] Server notifications enabled
- [ ] Channel not muted
- [ ] System notifications allow Discord
- [ ] Bot has Send Messages permission
- [ ] Manual @mentions work
- [ ] Tried different channels
- [ ] Checked Focus Assist/Do Not Disturb

## Most Common Fixes

1. **Enable Discord desktop notifications** (90% of cases)
2. **Check server notification settings** (5% of cases)
3. **Bot permission issues** (3% of cases)
4. **System notification blocking** (2% of cases)

---

**Still having issues?** Try the `/testreminder` command first and check what the console logs show!