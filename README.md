# mcp-smtp

An MCP (Model Context Protocol) server that enables Claude to send emails via SMTP.

(Written with help from Claude)
<img width="641" height="342" alt="image" src="https://github.com/user-attachments/assets/1218fc84-f8da-4e05-a401-602172581f4b" />


## Features

- Send plain text or HTML emails
- Support for CC and BCC recipients
- Configurable via a simple JSON config file
- Uses STARTTLS for secure connections

## Requirements

- Python 3.10+
- `mcp[cli]` package

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Edit `config.json` with your SMTP provider details:

```json
{
  "smtp_server": "smtp.example.com",
  "smtp_port": 587,
  "username": "your-username",
  "password": "your-password",
  "from_address": "you@example.com"
}
```

| Field | Description |
|---|---|
| `smtp_server` | Hostname of your SMTP server |
| `smtp_port` | SMTP port (typically `587` for STARTTLS) |
| `username` | SMTP authentication username |
| `password` | SMTP authentication password |
| `from_address` | The email address that will appear in the From field |

## Usage with Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "smtp-email": {
      "command": "python",
      "args": ["/path/to/mcp-smtp/server.py"]
    }
  }
}
```

Restart Claude Desktop. Claude will now have access to the `send_email` tool.

## Tool Reference

### `send_email`

Sends an email via the configured SMTP server.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `to` | string | Yes | Recipient address(es), comma-separated |
| `subject` | string | Yes | Email subject line |
| `body` | string | Yes | Email body content |
| `cc` | string | No | CC recipient(s), comma-separated |
| `bcc` | string | No | BCC recipient(s), comma-separated |
| `html` | boolean | No | Send body as HTML (default: `false`) |

