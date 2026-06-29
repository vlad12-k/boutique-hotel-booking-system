# Telegram Staff Bot Workflow

## Purpose

The Telegram staff bot extends the boutique hotel booking system by adding a two-way operational communication channel between the hotel system and authorised staff. The earlier API extension sent outbound Telegram notifications when housekeeping action was required. This additional layer allows staff to interact with the system from Telegram by checking room status, viewing rooms that require cleaning, marking rooms as ready, moving rooms into maintenance and reviewing recent notification logs.

## Implemented Communication Model

The system now supports two forms of Telegram API communication:

1. **System-to-staff notifications**
   - Guest check-out changes a room status to `Cleaning`.
   - The system sends a Telegram housekeeping alert.
   - The result is stored in the `NotificationLog` table.

2. **Staff-to-system commands**
   - Staff send commands to the Telegram bot.
   - The bot worker receives updates through Telegram long polling.
   - The command service performs the requested room or notification action.
   - The worker sends a response back to the authorised Telegram chat.

## Supported Staff Commands

| Command | Purpose | Expected response |
|---|---|---|
| `/help` | Shows available staff commands | List of supported commands |
| `/status` | Shows a count summary of room statuses | Room status summary |
| `/cleaning` | Lists rooms waiting for housekeeping | Rooms with `Cleaning` status |
| `/available` | Lists rooms currently available | Rooms with `Available` status |
| `/ready <room number>` | Marks a cleaned room as `Available` | Confirmation message and notification log entry |
| `/maintenance <room number>` | Marks a room as `Maintenance` | Confirmation message and notification log entry |
| `/notifications` | Shows recent notification log entries | Latest notification records |

## Security Controls

Telegram credentials and authorised staff chat IDs are stored as environment variables rather than hardcoded in source code.

The following environment variables are used:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_housekeeping_chat_id
TELEGRAM_ALLOWED_CHAT_IDS=your_authorised_staff_chat_ids
TELEGRAM_POLL_INTERVAL_SECONDS=3
```

The worker checks every incoming Telegram message against the configured authorised chat IDs. If an unauthorised chat sends a command, the bot responds with an access denied message and does not process the request.

## Local Demo Execution

The local demonstration uses two terminal sessions.

### Terminal 1: Flask application

```bash
python app.py
```

This runs the hotel booking system and exposes the web interface and JSON API endpoints.

### Terminal 2: Telegram staff bot worker

```bash
python telegram_bot_worker.py
```

This worker receives Telegram updates, validates the chat ID, routes valid commands to the command service and sends a Telegram response.

## Testing Evidence

The automated test suite checks that the command service returns correct responses for the help command, unknown commands and commands missing required room numbers. This protects the command parser from basic regressions before live Telegram testing.

The latest validation result was:

```text
10 passed
```

## Live Test Plan

The following screenshots should be collected for the appendix:

| Appendix item | Evidence |
|---|---|
| A16.1 | Telegram `/help` command showing available staff commands |
| A16.2 | Telegram `/status` command showing room status summary |
| A16.3 | Telegram `/cleaning` command listing rooms waiting for housekeeping |
| A16.4 | Telegram `/ready 103` command confirming that a room was marked as available |
| A16.5 | Rooms page showing the room status updated after the Telegram command |
| A16.6 | Notification log showing the Telegram command action recorded |
| A16.7 | `/api/notifications` showing the Telegram command action as structured JSON |
| A16.8 | Access control evidence showing unauthorised chat rejection, if available |

## Evaluation Notes

The Telegram staff bot improves the original API extension because it supports both outbound alerts and staff-driven operational actions. This makes the workflow closer to a real hotel environment, where housekeeping staff may need to check current work, update room status and confirm task completion quickly without opening the full web application.

The main limitation is that the current implementation uses long polling for local demonstration. In a production environment, the worker could be replaced or extended with a secure Telegram webhook endpoint hosted on a deployed server.
