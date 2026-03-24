import json
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from mcp.server.fastmcp import FastMCP

CONFIG_PATH = Path(__file__).parent / "config.json"

mcp = FastMCP("smtp-email")


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


@mcp.tool()
def send_email(
    to: str,
    subject: str,
    body: str,
    cc: str = "",
    bcc: str = "",
    html: bool = False,
) -> str:
    """Send an email via SMTP.

    Args:
        to: Recipient email address (or comma-separated list).
        subject: Email subject line.
        body: Email body content.
        cc: CC recipients (comma-separated, optional).
        bcc: BCC recipients (comma-separated, optional).
        html: Set to true to send body as HTML, false for plain text.
    """
    cfg = load_config()

    msg = MIMEMultipart("alternative")
    msg["From"] = cfg["from_address"]
    msg["To"] = to
    msg["Subject"] = subject
    if cc:
        msg["Cc"] = cc
    if bcc:
        msg["Bcc"] = bcc

    mime_type = "html" if html else "plain"
    msg.attach(MIMEText(body, mime_type))

    recipients = [addr.strip() for addr in to.split(",")]
    if cc:
        recipients += [addr.strip() for addr in cc.split(",")]
    if bcc:
        recipients += [addr.strip() for addr in bcc.split(",")]

    context = ssl.create_default_context()
    with smtplib.SMTP(cfg["smtp_server"], cfg["smtp_port"]) as server:
        server.ehlo()
        server.starttls(context=context)
        server.login(cfg["username"], cfg["password"])
        server.sendmail(cfg["from_address"], recipients, msg.as_string())

    return f"Email sent successfully to {to}"


if __name__ == "__main__":
    mcp.run()
